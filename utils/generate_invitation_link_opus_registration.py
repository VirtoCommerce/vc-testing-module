import uuid
from typing import Any, Dict

import requests


def generate_invitation_link_opus_registration(
    config: Dict[str, Any],
    first_name: str = "Test",
    last_name: str = "User",
    email: str = None,
    phone: str = "+1-555-0100",
    zip_code: str = "12345",
    job_title: str = "Manager",
    organization_name: str = "Test Organization",
) -> str:
    """
    Generate an invitation link by calling the opus-registration API.
    
    This utility calls the /api/v1/opus-registration endpoint which:
    1. Creates a new organization registration
    2. Returns a redirect_url (invitation link) for the user to complete registration
    
    Args:
        config: Configuration dictionary with backend_base_url and api_key
        first_name: User's first name
        last_name: User's last name
        email: User's email (auto-generated if not provided)
        phone: User's phone number
        zip_code: User's zip code
        job_title: User's job title
        organization_name: Organization name
    
    Returns:
        Invitation link (redirect_url) from the registration API
        
    Example:
        link = generate_invitation_link_opus_registration(
            config=config,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            organization_name="ACME Corp"
        )
        
        # Use the link in your test
        page.goto(link)
    """
    # Auto-generate email if not provided
    if email is None:
        email = f"test-{uuid.uuid4()}@example.com"
    
    # Prepare the API endpoint URL
    url = f"{config['backend_base_url']}/api/v1/opus-registration"
    
    # Prepare the request body
    body = {
        "outer_id": str(uuid.uuid4()),
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "zip_code": zip_code,
        "job_title": job_title,
        "organization_name": organization_name,
        "organization_outer_id": str(uuid.uuid4()),
        "created_way": "",
        "sub_source": "",
        "accept_terms_and_conditions": True
    }
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json-patch+json",
        "api_key": config["api_key"]
    }
    
    # Send the request
    response = requests.post(url, json=body, headers=headers)
    
    # Validate response
    response.raise_for_status()
    
    # Extract and return the invitation link
    response_data = response.json()
    
    if "redirect_url" not in response_data:
        raise ValueError("Response does not contain 'redirect_url' field")
    
    invitation_link = response_data["redirect_url"].strip('"')
    
    return invitation_link

