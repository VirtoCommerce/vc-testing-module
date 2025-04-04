def normalize_graphql_payload(payload: dict) -> dict:
    return {key: value for key, value in payload.items() if value is not None}
