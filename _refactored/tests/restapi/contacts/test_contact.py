"""Contact CRUD — migrated from Katalon `API Coverage/Contacts/Contact*` + `_module_Customer/contact*`.

Katalon scripts:
  ContactCreation       → test_contact_create
  ContactCycle          → test_contact_get, test_contact_update, test_contact_delete, test_contact_search
  ContactCycleBulk      → test_contact_create_bulk, test_contact_get_bulk, test_contact_update_bulk, test_contact_delete_bulk
  contactAddAddress     → test_contact_add_address
"""

import uuid

import allure
import pytest

from restapi.constants import ADDRESS_TEMPLATE
from restapi.operations import ContactOperations


@pytest.mark.restapi
@allure.feature("Contacts / Contacts (REST API)")
@allure.title("Create contact")
def test_contact_create(make_contact):
    with allure.step("POST /api/contacts"):
        contact = make_contact()

    with allure.step("Verify response"):
        assert contact["id"]
        assert contact["memberType"] == "Contact"
        assert contact["firstName"].startswith("QAFirst_")


@pytest.mark.restapi
@allure.feature("Contacts / Contacts (REST API)")
@allure.title("Get contact by id")
def test_contact_get(make_contact, contact_ops: ContactOperations):
    contact = make_contact()

    with allure.step(f"GET /api/contacts/{contact['id']}"):
        reloaded = contact_ops.get_by_id(contact["id"])

    with allure.step("Verify fields match"):
        assert reloaded["id"] == contact["id"]
        assert reloaded["firstName"] == contact["firstName"]
        assert reloaded["lastName"] == contact["lastName"]


@pytest.mark.restapi
@allure.feature("Contacts / Contacts (REST API)")
@allure.title("Update contact — change name")
def test_contact_update(make_contact, contact_ops: ContactOperations):
    contact = make_contact()
    new_first = f"Updated_{uuid.uuid4().hex[:6]}"

    with allure.step(f"PUT /api/contacts — firstName={new_first}"):
        contact_ops.update(contact, firstName=new_first)

    with allure.step("Verify update"):
        reloaded = contact_ops.get_by_id(contact["id"])
        assert reloaded["firstName"] == new_first


@pytest.mark.restapi
@allure.feature("Contacts / Contacts (REST API)")
@allure.title("Search contacts")
def test_contact_search(make_contact, contact_ops: ContactOperations):
    contact = make_contact()

    with allure.step("POST /api/contacts/search — objectIds"):
        search = contact_ops.search(objectIds=[contact["id"]])

    with allure.step("Verify contact in results"):
        assert search.get("totalCount", 0) >= 1
        found = next((r for r in search.get("results", []) if r["id"] == contact["id"]), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Contacts / Contacts (REST API)")
@allure.title("Delete contact")
def test_contact_delete(make_contact, contact_ops: ContactOperations):
    contact = make_contact()

    with allure.step(f"DELETE /api/contacts?ids={contact['id']}"):
        contact_ops.delete(contact["id"])

    with allure.step("Verify deleted"):
        search = contact_ops.search(objectIds=[contact["id"]])
        assert search.get("totalCount", 0) == 0


@pytest.mark.restapi
@allure.feature("Contacts / Contacts (REST API)")
@allure.title("Create contacts in bulk")
def test_contact_create_bulk(contact_ops: ContactOperations):
    suffix = uuid.uuid4().hex[:6]
    contacts = [
        {
            "memberType": "Contact",
            "firstName": f"QABulk1_{suffix}",
            "lastName": "Bulk",
            "name": f"QABulk1_{suffix} Bulk",
        },
        {
            "memberType": "Contact",
            "firstName": f"QABulk2_{suffix}",
            "lastName": "Bulk",
            "name": f"QABulk2_{suffix} Bulk",
        },
    ]

    with allure.step("POST /api/contacts/bulk"):
        result = contact_ops.create_bulk(contacts)

    with allure.step("Verify bulk create"):
        assert isinstance(result, list), f"Expected list, got {type(result)}"
        created_ids = [c["id"] for c in result]
        assert len(created_ids) == 2

    with allure.step("Cleanup"):
        for cid in created_ids:
            try:
                contact_ops.delete(cid)
            except Exception:
                pass


@pytest.mark.restapi
@allure.feature("Contacts / Contacts (REST API)")
@allure.title("Get contacts by ids (bulk)")
def test_contact_get_bulk(make_contact, contact_ops: ContactOperations):
    c1 = make_contact()
    c2 = make_contact()

    with allure.step(f"GET /api/contacts?ids={c1['id']}&ids={c2['id']}"):
        result = contact_ops.get_by_ids([c1["id"], c2["id"]])

    with allure.step("Verify both returned"):
        assert isinstance(result, list)
        ids = [c["id"] for c in result]
        assert c1["id"] in ids
        assert c2["id"] in ids


@pytest.mark.restapi
@allure.feature("Contacts / Contacts (REST API)")
@allure.title("Update contacts in bulk")
def test_contact_update_bulk(make_contact, contact_ops: ContactOperations):
    c1 = make_contact()
    c2 = make_contact()
    suffix = uuid.uuid4().hex[:4]

    with allure.step("PUT /api/contacts/bulk"):
        contact_ops.update_bulk(
            [
                {**c1, "firstName": f"BulkUpd1_{suffix}"},
                {**c2, "firstName": f"BulkUpd2_{suffix}"},
            ]
        )

    with allure.step("Verify updates"):
        r1 = contact_ops.get_by_id(c1["id"])
        r2 = contact_ops.get_by_id(c2["id"])
        assert r1["firstName"] == f"BulkUpd1_{suffix}"
        assert r2["firstName"] == f"BulkUpd2_{suffix}"


@pytest.mark.restapi
@allure.feature("Contacts / Contacts (REST API)")
@allure.title("Delete contacts in bulk")
def test_contact_delete_bulk(contact_ops: ContactOperations):
    suffix = uuid.uuid4().hex[:6]
    c1 = contact_ops.create(first_name=f"QADel1_{suffix}", last_name="Del")
    c2 = contact_ops.create(first_name=f"QADel2_{suffix}", last_name="Del")

    with allure.step(f"DELETE /api/contacts?ids={c1['id']}&ids={c2['id']}"):
        contact_ops.delete(c1["id"], c2["id"])

    with allure.step("Verify deleted"):
        search = contact_ops.search(objectIds=[c1["id"], c2["id"]])
        assert search.get("totalCount", 0) == 0


@pytest.mark.restapi
@allure.feature("Contacts / Contacts (REST API)")
@allure.title("Add address to contact")
def test_contact_add_address(make_contact, contact_ops: ContactOperations):
    contact = make_contact()

    with allure.step("PUT /api/addresses?memberId=..."):
        contact_ops.update_addresses(contact["id"], [ADDRESS_TEMPLATE])

    with allure.step("Verify address added"):
        reloaded = contact_ops.get_by_id(contact["id"])
        addresses = reloaded.get("addresses", [])
        assert len(addresses) >= 1
