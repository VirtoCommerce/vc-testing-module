import os
import re
from typing import Any
from urllib.parse import urlparse, parse_qs, unquote

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from fixtures.webapi_client import WebAPISession
from graphql_client.mutations.reset_password import SendPasswordResetEmailMutation
from graphql_client.mutations.reset_password_by_token import ResetPasswordByTokenMutation
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Reset password (GraphQL)")
def test_reset_password(
    config: dict[str, Any],
    dataset: dict[str, Any],   
    graphql_client: GraphQLClient,
    webapi_client: WebAPISession,
    auth: Auth):

    print(f"{os.linesep}Running test to reset password...", end=" ")

    send_password_reset_email_mutation = SendPasswordResetEmailMutation(graphql_client)
    send_password_reset_email_result = send_password_reset_email_mutation.execute(
        payload={
            "storeId": config["store_id"],
            "cultureName": dataset["languages"][0]["defaultValue"],
            "loginOrEmail": dataset["users"][2]["email"],
            "urlSuffix": "/reset-password",
        }
    )

    assert send_password_reset_email_result is True

    auth.authenticate(config["admin_username"], config["admin_password"])

    search_reset_password_email_notification = webapi_client.post(
        "/api/notifications/journal",
        data={
            "notificationType": "ResetPasswordEmailNotification",
            "keyword": dataset["users"][2]["email"],
            "sort": "",
            "skip": 0,
            "take": 20,
            "responseGroup": "Default"
        }
    )

    assert search_reset_password_email_notification["totalCount"] > 0
    assert search_reset_password_email_notification["results"] is not None
    assert len(search_reset_password_email_notification["results"]) > 0
    notification = search_reset_password_email_notification["results"][0]
    
    assert notification["notificationType"] == "ResetPasswordEmailNotification"
    assert notification["to"] == dataset["users"][2]["email"]
    assert notification["subject"] is not None and notification["subject"] == "Reset password link"
    assert notification["body"] is not None
    assert notification["status"] is not None and notification["status"] == "Sent"

    # Extract and set Token from URL
    body_html = notification["body"]
    
    url_match = re.search(r'href="([^"]+)"', body_html)
    if not url_match:
        pytest.fail("Reset password URL not found in the notification body.")
    
    reset_password_url = url_match.group(1)
    
    parsed_url = urlparse(reset_password_url)
    query_params = parse_qs(parsed_url.query)
    
    if "token" not in query_params:
        pytest.fail("Token parameter not found in the reset password URL.")   

    token_encoded = query_params["token"][0]
    
    token = unquote(token_encoded)    
  
    if token.endswith("\\"):
        token = token[:-1]

    #print(f"Extracted Token: {token}")    

    assert token, "Token should not be empty"

    reset_password_mutation = ResetPasswordByTokenMutation(graphql_client)
    reset_password_result = reset_password_mutation.execute(
        variables={
            "token": token,
            "userId": dataset["users"][2]["id"],
            "newPassword": "NewPassword123!"
        }
    )
    
    assert reset_password_result["succeeded"] is True, f"Password reset failed: {reset_password_result['errors'][0]['description']}"

    auth.authenticate(dataset["users"][2]["email"], "NewPassword123!")    

    user_operations = UserOperations(graphql_client)
    user = user_operations.get_me()
    assert user["email"] == dataset["users"][2]["email"], "User email is not correct" 
