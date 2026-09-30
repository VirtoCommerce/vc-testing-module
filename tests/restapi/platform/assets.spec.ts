import * as allure from "allure-js-commons";

import { ASSETS_PATH, AssetsClient } from "@api/rest/clients/assets-client";
import { uniqueId } from "@core/unique-id";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const MARKDOWN_FILE_URL = "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/README.md";
const DOTFILE_URL = "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/.gitignore";

test.beforeEach(async () => {
  await allure.feature("Platform / Assets");
});

test.describe("platform assets (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  for (const { title, url, name } of [
    { title: "a markdown file", url: MARKDOWN_FILE_URL, name: "README.md" },
    { title: "a dotfile", url: DOTFILE_URL, name: ".gitignore" },
  ]) {
    test(`upload ${title} from a URL`, async ({ httpClient, cleanupStack }) => {
      const assetsClient = new AssetsClient(httpClient);
      const folderName = uniqueId("test-folder");
      cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));

      const file = await test.step("act: upload file from URL", () => assetsClient.uploadFromUrl(folderName, url));

      await test.step("assert: file is in the folder", async () => {
        expect(file.name).toBe(name);
        expect((await assetsClient.list(folderName)).map((entry) => entry.name)).toContain(name);
      });
    });
  }

  test("upload a local file", async ({ httpClient, cleanupStack }) => {
    const assetsClient = new AssetsClient(httpClient);
    const folderName = uniqueId("test-folder");
    cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));
    const content = "Test asset content";

    const file = await test.step("act: upload local file", () =>
      assetsClient.upload(folderName, {
        name: "test-local.txt",
        mimeType: "text/plain",
        buffer: Buffer.from(content),
      }));

    await test.step("assert: file is in the folder", async () => {
      expect(file).toMatchObject({ name: "test-local.txt", url: expect.stringContaining(folderName) });
    });
  });

  test("upload a file to local storage", async ({ httpClient }) => {
    const assetsClient = new AssetsClient(httpClient);
    const name = `${uniqueId("test-local-storage")}.txt`;

    const file = await test.step("act: upload file to local storage", () =>
      assetsClient.uploadToLocalStorage({ name, mimeType: "text/plain", buffer: Buffer.from("Test storage content") }));

    await test.step("assert: file is stored under its name", async () => {
      expect(file.name).toBe(name);
    });
  });

  test("download an uploaded file", async ({ httpClient, cleanupStack }) => {
    const assetsClient = new AssetsClient(httpClient);
    const folderName = uniqueId("test-folder");
    cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));
    const content = "Test downloadable content";
    const file = await test.step("arrange: uploaded file", () =>
      assetsClient.upload(folderName, {
        name: "test-download.txt",
        mimeType: "text/plain",
        buffer: Buffer.from(content),
      }));

    const response = await test.step("act: download file", () => httpClient.get(file.url));

    await test.step("assert: file content is served", async () => {
      expect(response.status).toBe(200);
      expect(response.text).toBe(content);
    });
  });

  test("a deleted file is not served", async ({ httpClient, cleanupStack }) => {
    const assetsClient = new AssetsClient(httpClient);
    const folderName = uniqueId("test-folder");
    cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));
    const file = await test.step("arrange: uploaded file", () =>
      assetsClient.upload(folderName, {
        name: "test-deleted.txt",
        mimeType: "text/plain",
        buffer: Buffer.from("gone"),
      }));

    await test.step("act: delete file", () => assetsClient.remove(file.url));

    await test.step("assert: file is not found", async () => {
      expect((await httpClient.get(file.url)).status).toBe(404);
    });
  });

  test("create a folder", async ({ httpClient, cleanupStack }) => {
    const assetsClient = new AssetsClient(httpClient);
    const folderName = uniqueId("test-folder");
    cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));

    await test.step("act: create folder", () => assetsClient.createFolder(folderName));

    await test.step("assert: folder is listed", async () => {
      expect(await assetsClient.find(folderName)).toMatchObject({ name: folderName, type: "folder" });
    });
  });

  test("list assets in a folder", async ({ httpClient, cleanupStack }) => {
    const assetsClient = new AssetsClient(httpClient);
    const folderName = uniqueId("test-folder");
    cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));
    await test.step("arrange: uploaded file", () =>
      assetsClient.upload(folderName, { name: "test-listed.txt", mimeType: "text/plain", buffer: Buffer.from("x") }));

    const entries = await test.step("act: list folder", () => assetsClient.list(folderName));

    await test.step("assert: folder lists the file", async () => {
      expect(entries.map(({ name }) => name)).toEqual(["test-listed.txt"]);
    });
  });

  test("delete a folder", async ({ httpClient, cleanupStack }) => {
    const assetsClient = new AssetsClient(httpClient);
    const folderName = uniqueId("test-folder");
    cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));
    await test.step("arrange: folder", () => assetsClient.createFolder(folderName));

    await test.step("act: delete folder", () => assetsClient.removeFolder(folderName));

    await test.step("assert: folder is not listed", async () => {
      expect(await assetsClient.find(folderName)).toBeUndefined();
    });
  });

  test("create and delete folders in bulk", async ({ httpClient, cleanupStack }) => {
    const assetsClient = new AssetsClient(httpClient);
    const folderNames = [uniqueId("test-folder"), uniqueId("test-folder"), uniqueId("test-folder")];
    for (const folderName of folderNames) {
      cleanupStack.push(`remove folder ${folderName}`, () => assetsClient.removeFolder(folderName));
    }
    await test.step("arrange: three folders", () =>
      Promise.all(folderNames.map((folderName) => assetsClient.createFolder(folderName))));
    const folders = await assetsClient.list();
    const urls = folders.filter(({ name }) => folderNames.includes(name)).map(({ url }) => url);

    await test.step("act: delete the folders in one request", () => assetsClient.removeMany(urls));

    await test.step("assert: no folder is listed", async () => {
      const remaining = (await assetsClient.list()).map(({ name }) => name);
      expect(folderNames.filter((folderName) => remaining.includes(folderName))).toEqual([]);
    });
  });

  test("reject a folder without a name", async ({ httpClient }) => {
    const response = await test.step("act: create folder with an empty name", () =>
      httpClient.post(`${ASSETS_PATH}/folder`, { json: { name: "", parentUrl: "" } }));

    await test.step("assert: folder name is required", async () => {
      expect(response.status).toBe(400);
      expect(response.text).toContain("Folder name must not be empty");
    });
  });
});
