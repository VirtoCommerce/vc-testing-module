from gql.operations.base_operations import BaseOperations, gql
from gql.types.contact import Contact
from gql.types.identity_result import IdentityResult
from gql.types.member_address import MemberAddress
from gql.types.registration import Registration


class ContactOperations(BaseOperations):
    def get_contact_addresses(self, contact_id: str) -> list[MemberAddress]:
        # fmt: off
        query = gql("""
            query GetContactAddresses($id: String!) {
              contact(id: $id) {
                addresses {
                  items {
                    ...MemberAddressFragment
                  }
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={"id": contact_id},
        )
        items = result["data"]["contact"]["addresses"]["items"] or []
        return [MemberAddress.model_validate(a) for a in items]

    def add_address_to_favorites(self, address_id: str) -> bool:
        # fmt: off
        mutation = gql("""
            mutation AddAddressToFavorites($command: AddAddressToFavoritesCommandType!) {
              addAddressToFavorites(command: $command)
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"addressId": address_id}},
        )
        return result["data"]["addAddressToFavorites"]

    def remove_address_from_favorites(self, address_id: str) -> bool:
        # fmt: off
        mutation = gql("""
            mutation RemoveAddressFromFavorites($command: RemoveAddressFromFavoritesCommandType!) {
              removeAddressFromFavorites(command: $command)
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"addressId": address_id}},
        )
        return result["data"]["removeAddressFromFavorites"]

    def update_member_addresses(self, member_id: str, addresses: list[MemberAddress]) -> list[MemberAddress]:
        # fmt: off
        mutation = gql("""
            mutation UpdateMemberAddresses($command: InputUpdateMemberAddressType!) {
              updateMemberAddresses(command: $command) {
                addresses {
                  items {
                    ...MemberAddressFragment
                  }
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "memberId": member_id,
                    "addresses": [
                        a.model_dump(
                            by_alias=True,
                            exclude={"is_default", "is_favorite"},
                            exclude_none=True,
                        )
                        for a in addresses
                    ],
                }
            },
        )
        data = result["data"]["updateMemberAddresses"]["addresses"]["items"]
        return [MemberAddress.model_validate(a) for a in data]

    def delete_member_addresses(self, member_id: str, addresses: list[MemberAddress]) -> list[MemberAddress]:
        # fmt: off
        mutation = gql("""
            mutation DeleteMemberAddresses($command: InputDeleteMemberAddressType!) {
              deleteMemberAddresses(command: $command) {
                addresses {
                  items {
                    ...MemberAddressFragment
                  }
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "memberId": member_id,
                    "addresses": [
                        a.model_dump(
                            by_alias=True,
                            exclude={"is_default", "is_favorite"},
                            exclude_none=True,
                        )
                        for a in addresses
                    ],
                }
            },
        )
        data = result["data"]["deleteMemberAddresses"]["addresses"]["items"]
        return [MemberAddress.model_validate(a) for a in data]

    def change_organization_contact_role(
        self,
        member_id: str,
        role_ids: list[str],
    ) -> IdentityResult:
        # fmt: off
        mutation = gql("""
            mutation ChangeOrganizationContactRole($command: InputChangeOrganizationContactRoleType!) {
              changeOrganizationContactRole(command: $command) {
                ...CustomIdentityResultFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"memberId": member_id, "roleIds": role_ids}},
        )
        return IdentityResult.model_validate(result["data"]["changeOrganizationContactRole"])

    def get_contact(self, contact_id: str) -> Contact | None:
        # fmt: off
        query = gql("""
            query GetContact($id: String!) {
              contact(id: $id) {
                ...ContactFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={"id": contact_id},
        )
        data = result["data"]["contact"]
        return Contact.model_validate(data) if data else None

    def lock_organization_contact(self, member_id: str) -> Contact:
        # fmt: off
        mutation = gql("""
            mutation LockOrganizationContact($command: InputLockUnlockOrganizationContactType!) {
              lockOrganizationContact(command: $command) {
                ...ContactFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"memberId": member_id}},
        )
        return Contact.model_validate(result["data"]["lockOrganizationContact"])

    def unlock_organization_contact(self, member_id: str) -> Contact:
        # fmt: off
        mutation = gql("""
            mutation UnlockOrganizationContact($command: InputLockUnlockOrganizationContactType!) {
              unlockOrganizationContact(command: $command) {
                ...ContactFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"memberId": member_id}},
        )
        return Contact.model_validate(result["data"]["unlockOrganizationContact"])

    def request_registration(
        self,
        store_id: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        language_code: str | None = None,
        organization_name: str | None = None,
    ) -> Registration:
        # fmt: off
        mutation = gql("""
            mutation RequestRegistration($command: InputRequestRegistrationType!) {
              requestRegistration(command: $command) {
                contact {
                  id
                  firstName
                  lastName
                  status
                }
                organization {
                  id
                  name
                  status
                  ownerId
                }
                account {
                  id
                  username
                  email
                  status
                }
                result {
                  succeeded
                  requireEmailVerification
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "storeId": store_id,
                    **({"languageCode": language_code} if language_code else {}),
                    "contact": {"firstName": first_name, "lastName": last_name},
                    **({"organization": {"name": organization_name}} if organization_name else {}),
                    "account": {"username": email, "email": email, "password": password},
                }
            },
        )
        return Registration.model_validate(result["data"]["requestRegistration"])

    def delete_contact(self, contact_id: str) -> bool:
        # fmt: off
        mutation = gql("""
            mutation DeleteContact($command: InputDeleteContactType!) {
              deleteContact(command: $command)
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"contactId": contact_id}},
        )
        return result["data"]["deleteContact"]

    def get_current_customer_addresses(
        self,
        after: str | None = None,
        first: int | None = None,
        country_codes: list[str] | None = None,
        region_ids: list[str] | None = None,
        cities: list[str] | None = None,
        keyword: str | None = None,
        sort: str | None = None,
    ) -> tuple[int, list[MemberAddress]]:
        # fmt: off
        query = gql("""
            query GetCurrentCustomerAddresses(
                $after: String,
                $first: Int,
                $countryCodes: [String],
                $regionIds: [String],
                $cities: [String],
                $keyword: String,
                $sort: String,
            ) {
              currentCustomerAddresses(
                after: $after,
                first: $first,
                countryCodes: $countryCodes,
                regionIds: $regionIds,
                cities: $cities,
                keyword: $keyword,
                sort: $sort,
              ) {
                totalCount
                items {
                  ...MemberAddressFragment
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "after": after,
                "first": first,
                "countryCodes": country_codes,
                "regionIds": region_ids,
                "cities": cities,
                "keyword": keyword,
                "sort": sort,
            },
        )
        data = result["data"]["currentCustomerAddresses"]
        total_count: int = data.get("totalCount") or 0
        items = [MemberAddress.model_validate(a) for a in (data.get("items") or [])]
        return total_count, items

    def get_current_organization_addresses(
        self,
        after: str | None = None,
        first: int | None = None,
        country_codes: list[str] | None = None,
        region_ids: list[str] | None = None,
        cities: list[str] | None = None,
        keyword: str | None = None,
        sort: str | None = None,
    ) -> tuple[int, list[MemberAddress]]:
        # fmt: off
        query = gql("""
            query GetCurrentOrganizationAddresses(
                $after: String,
                $first: Int,
                $countryCodes: [String],
                $regionIds: [String],
                $cities: [String],
                $keyword: String,
                $sort: String,
            ) {
              currentOrganizationAddresses(
                after: $after,
                first: $first,
                countryCodes: $countryCodes,
                regionIds: $regionIds,
                cities: $cities,
                keyword: $keyword,
                sort: $sort,
              ) {
                totalCount
                items {
                  ...MemberAddressFragment
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "after": after,
                "first": first,
                "countryCodes": country_codes,
                "regionIds": region_ids,
                "cities": cities,
                "keyword": keyword,
                "sort": sort,
            },
        )
        data = result["data"]["currentOrganizationAddresses"]
        total_count: int = data.get("totalCount") or 0
        items = [MemberAddress.model_validate(a) for a in (data.get("items") or [])]
        return total_count, items

    def get_contact_lock_status(self, contact_id: str, organization_id: str) -> bool:
        # fmt: off
        query = gql("""
            query GetContactLockStatus($id: String!, $organizationId: String!) {
              contact(id: $id) {
                isLockedInOrganization(organizationId: $organizationId)
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={"id": contact_id, "organizationId": organization_id},
        )
        data = result["data"]["contact"]
        return bool(data["isLockedInOrganization"]) if data else False

    def get_contact_roles_in_organization(self, contact_id: str, organization_id: str) -> list:
        # fmt: off
        query = gql("""
            query GetContactRolesInOrganization($id: String!, $organizationId: String!) {
              contact(id: $id) {
                rolesInOrganization(organizationId: $organizationId) {
                  id
                  name
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={"id": contact_id, "organizationId": organization_id},
        )
        data = result["data"]["contact"]
        if not data:
            return []
        from gql.types.role import Role
        return [Role.model_validate(r) for r in (data.get("rolesInOrganization") or [])]

    def get_organization_contacts(
        self,
        organization_id: str,
        search_phrase: str | None = None,
        sort: str | None = None,
        first: int | None = None,
        after: str | None = None,
    ) -> list[Contact]:
        # fmt: off
        query = gql("""
            query GetOrganizationContacts(
                $organizationId: String!,
                $searchPhrase: String,
                $sort: String,
                $first: Int,
                $after: String,
            ) {
              organization(id: $organizationId) {
                contacts(
                  searchPhrase: $searchPhrase,
                  sort: $sort,
                  first: $first,
                  after: $after,
                ) {
                  items {
                    ...ContactFragment
                  }
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "organizationId": organization_id,
                "searchPhrase": search_phrase,
                "sort": sort,
                "first": first,
                "after": after,
            },
        )
        items = result["data"]["organization"]["contacts"]["items"] or []
        return [Contact.model_validate(item) for item in items]
