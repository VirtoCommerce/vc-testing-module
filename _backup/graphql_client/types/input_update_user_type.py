from pydantic import BaseModel


class InputUpdateUserType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_update_application_user_type import InputUpdateApplicationUserType

        self.applicationUser: InputUpdateApplicationUserType
