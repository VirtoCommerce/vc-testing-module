from typing import Optional
import allure, json, pytest, requests


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize Web API Client")
def webapi_client(config, auth):
    class WebAPISession(requests.Session):
        def update_auth_headers(self):
            auth_headers = auth.get_auth_headers()

            if auth_headers:
                self.headers.update(auth_headers)
            else:
                self.headers.pop("Authorization", None)

        def send_request(self, method: str, endpoint: str, **kwargs):
            self.update_auth_headers()

            url = f"{config['backend_base_url']}{endpoint}"

            response = super().request(method, url, **kwargs)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")

            if "application/json" in content_type:
                return response.json()
            elif "text/" in content_type:
                return response.text
            elif "application/octet-stream" in content_type:
                return response.content
            else:
                return response.text

        def get(self, endpoint: str, params: Optional[dict] = None, **kwargs):
            return self.send_request("GET", endpoint, params=params, **kwargs)

        def post(self, endpoint: str, data: Optional[dict] = None, **kwargs):
            return self.send_request("POST", endpoint, data=json.dumps(data), **kwargs)

        def put(self, endpoint: str, data: Optional[dict] = None, **kwargs):
            return self.send_request("PUT", endpoint, data=json.dumps(data), **kwargs)

        def delete(self, endpoint: str, **kwargs):
            return self.send_request("DELETE", endpoint, **kwargs)

        def patch(self, endpoint: str, data: Optional[dict] = None, **kwargs):
            return self.send_request("PATCH", endpoint, data=json.dumps(data), **kwargs)

        def request(self, method: str, endpoint: str, data: Optional[dict] = None, **kwargs):
            return self.send_request(method, endpoint, data=json.dumps(data), **kwargs)

    session = WebAPISession()
    session.headers.update({"Content-Type": "application/json"})

    return session
