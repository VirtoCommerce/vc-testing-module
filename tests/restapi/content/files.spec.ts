import type { ContentType } from "@api/rest/types/content";

import * as allure from "allure-js-commons";

import { ContentClient, contentPath } from "@api/rest/clients/content-client";
import { uniqueId } from "@core/unique-id";
import { FORBIDDEN_EXTENSION, newMarkdownFile } from "@dataset/builders/content";
import { getCredentials } from "@dataset/dataset";
import { expect, test } from "@fixtures";

const USERNAME = "acme_store_administrator@acme.com";
const SEARCHABLE_CONTENT_TYPES: readonly ContentType[] = ["pages", "blogs", "themes"];

test.beforeEach(async () => {
  await allure.feature("Content / Files");
});

test.describe("content files (admin)", () => {
  test.use({ user: async ({ dataset }, use) => use(getCredentials(dataset, USERNAME)) });

  test("get content statistic", async ({ httpClient, env }) => {
    const contentClient = new ContentClient(httpClient, env.storeId);

    const statistic = await test.step("act: get content statistic", () => contentClient.getStatistic());

    await test.step("assert: statistic reports pages, blogs and themes counts", async () => {
      expect(statistic).toMatchObject({
        pagesCount: expect.any(Number),
        blogsCount: expect.any(Number),
        themesCount: expect.any(Number),
      });
    });
  });

  for (const contentType of SEARCHABLE_CONTENT_TYPES) {
    test(`find a folder in ${contentType}`, async ({ httpClient, cleanupStack, env }) => {
      const contentClient = new ContentClient(httpClient, env.storeId);
      const folderName = uniqueId("test-folder");
      cleanupStack.push(`remove ${contentType} folder ${folderName}`, () =>
        contentClient.removeFolder(contentType, folderName),
      );
      await test.step("arrange: folder", () => contentClient.createFolder(contentType, folderName));

      const found = await test.step("act: search by folder name", () => contentClient.search(contentType, folderName));

      await test.step("assert: folder is found", async () => {
        expect(found).toContainEqual(expect.objectContaining({ name: folderName, type: "folder" }));
      });
    });
  }

  test("upload, rename and delete a page", async ({ httpClient, cleanupStack, env }) => {
    const contentClient = new ContentClient(httpClient, env.storeId);
    const folderName = uniqueId("test-folder");
    const file = newMarkdownFile("test-page");
    const renamedFileName = `renamed-${file.name}`;
    cleanupStack.push(`remove pages folder ${folderName}`, () => contentClient.removeFolder("pages", folderName));
    await test.step("arrange: folder", () => contentClient.createFolder("pages", folderName));

    await test.step("act: upload page", () => contentClient.upload("pages", folderName, file));
    const page = await test.step("assert: page is found with its content", async () => {
      const found = await contentClient.getByName("pages", file.name);
      expect(await contentClient.getFileContent("pages", found.relativeUrl)).toBe(file.buffer.toString());
      return found;
    });
    const renamedUrl = page.url.replace(file.name, renamedFileName);

    await test.step("act: rename page", () => contentClient.move("pages", page.url, renamedUrl));
    await test.step("assert: page is found by the new name", async () => {
      expect(await contentClient.getByName("pages", renamedFileName)).toMatchObject({ url: renamedUrl });
    });

    await test.step("act: delete page", () => contentClient.delete("pages", renamedUrl));
    await test.step("assert: page is not found", async () => {
      expect(await contentClient.findByName("pages", renamedFileName)).toBeUndefined();
    });
  });

  test("upload, rename and delete a blog post", async ({ httpClient, cleanupStack, env }) => {
    const contentClient = new ContentClient(httpClient, env.storeId);
    const folderName = uniqueId("test-folder");
    const file = newMarkdownFile("test-post");
    const renamedFileName = `renamed-${file.name}`;
    cleanupStack.push(`remove blogs folder ${folderName}`, () => contentClient.removeFolder("blogs", folderName));
    await test.step("arrange: blog folder", () => contentClient.createFolder("blogs", folderName));
    await test.step("arrange: uploaded post", () => contentClient.upload("blogs", folderName, file));
    const post = await test.step("arrange: located post", () => contentClient.getByName("blogs", file.name));
    const renamedUrl = post.url.replace(file.name, renamedFileName);

    const forbiddenRename = await test.step(`act: rename post to ${FORBIDDEN_EXTENSION}`, () =>
      httpClient.get(`${contentPath("blogs", env.storeId)}/move`, {
        query: { oldUrl: post.url, newUrl: post.url.replace(".md", FORBIDDEN_EXTENSION) },
      }));
    await test.step(`assert: rename to ${FORBIDDEN_EXTENSION} is rejected`, async () => {
      expect(forbiddenRename.ok).toBe(false);
      expect(forbiddenRename.text).toContain(`File extension ${FORBIDDEN_EXTENSION} is not allowed`);
    });

    await test.step("act: rename post", () => contentClient.move("blogs", post.url, renamedUrl));
    await test.step("assert: post is found by the new name", async () => {
      expect(await contentClient.getByName("blogs", renamedFileName)).toMatchObject({ url: renamedUrl });
    });

    await test.step("act: delete post", () => contentClient.delete("blogs", renamedUrl));
    await test.step("assert: post content is gone", async () => {
      expect(await contentClient.getFileContent("blogs", post.relativeUrl)).toBeUndefined();
      expect(await contentClient.findByName("blogs", renamedFileName)).toBeUndefined();
    });
  });

  test("rename and delete a theme folder", async ({ httpClient, cleanupStack, env }) => {
    const contentClient = new ContentClient(httpClient, env.storeId);
    const folderName = uniqueId("test-theme");
    const renamedFolderName = `${folderName}-renamed`;
    cleanupStack.push(`remove themes folder ${folderName}`, () => contentClient.removeFolder("themes", folderName));
    cleanupStack.push(`remove themes folder ${renamedFolderName}`, () =>
      contentClient.removeFolder("themes", renamedFolderName),
    );
    await test.step("arrange: theme folder", () => contentClient.createFolder("themes", folderName));
    const folder = await test.step("arrange: located theme folder", () =>
      contentClient.getByName("themes", folderName));
    const renamedUrl = folder.url.replace(folderName, renamedFolderName);

    await test.step("act: rename theme folder", () => contentClient.move("themes", folder.url, renamedUrl));
    await test.step("assert: theme folder is found by the new name", async () => {
      expect(await contentClient.getByName("themes", renamedFolderName)).toMatchObject({ type: "folder" });
    });

    await test.step("act: delete theme folder", () => contentClient.delete("themes", renamedUrl));
    await test.step("assert: theme folder is not found", async () => {
      expect(await contentClient.findByName("themes", renamedFolderName)).toBeUndefined();
    });
  });

  test("upload and unpack a theme archive", async () => {
    test.fixme(true, "Needs a theme .zip fixture with a known internal file (Katalon used qwetheme_test_x.zip)");
  });
});
