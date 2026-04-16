"""Push notifications — migrated from Katalon `API Coverage/ModulePlatform/PushNotifications*`."""

import allure
import pytest

from restapi.operations import NotificationsOperations


@pytest.mark.restapi
@allure.feature("Platform / Notifications (REST API)")
@allure.title("Search push notifications")
def test_push_notifications_search(notifications_ops: NotificationsOperations):
    with allure.step("GET /api/platform/pushnotifications"):
        result = notifications_ops.search()

    with allure.step("Verify response structure"):
        assert result is not None
        assert "notifyEvents" in result or "totalCount" in result


@pytest.mark.restapi
@allure.feature("Platform / Notifications (REST API)")
@allure.title("Mark all notifications as read")
def test_push_notifications_mark_as_read(notifications_ops: NotificationsOperations):
    with allure.step("POST /api/platform/pushnotifications/markallasread"):
        notifications_ops.mark_all_as_read()

    with allure.step("Verify new count is zero"):
        result = notifications_ops.search()
        new_count = result.get("newCount", 0)
        assert new_count == 0, f"Expected newCount=0 after mark-all-as-read, got {new_count}"
