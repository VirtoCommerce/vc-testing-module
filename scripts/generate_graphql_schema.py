import os
from dotenv import load_dotenv
from pathlib import Path
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from introspection_query import INTROSPECTION_QUERY
from graphql import build_client_schema, print_schema


def fetch_graphl_schema(endpoint_url: str, output_file: str):
    transport = RequestsHTTPTransport(url=endpoint_url, use_json=True, verify=True)

    try:
        print(f"\nFetching GraphQL schema from {endpoint_url}...", end=" ")

        client = Client(transport=transport, fetch_schema_from_transport=True)

        introspection_query = gql(INTROSPECTION_QUERY)
        introspection_data = client.execute(introspection_query)

        print("Done\n")

        schema = build_client_schema(introspection_data)
        sdl = print_schema(schema)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(sdl)

        print(f"GraphQL schema saved to: {output_file}\n")
    except Exception as e:
        print("Fail\n\n")
        print(f"Error fetching schema: {e}")


def main():
    load_dotenv()

    base_url = os.getenv("BASE_URL")
    endpoint_url = f"{base_url}/graphql"

    current_dir = Path(__file__).parent
    output_file = current_dir / "schema.graphql"

    fetch_graphl_schema(endpoint_url, output_file)


if __name__ == "__main__":
    main()
