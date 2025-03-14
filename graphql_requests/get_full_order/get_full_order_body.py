from gql import gql

GET_FULL_ORDER = gql(
    """
    query GetFullOrder($id: String!) {
        order(id: $id) {
            id
            number
            status
            createdDate
            customerId
            customerName
            items {
                id
                sku
                productId
                name
                quantity
                price {
                    amount
                    formattedAmount
                }
                extendedPrice {
                    amount
                    formattedAmount
                }
            }
            total {
                amount
                formattedAmount
            }
            subTotal {
                amount
                formattedAmount
            }
            shippingTotal {
                amount
                formattedAmount
            }
            taxTotal {
                amount
                formattedAmount
            }
            paymentTotal {
                amount
                formattedAmount
            }
            addresses {
                firstName
                lastName
                line1
                line2
                city
                countryCode
                countryName
                postalCode          
                addressType
            }
        }
    }
    """
)