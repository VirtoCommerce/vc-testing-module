"""Vendor search — migrated from Katalon `API Coverage/Contacts/VendorGetSearch`.

Katalon scripts:
  VendorGetSearch → test_vendor_search
"""

import allure
import pytest

from restapi.operations import VendorOperations


@pytest.mark.restapi
@allure.feature("Contacts / Vendors (REST API)")
@allure.title("Search vendors")
def test_vendor_search(vendor_ops: VendorOperations):
    with allure.step("POST /api/vendors/search"):
        search = vendor_ops.search()

    with allure.step("Verify response"):
        assert "totalCount" in search, "Response missing 'totalCount'"
        assert search["totalCount"] >= 0
        assert "results" in search, "Response missing 'results'"
