from typing import Dict, Union

class OrdersTestData:
    """Test data for order-related tests."""

    # Order identification
    TEST_ORDER_ID: str = "c94f55a7-37c2-486c-b26e-5f0f417b44ac"

    # Order status
    EXPECTED_STATUS: str = "Processing"

    # Test address data
    TEST_ADDRESS: Dict[str, Union[str, int]] = {
        "addressType": 2,
        "city": "Test City",
        "countryCode": "USA",
        "countryName": "United States of America",        
        "firstName": "Elena",
        "id": "c89875fd-cdbf-4e88-a587-61ec2de453ef",
        "lastName": "Mut",
        "line1": "Test st., 123",      
        "name": "USA, Florida, Test City, Test st., 123",
        "organization": "",    
        "postalCode": "12345",
        "regionId": "FL",
        "regionName": "Florida"
    }

    # Test item data
    TEST_ITEM: Dict[str, Union[str, int, Dict[str, str]]] = {
        "sku": "TEST-SKU-001",
        "name": "Test Product",
        "quantity": 1,
        "price": {
            "amount": "99.99",
            "formattedAmount": "$99.99"
        }
    } 