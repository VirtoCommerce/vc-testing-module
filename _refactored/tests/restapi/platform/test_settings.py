"""Platform settings — migrated from Katalon `API Coverage/ModulePlatform/Settings*`."""

import allure
import pytest

from restapi.operations import SettingsOperations


@pytest.mark.restapi
@allure.feature("Platform / Settings (REST API)")
@allure.title("Get all settings")
def test_settings_get_all(settings_ops: SettingsOperations) -> None:
    with allure.step("GET /api/platform/settings"):
        settings = settings_ops.get_all()

    with allure.step("Verify non-empty and contains known setting"):
        assert isinstance(settings, list)
        assert len(settings) > 0
        names = [s.get("name", "") for s in settings]
        assert any("AccountTypes" in n for n in names), f"Expected AccountTypes setting, got: {names[:5]}..."


@pytest.mark.restapi
@allure.feature("Platform / Settings (REST API)")
@allure.title("Get setting by name")
def test_settings_get_by_name(settings_ops: SettingsOperations) -> None:
    setting_name = "VirtoCommerce.Search.IndexingJobs.Enable"

    with allure.step(f"GET /api/platform/settings/{setting_name}"):
        setting = settings_ops.get_by_name(setting_name)

    with allure.step("Verify setting fields"):
        assert setting["name"] == setting_name


@pytest.mark.restapi
@allure.feature("Platform / Settings (REST API)")
@allure.title("Get settings by module id")
def test_settings_get_by_module_id(settings_ops: SettingsOperations) -> None:
    module_id = "VirtoCommerce.Catalog"

    with allure.step(f"GET /api/platform/settings/modules/{module_id}"):
        settings = settings_ops.get_by_module_id(module_id)

    with allure.step("Verify module settings returned"):
        assert isinstance(settings, list)
        assert len(settings) > 0
        assert all(s.get("moduleId") == module_id for s in settings if s.get("moduleId"))


@pytest.mark.restapi
@allure.feature("Platform / Settings (REST API)")
@allure.title("Get UI customization settings")
def test_settings_get_ui_customization(settings_ops: SettingsOperations) -> None:
    with allure.step("GET /api/platform/settings/ui/customization"):
        setting = settings_ops.get_ui_customization()

    with allure.step("Verify UI customization setting"):
        assert setting is not None


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Platform / Settings (REST API)")
@allure.title("Update boolean setting")
def test_settings_update_boolean(settings_ops: SettingsOperations) -> None:
    setting_name = "VirtoCommerce.Search.IndexingJobs.Enable"

    with allure.step("Read current value"):
        original = settings_ops.get_by_name(setting_name)
        original_value = original.get("value")

    new_value = not bool(original_value) if isinstance(original_value, bool) else False

    try:
        with allure.step(f"POST /api/platform/settings — {setting_name}={new_value}"):
            settings_ops.update([{**original, "value": new_value}])

        with allure.step("Verify value changed"):
            updated = settings_ops.get_by_name(setting_name)
            assert str(updated.get("value")).lower() == str(new_value).lower()
    finally:
        with allure.step("Restore original value"):
            settings_ops.update([{**original, "value": original_value}])


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Platform / Settings (REST API)")
@allure.title("Update blacklist setting — add file extension")
def test_settings_update_blacklist(settings_ops: SettingsOperations) -> None:
    setting_name = "VirtoCommerce.Platform.Security.FileExtensionsBlackList"

    with allure.step("Read current blacklist"):
        original = settings_ops.get_by_name(setting_name)
        original_allowed = original.get("allowedValues", []) or []

    test_ext = ".qatest"

    try:
        with allure.step(f"POST /api/platform/settings — append {test_ext}"):
            new_allowed = original_allowed + [test_ext]
            settings_ops.update([{**original, "allowedValues": new_allowed}])

        with allure.step("Verify extension added"):
            updated = settings_ops.get_by_name(setting_name)
            updated_allowed = updated.get("allowedValues", []) or []
            assert test_ext in updated_allowed
    finally:
        with allure.step("Restore original blacklist"):
            settings_ops.update([{**original, "allowedValues": original_allowed}])
