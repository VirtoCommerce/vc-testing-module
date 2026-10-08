# [Platform] Signing in the same user in parallel sometimes returns HTTP 500 from `/connect/token`

| Field | Value |
|---|---|
| **Type** | Bug |
| **Component** | Platform / Security (OpenIddict token endpoint) |
| **Priority** | Medium |
| **Environment** | Local platform `http://localhost:8090`, PostgreSQL, store `store-acme` |
| **Platform version** | 3.1074.0 (`GET /api/platform/diagnostics/systeminfo`) |
| **Found by** | Automated test suite (`vc-testing-module`, Playwright with 8 workers) |

## Summary

If the same user requests a token from `POST /connect/token` (password grant) several times at once, some of the requests fail with **HTTP 500**. They return the HTML "Virto Commerce Error" page instead of a token. The same number of parallel sign-ins spread across **different** users all succeed, and so do sign-ins of one user made one after another.

## Steps to reproduce

1. Start the platform, and have one active user (for example `admin`).
2. Send 8 `POST /connect/token` requests for that user at the same moment:
   - `Content-Type: application/x-www-form-urlencoded`
   - body: `grant_type=password&username=<user>&password=<password>&scope=offline_access`
3. Repeat step 2 ten times (80 requests in total).
4. For comparison, send the same 80 requests one after another, or in parallel but with a different user in each request.

Reproduction script (Node 22, no dependencies):

```js
// token-race.mjs — usage: U=admin P=<password> BASE=http://localhost:8090 node token-race.mjs
const base = process.env.BASE ?? "http://localhost:8090";
const { U: username, P: password } = process.env;

async function signIn() {
  const body = new URLSearchParams({ grant_type: "password", username, password, scope: "offline_access" });
  const response = await fetch(`${base}/connect/token`, { method: "POST", body });
  const text = await response.text();
  return { status: response.status, requestId: /Request ID:<\/strong>\s*<code>([^<]+)/.exec(text)?.[1] };
}

let failed = 0;
const requestIds = [];
for (let round = 0; round < 10; round++) {
  const results = await Promise.all(Array.from({ length: 8 }, signIn));
  for (const result of results.filter(({ status }) => status >= 500)) {
    failed += 1;
    requestIds.push(result.requestId);
  }
}
console.log(`same user, 10 x 8 parallel: ${failed}/80 failed with 5xx`, requestIds.slice(0, 5));
```

## Actual result

| Scenario | Requests | Failed with 500 |
|---|---|---|
| Same user (`admin`), 8 in parallel × 10 rounds | 80 | **63** |
| 8 different users (`acme_store_employee_1..8@acme.com`), 8 in parallel × 10 rounds | 80 | 0 |
| Same user, one after another | 20 | 0 |
| Same user, one extra round of 8 in parallel | 8 | 4 |

Measured on 2026-09-30. An earlier run the same day gave 57/80 for the same-user scenario.

The failing responses are `500 Internal Server Error` with the HTML error page ("An error occurred while processing your request.") and a **Request ID**. Examples from the last run:

- `00-0e1d440304249ec9fc7840003e0e17e3-186de7a24abebf4f-00`
- `00-58ff46f0e471c91f62b2a8c979b4e1c3-fecb86e275f09650-00`

The script above prints the request IDs, so you can find the matching exception in the platform log.

## Expected result

Every request with valid credentials returns `200` with a token, however many sign-ins of the same user run at the same time. If concurrency really has to be limited, the endpoint should return a well-formed OAuth error (for example `429`, or `400` with an `error` code), not an unhandled 500.

## Impact

- Any client that signs in one account from several processes at once hits this intermittently: parallel test workers, several frontend instances, or integrations sharing a service account.
- In our test suite, the first test on each worker sometimes fails before it runs, because all workers sign in the same admin when the run starts. Client-side retries only reduce how often this happens.

## Notes for investigation

- The failures only happen with concurrent requests for the **same** user, which points to a race in per-user state written during the password grant. Candidates:
  - a concurrency/optimistic-lock conflict on the user record (security stamp, `LastLoginDate`, access-failed count);
  - concurrent creation of OpenIddict authorizations or tokens for the same subject.
- The platform log entries for the Request IDs above should show the exact exception and stack trace.

## Workaround

Retry `/connect/token` on 5xx with exponential backoff and jitter, or sign in once and share the token between processes.
