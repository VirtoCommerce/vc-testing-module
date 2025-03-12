from gql import gql


def get_slug_info(graphql_client, slug, store_id, user_id, culture_name):
    query = gql(
        """
                    query GetSlugInfo($slug: String, $storeId: String, $userId: String, $cultureName: String) {
                      slugInfo(
                        slug: $slug
                        storeId: $storeId
                        userId: $userId
                        cultureName: $cultureName
                      ) {
                        entityInfo {
                          isActive
                          languageCode
                          objectId
                          objectType
                          semanticUrl
                          metaDescription
                          metaKeywords
                          pageTitle                        
                        }
                      }
                    }
                    """
    )

    variables = {
        "storeId": store_id,
        "userId": user_id,
        "cultureName": culture_name,
        "slug": slug,
    }

    result = graphql_client.execute(query, variable_values=variables)

    return result


def get_categories(
    graphql_client,
    storeId,
    userId,
    cultureName,
    currencyCode,
    maxLevel,
    onlyActive,
    productFilter,
):
    query = gql(
        """
        query GetCategory($storeId: String!, $userId: String, $cultureName: String, $currencyCode: String, $maxLevel: Int, $onlyActive: Boolean, $productFilter: String) {
                  category(
                    storeId: $storeId
                    userId: $userId
                    cultureName: $cultureName
                    currencyCode: $currencyCode
                    id: \"1dbe91e2-b7c6-4aba-b78f-3c7da9bd9d55\"
                  ) {
                    id
                    name
                    priority
                    slug
                    seoInfo {
                      pageTitle
                      metaKeywords
                      metaDescription
                    }
                    breadcrumbs {
                      title
                      seoPath
                    }
                    parent {
                      id
                      name
                      slug
                    }
                    images {
                      url
                    }
                    facets
                  }
                  childCategories(
                    storeId: $storeId
                    userId: $userId
                    cultureName: $cultureName
                    currencyCode: $currencyCode
                    maxLevel: $maxLevel
                    onlyActive: $onlyActive
                    productFilter: $productFilter
                    categoryId: \"1dbe91e2-b7c6-4aba-b78f-3c7da9bd9d55\"
                  ) {
                    __typename
                    childCategories {
                      id
                      name
                      level
                      imgSrc
                      priority
                      relevanceScore
                      slug
                      parent {
                        id
                        name
                        slug
                      }
                      seoInfo {
                        pageTitle
                        metaKeywords
                        metaDescription
                      }
                      breadcrumbs {
                        title
                        seoPath
                      }
                      childCategories {
                        id
                        name
                        level
                        imgSrc
                        priority
                        relevanceScore
                        slug
                        parent {
                          id
                          name
                          slug
                        }
                        seoInfo {
                          pageTitle
                          metaKeywords
                          metaDescription
                        }
                        breadcrumbs {
                          title
                          seoPath
                        }
                        childCategories {
                          id
                          name
                          level
                          imgSrc
                          priority
                          relevanceScore
                          slug
                          parent {
                            id
                            name
                            slug
                          }
                          seoInfo {
                            pageTitle
                            metaKeywords
                            metaDescription
                          }
                          breadcrumbs {
                            title
                            seoPath
                          }
                        }
                      }
                    }
                  }
                }"""
    )


def get_me(graphql_client, user_id):
    query = gql(
        """query GetMe($userId: String) {
                      me(userId: $userId) {
                        id
                        memberId
                        userName
                        email
                        emailConfirmed
                        photoUrl
                        phoneNumber
                        permissions
                        isAdministrator
                        passwordExpired
                        passwordExpiryInDays
                        forcePasswordChange
                        lockedState
                        contact {
                          id
                          firstName
                          lastName
                          fullName
                          organizationId
                          defaultLanguage
                          currencyCode
                          organizations {
                            items {
                              id
                              outerId
                              name
                            }
                            items {
                              status
                              dynamicProperties {
                                name
                                value
                              }
                              accountsPayableContact {
                                address {
                                  line1
                                  line2
                                  city
                                  countryCode
                                  countryName
                                  regionId
                                  regionName
                                  postalCode
                                }
                                email
                                firstName
                                lastName
                                phone
                                fullName
                              }
                            }
                          }
                          dynamicProperties {
                            name
                            value
                          }
                          securityAccounts {
                            id
                            email
                            roles {
                              id
                              name
                            }
                          }
                          phones
                          selectedShippingLocation
                          favoriteSupplierOuterIds
                        }
                        operator {
                          userName
                          contact {
                            fullName
                          }
                        }
                        temporaryPassword
                        industrySector
                        canBypassTermsAndConditionsSection1
                        canBypassTermsAndConditionsSection2
                      }
                    }"""
    )
    variables = {
        "userId": user_id,
    }

    result = graphql_client.execute(query, variable_values=variables)

    return result


def add_item(graphql_client, user_id, product_id, quantity):
    query = gql(
        """
        mutation AddItem($command: InputAddItemType!) {
        addItem(command: $command) {
            ...shortCart
            __typename
          }
        }
        
        fragment cartId on CartType {
          id
          __typename
        }
        
        fragment shortLineItem on LineItemType {
          id
          sku
          quantity
          productId
          extendedPrice {
            amount
            formattedAmount
            __typename
          }
          __typename
        }
        
        fragment validationError on ValidationErrorType {
          errorCode
          errorMessage
          errorParameters {
            key
            value
            __typename
          }
          objectId
          objectType
          __typename
        }
        
        fragment shortCart on CartType {
          ...cartId
          itemsQuantity
          items {
            ...shortLineItem
            __typename
          }
          validationErrors(ruleSet: "*") {
            ...validationError
            __typename
          }
          warnings {
            ...validationError
            __typename
          }
          __typename
        }
    """
    )

    variables = {
        "command": {
            "storeId": "",
            "cultureName": "en-US",
            "currencyCode": "USD",
            "userId": user_id,
            "productId": product_id,
            "quantity": quantity,
        }
    }

    result = graphql_client.execute(query, variable_values=variables)

    return result


def get_full_cart(graphql_client, store_id, user_id, currency_code, culture_name):
    query = gql(
        """
        query GetFullCart($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String) {
          cart(
            storeId: $storeId
            userId: $userId
            currencyCode: $currencyCode
            cultureName: $cultureName
          ) {
            ...fullCart
            __typename
          }
        }
        # Including only essential fragments for brevity - the full query includes all fragments
        fragment cartId on CartType {
          id
          __typename
        }
        fragment fullCart on CartType {
          ...cartId
          itemsQuantity
          items {
            id
            sku
            quantity
            productId
          }
          __typename
        }
    """
    )

    variables = {
        "storeId": store_id,
        "userId": user_id,
        "currencyCode": currency_code,
        "cultureName": culture_name,
    }

    result = graphql_client.execute(query, variable_values=variables)
    return result


def clear_cart(graphql_client, store_id, user_id, currency_code, culture_name, cart_id):
    query = gql(
        """
        mutation ClearCart($command: InputClearCartType!, $skipQuery: Boolean!) {
          clearCart(command: $command) {
            ...fullCart @skip(if: $skipQuery)
            __typename
          }
        }
        # Including only essential fragments for brevity
        fragment cartId on CartType {
          id
          __typename
        }
        fragment fullCart on CartType {
          ...cartId
          itemsQuantity
          __typename
        }
    """
    )

    variables = {
        "command": {
            "storeId": store_id,
            "cultureName": culture_name,
            "currencyCode": currency_code,
            "userId": user_id,
            "cartId": cart_id,
        },
        "skipQuery": False,
    }

    result = graphql_client.execute(query, variable_values=variables)
    return result
