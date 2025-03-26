from typing import Dict, Union

class OrdersTestData:
    """Test data for order-related tests."""

    # Order identification
    TEST_ORDER_ID: str = "4580ede7-a35c-4a7b-9a52-c0d060db761d"

    # Order status
    EXPECTED_STATUS: str = "Processing"

    # Test address data
    TEST_ADDRESS: Dict[str, Union[str, int]] = {
        "addressType": 2,
        "city": "Test City",
        "countryCode": "USA",
        "countryName": "United States of America",        
        "firstName": "Admin",
        "id": "c89875fd-cdbf-4e88-a587-61ec2de453ef",
        "lastName": "b2b",
        "line1": "Test st., 123",      
        "name": "USA, Florida, Test City, Test st., 123",
        "organization": "",    
        "postalCode": "12345",
        "regionId": "FL",
        "regionName": "Florida"
    }

    # Test item data
    TEST_ITEM: Dict[str, Union[str, int, Dict[str, str]]] = {
        "sku": "555929573",
        "name": "Epson WorkForce WF-2760 All-in-One (PRICE 0 reorder )",
        "quantity": 1,
        "price": {
            "amount": "64.00",
            "formattedAmount": "$64.00"
        }
    } 