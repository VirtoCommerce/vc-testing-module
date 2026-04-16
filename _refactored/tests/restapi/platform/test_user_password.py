"""User password operations — migrated from Katalon `API Coverage/ModulePlatform/UserPassword*`."""

import uuid

import allure
import pytest
from pydantic import SecretStr

from core.auth import AuthProvider
from core.global_settings import GlobalSettings
from restapi.operations import UserOperations


@pytest.mark.restapi
@allure.feature("Platform / User Password (REST API)")
@allure.title("Reset password — admin path")
def test_user_password_reset_admin(make_user, user_ops: UserOperations, global_settings: GlobalSettings):
    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])
    new_password = f"NewPwd!{uuid.uuid4().hex[:8]}"

    with allure.step(f"POST /api/platform/security/users/{full_user['id']}/resetpassword"):
        result = user_ops.reset_password(full_user["id"], new_password)

    with allure.step("Verify succeeded"):
        assert result.get("succeeded") is True

    with allure.step("Verify new password works"):
        provider = AuthProvider(global_settings)
        provider.sign_in(user["user_name"], SecretStr(new_password))
        assert provider.is_authenticated
        provider.sign_out()


@pytest.mark.restapi
@allure.feature("Platform / User Password (REST API)")
@allure.title("Change password — current user path")
def test_user_password_change(make_user, user_ops: UserOperations, global_settings: GlobalSettings):
    user = make_user()
    new_password = f"Changed!{uuid.uuid4().hex[:8]}"

    with allure.step(f"POST /api/platform/security/users/{user['user_name']}/changepassword"):
        result = user_ops.change_password(user["user_name"], user["password"], new_password)

    with allure.step("Verify succeeded"):
        assert result.get("succeeded") is True

    with allure.step("Verify new password works"):
        provider = AuthProvider(global_settings)
        provider.sign_in(user["user_name"], SecretStr(new_password))
        assert provider.is_authenticated
        provider.sign_out()


@pytest.mark.restapi
@allure.feature("Platform / User Password (REST API)")
@allure.title("Validate password — weak password rejected")
def test_user_password_validate_weak(user_ops: UserOperations):
    with allure.step("POST /api/platform/security/validatepassword — '123'"):
        result = user_ops.validate_password("123")

    with allure.step("Verify validation failed"):
        assert result.get("succeeded") is False or result.get("errors")


@pytest.mark.restapi
@allure.feature("Platform / User Password (REST API)")
@allure.title("Validate password — strong password accepted")
def test_user_password_validate_strong(user_ops: UserOperations):
    strong = f"StrongPwd!{uuid.uuid4().hex[:8]}"

    with allure.step(f"POST /api/platform/security/validatepassword — '{strong}'"):
        result = user_ops.validate_password(strong)

    with allure.step("Verify validation passed"):
        assert result.get("succeeded") is True


@pytest.mark.restapi
@allure.feature("Platform / User Password (REST API)")
@allure.title("Send verification email")
def test_user_send_verification_email(make_user, user_ops: UserOperations):
    user = make_user()
    full_user = user_ops.get_by_name(user["user_name"])

    with allure.step(f"POST /api/platform/security/users/{full_user['id']}/sendverificationemail"):
        user_ops.send_verification_email(full_user["id"])
    # No assertion on response body — endpoint returns 204/200 with no content.
    # The test verifies the endpoint doesn't error out.
