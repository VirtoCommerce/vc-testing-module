"""Dynamic content CRUD — migrated from Katalon `API Coverage/ModuleMarketing/DynamicContent/*` + `dynamicContent/*` + `contentItem/*`.

Katalon scripts:
  ContentFolders      → test_folder_create, test_folder_get, test_folder_update, test_folder_delete
  ContentItems        → test_item_create, test_item_get, test_item_update, test_item_search, test_item_delete, test_item_delete_bulk
  ContentPlaceholders → test_place_create, test_place_get, test_place_update, test_place_search, test_place_delete, test_place_delete_bulk
  ContentPublications → test_pub_create, test_pub_get_new, test_pub_get, test_pub_update, test_pub_search, test_pub_delete, test_pub_delete_bulk
"""

import uuid

import allure
import pytest

from restapi.operations import (
    ContentFolderOperations,
    ContentItemOperations,
    ContentPlaceOperations,
    ContentPublicationOperations,
)


# ── Content Folders ──


@pytest.mark.restapi
@allure.feature("Marketing / Content Folders (REST API)")
@allure.title("Create content folder")
def test_folder_create(make_content_folder):
    with allure.step("POST /api/marketing/contentfolders"):
        folder = make_content_folder()
    assert folder["id"]
    assert folder["name"].startswith("QAFolder_")


@pytest.mark.restapi
@allure.feature("Marketing / Content Folders (REST API)")
@allure.title("Get content folder by id")
def test_folder_get(make_content_folder, content_folder_ops: ContentFolderOperations):
    folder = make_content_folder()
    with allure.step(f"GET /api/marketing/contentfolders/{folder['id']}"):
        reloaded = content_folder_ops.get_by_id(folder["id"])
    assert reloaded["id"] == folder["id"]


@pytest.mark.restapi
@allure.feature("Marketing / Content Folders (REST API)")
@allure.title("Update content folder")
def test_folder_update(make_content_folder, content_folder_ops: ContentFolderOperations):
    folder = make_content_folder()
    new_name = f"{folder['name']}_UPD"
    with allure.step("PUT /api/marketing/contentfolders"):
        content_folder_ops.update(folder, name=new_name)
    reloaded = content_folder_ops.get_by_id(folder["id"])
    assert reloaded["name"] == new_name


@pytest.mark.restapi
@allure.feature("Marketing / Content Folders (REST API)")
@allure.title("Delete content folder")
def test_folder_delete(content_folder_ops: ContentFolderOperations):
    folder = content_folder_ops.create(name=f"QADelFolder_{uuid.uuid4().hex[:8]}")
    with allure.step(f"DELETE /api/marketing/contentfolders?ids={folder['id']}"):
        content_folder_ops.delete(folder["id"])


# ── Content Items ──


@pytest.mark.restapi
@allure.feature("Marketing / Content Items (REST API)")
@allure.title("Create content item")
def test_item_create(make_content_item):
    with allure.step("POST /api/marketing/contentitems"):
        item = make_content_item()
    assert item["id"]


@pytest.mark.restapi
@allure.feature("Marketing / Content Items (REST API)")
@allure.title("Get content item by id")
def test_item_get(make_content_item, content_item_ops: ContentItemOperations):
    item = make_content_item()
    with allure.step(f"GET /api/marketing/contentitems/{item['id']}"):
        reloaded = content_item_ops.get_by_id(item["id"])
    assert reloaded["id"] == item["id"]


@pytest.mark.restapi
@allure.feature("Marketing / Content Items (REST API)")
@allure.title("Update content item")
def test_item_update(make_content_item, content_item_ops: ContentItemOperations):
    item = make_content_item()
    new_desc = f"Updated_{uuid.uuid4().hex[:6]}"
    with allure.step("PUT /api/marketing/contentitems — description"):
        content_item_ops.update(item, description=new_desc)
    with allure.step("Verify update"):
        reloaded = content_item_ops.get_by_id(item["id"])
        assert reloaded.get("description") == new_desc


@pytest.mark.restapi
@allure.feature("Marketing / Content Items (REST API)")
@allure.title("Search content items")
def test_item_search(make_content_item, content_item_ops: ContentItemOperations):
    item = make_content_item()
    with allure.step("POST /api/marketing/contentitems/search"):
        result = content_item_ops.search()
    assert result is not None


@pytest.mark.restapi
@allure.feature("Marketing / Content Items (REST API)")
@allure.title("Delete content item")
def test_item_delete(content_item_ops: ContentItemOperations):
    item = content_item_ops.create(name=f"QADelItem_{uuid.uuid4().hex[:8]}")
    with allure.step(f"DELETE /api/marketing/contentitems?ids={item['id']}"):
        content_item_ops.delete(item["id"])


@pytest.mark.restapi
@allure.feature("Marketing / Content Items (REST API)")
@allure.title("Delete content items in bulk")
def test_item_delete_bulk(content_item_ops: ContentItemOperations):
    suffix = uuid.uuid4().hex[:6]
    i1 = content_item_ops.create(name=f"QABulk1_{suffix}")
    i2 = content_item_ops.create(name=f"QABulk2_{suffix}")
    with allure.step("DELETE /api/marketing/contentitems?ids=...&ids=..."):
        content_item_ops.delete(i1["id"], i2["id"])


# ── Content Places (Placeholders) ──


