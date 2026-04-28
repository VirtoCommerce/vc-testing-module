from pydantic import BaseModel


class InputUpdatePersonalDataType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_personal_data_type import InputPersonalDataType

        self.personalData: InputPersonalDataType
