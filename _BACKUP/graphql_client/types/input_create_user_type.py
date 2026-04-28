from pydantic import BaseModel


class InputCreateUserType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_create_application_user_type import InputCreateApplicationUserType

        self.applicationUser: InputCreateApplicationUserType