@pytest.mark.restapi
@allure.feature("Marketing / Content Places (REST API)")
@allure.title("Create content place")
def test_place_create(make_content_place):
    with allure.step("POST /api/marketing/contentplaces"):
        place = make_content_place()
    assert place["id"]


@pytest.mark.restapi
@allure.feature("Marketing / Content Places (REST API)")
@allure.title("Get content place by id")
def test_place_get(make_content_place, content_place_ops: ContentPlaceOperations):
    place = make_content_place()
    with allure.step(f"GET /api/marketing/contentplaces/{place['id']}"):
        reloaded = content_place_ops.get_by_id(place["id"])
    assert reloaded["id"] == place["id"]


@pytest.mark.restapi
@allure.feature("Marketing / Content Places (REST API)")
@allure.title("Update content place")
def test_place_update(make_content_place, content_place_ops: ContentPlaceOperations):
    place = make_content_place()
    new_name = f"{place['name']}_UPD"
    with allure.step("PUT /api/marketing/contentplaces"):
        content_place_ops.update(place, name=new_name)
    reloaded = content_place_ops.get_by_id(place["id"])
    assert reloaded["name"] == new_name


@pytest.mark.restapi
@allure.feature("Marketing / Content Places (REST API)")
@allure.title("Search content places")
def test_place_search(make_content_place, content_place_ops: ContentPlaceOperations):
    place = make_content_place()
    with allure.step("POST /api/marketing/contentplaces/search"):
        result = content_place_ops.search()
    assert result is not None


@pytest.mark.restapi
@allure.feature("Marketing / Content Places (REST API)")
@allure.title("Delete content place")
def test_place_delete(content_place_ops: ContentPlaceOperations):
    place = content_place_ops.create(name=f"QADelPlace_{uuid.uuid4().hex[:8]}")
    with allure.step(f"DELETE /api/marketing/contentplaces?ids={place['id']}"):
        content_place_ops.delete(place["id"])


@pytest.mark.restapi
@allure.feature("Marketing / Content Places (REST API)")
@allure.title("Delete content places in bulk")
def test_place_delete_bulk(content_place_ops: ContentPlaceOperations):
    suffix = uuid.uuid4().hex[:6]
    p1 = content_place_ops.create(name=f"QABulkPlace1_{suffix}")
    p2 = content_place_ops.create(name=f"QABulkPlace2_{suffix}")
    with allure.step("DELETE /api/marketing/contentplaces?ids=...&ids=..."):
        content_place_ops.delete(p1["id"], p2["id"])


# ── Content Publications ──


@pytest.mark.restapi
@allure.feature("Marketing / Content Publications (REST API)")
@allure.title("Create content publication")
def test_pub_create(make_content_publication):
    with allure.step("POST /api/marketing/contentpublications"):
        pub = make_content_publication()
    assert pub["id"]


@pytest.mark.restapi
@allure.feature("Marketing / Content Publications (REST API)")
@allure.title("Get new publication template")
def test_pub_get_new(content_pub_ops: ContentPublicationOperations):
    with allure.step("GET /api/marketing/contentpublications/new"):
        template = content_pub_ops.get_new()
    assert template is not None


@pytest.mark.restapi
@allure.feature("Marketing / Content Publications (REST API)")
@allure.title("Get content publication by id")
def test_pub_get(make_content_publication, content_pub_ops: ContentPublicationOperations):
    pub = make_content_publication()
    with allure.step(f"GET /api/marketing/contentpublications/{pub['id']}"):
        reloaded = content_pub_ops.get_by_id(pub["id"])
    assert reloaded["id"] == pub["id"]


@pytest.mark.restapi
@allure.feature("Marketing / Content Publications (REST API)")
@allure.title("Update content publication")
def test_pub_update(make_content_publication, content_pub_ops: ContentPublicationOperations):
    pub = make_content_publication()
    new_name = f"{pub['name']}_UPD"
    with allure.step("PUT /api/marketing/contentpublications"):
        content_pub_ops.update(pub, name=new_name)
    reloaded = content_pub_ops.get_by_id(pub["id"])
    assert reloaded["name"] == new_name


@pytest.mark.restapi
@allure.feature("Marketing / Content Publications (REST API)")
@allure.title("Search content publications")
def test_pub_search(make_content_publication, content_pub_ops: ContentPublicationOperations):
    pub = make_content_publication()
    with allure.step("POST /api/marketing/contentpublications/search"):
        result = content_pub_ops.search()
    assert result is not None


@pytest.mark.restapi
@allure.feature("Marketing / Content Publications (REST API)")
@allure.title("Delete content publication")
def test_pub_delete(content_pub_ops: ContentPublicationOperations):
    pub = content_pub_ops.create(name=f"QADelPub_{uuid.uuid4().hex[:8]}")
    with allure.step(f"DELETE /api/marketing/contentpublications?ids={pub['id']}"):
        content_pub_ops.delete(pub["id"])


@pytest.mark.restapi
@allure.feature("Marketing / Content Publications (REST API)")
@allure.title("Delete content publications in bulk")
def test_pub_delete_bulk(content_pub_ops: ContentPublicationOperations):
    suffix = uuid.uuid4().hex[:6]
    p1 = content_pub_ops.create(name=f"QABulkPub1_{suffix}")
    p2 = content_pub_ops.create(name=f"QABulkPub2_{suffix}")
    with allure.step("DELETE /api/marketing/contentpublications?ids=...&ids=..."):
        content_pub_ops.delete(p1["id"], p2["id"])
