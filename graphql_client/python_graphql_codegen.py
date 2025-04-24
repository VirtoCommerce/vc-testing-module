import os, requests
from colorama import Fore, Style, init as init_colorama
from graphql import (
    build_client_schema,
    get_introspection_query,
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLType,
)
from inflection import camelize, underscore
from typing import Callable


endpoint_url = f"{os.getenv('BASE_URL')}/graphql"

python_types_import_map = {
    "int": None,
    "float": None,
    "bool": None,
    "str": None,
    "datetime": "datetime",
    "decimal": "Decimal",
}


def fetch_graphql_schema(endpoint_url: str) -> GraphQLSchema:
    """Fetch GraphQL schema from endpoint URL using introspection query.

    Args:
        endpoint_url (str): URL of the GraphQL endpoint to fetch schema from

    Returns:
        GraphQLSchema: The parsed GraphQL schema object

    Raises:
        Exception: If schema fetch fails or response is invalid
    """

    introspection_query = get_introspection_query()

    headers = {"Content-Type": "application/json"}
    response = requests.post(endpoint_url, json={"query": introspection_query}, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch GraphQL schema: {response.status_code} {response.text}")

    try:
        return build_client_schema(response.json()["data"])
    except Exception as e:
        raise Exception(f"Failed to build client schema: {e}")


def graphql_type_to_python_type(graphql_type: GraphQLType) -> str:
    """Convert a GraphQL type to its corresponding Python type.

    Handles unwrapping non-null and list types to get to the underlying named type.
    Maps GraphQL scalar types to Python built-in types.

    Args:
        graphql_type (GraphQLType): The GraphQL type to convert

    Returns:
        str: The corresponding Python type name
    """

    # Handle list types
    if isinstance(graphql_type, GraphQLList):
        inner_type = graphql_type_to_python_type(graphql_type.of_type)
        return f"list[{inner_type}]"

    # Handle non-null types
    if isinstance(graphql_type, GraphQLNonNull):
        return graphql_type_to_python_type(graphql_type.of_type)

    # Handle base types
    match graphql_type.name:
        case "Int" | "Long" | "Seconds":
            return "int"
        case "Float":
            return "float"
        case "Boolean":
            return "bool"
        case "String" | "OptionalString" | "ID" | "DynamicPropertyValue" | "ModuleSettingValue" | "PropertyValue":
            return "str"
        case "Date" | "DateTime" | "Time":
            return "datetime"
        case "OptionalDecimal" | "OptionalNullableDecimal":
            return "Decimal"
        case _:
            return graphql_type.name


def get_import_lines(directory_path: str, imports: set, indent: int = 0) -> list[str]:
    result = []

    tabs = " " * (indent * 4)

    for item in imports:
        matched = False

        # Handle list types by extracting the inner type
        if item.startswith("list["):
            inner_type = item[5:-1]  # Remove 'list[' and ']'
            if inner_type not in python_types_import_map:
                module_path = f"{directory_path.replace('/', '.')}.{underscore(inner_type)}"
                result.append(f"{tabs}from {module_path} import {inner_type}")
            continue

        for module, import_name in python_types_import_map.items():
            if item == import_name:
                result.append(f"{tabs}from {module} import {import_name}")
                matched = True
                break

        if not matched:
            module_path = f"{directory_path.replace('/', '.')}.{underscore(item)}"
            result.append(f"{tabs}from {module_path} import {item}")

    return result


def write_content_to_file(file_path: str, content: str) -> None:
    with open(file_path, "w", encoding="utf-8", newline=None) as file:
        file.write(content)


def get_type_class_content(
    graphql_type: GraphQLObjectType | GraphQLInputObjectType | GraphQLEnumType, import_type_dir: str
) -> str:
    imports = set()

    content_lines = ["from pydantic import BaseModel"]
    content_lines.append("")

    content_lines.append(f"class {graphql_type.name}(BaseModel):")

    if hasattr(graphql_type, "fields") and graphql_type.fields:
        content_lines.append("    def __init__(self):")

        import_lines = get_import_lines(import_type_dir, imports, indent=2)
        for import_line in import_lines:
            content_lines.append(f"    {import_line}")

        content_lines.append("")

        for field_name, field in graphql_type.fields.items():
            is_required = isinstance(field.type, GraphQLNonNull)
            field_type = graphql_type_to_python_type(field.type)

            if field_type in python_types_import_map and python_types_import_map[field_type] is not None:
                imports.add(python_types_import_map[field_type])

            if field_type not in python_types_import_map:
                imports.add(field_type)

            optional_suffix = " | None" if not is_required else ""

            if field_name == "from":
                field_name = "from_"

            content_lines.append(f"        self.{field_name}: {field_type}{optional_suffix}")
    elif isinstance(graphql_type, GraphQLEnumType):
        for value_name in graphql_type.values:
            content_lines.append(f"    {value_name} = '{value_name}'")
    else:
        content_lines.append("    pass")

    content_lines.append("")

    content_lines[4:2] = get_import_lines(import_type_dir, imports, indent=2)

    return "\n".join(content_lines)


def get_request_class_content(request_name: str, request_field, request_type="query") -> str:
    args = []

    content_lines = ["from gql import gql"]

    return_type = graphql_type_to_python_type(request_field.type)

    if return_type in python_types_import_map and python_types_import_map[return_type] is not None:
        content_lines.append(f"from graphql_client.types.{python_types_import_map[return_type]} import {return_type}")

    if return_type not in python_types_import_map:
        content_lines.append(f"from graphql_client.types.{underscore(return_type)} import {return_type}")

    content_lines.append("")

    content_lines.append("")
    content_lines.append(f"class {camelize(request_name)}{camelize(request_type)}:")
    content_lines.append("    def __init__(self, graphql_client):")
    content_lines.append("        self.graphql_client = graphql_client")
    content_lines.append("")

    for arg_name, arg in request_field.args.items():
        args.append(f"${arg_name}: {arg.type}")

    args_string = ", ".join(args)

    has_return_fields = hasattr(request_field.type, "fields") and request_field.type.fields

    content_lines.append(f"    def execute(self, variables: dict, return_fields: str = None) -> {return_type}:")
    content_lines.append(f'        query_string = f"""')
    content_lines.append(f"            {request_type} {request_name}({args_string}) {{{{")
    content_lines.append(f"                {request_name}(")
    content_lines.append(
        f"                    "
        + ",\n                    ".join(f"{arg_name}: ${arg_name}" for arg_name in request_field.args)
    )
    content_lines.append("                )" + (" {{" if has_return_fields else ""))
    if has_return_fields:
        content_lines.append("                    {return_fields}")
        content_lines.append("                }}")
    content_lines.append("            }}")
    content_lines.append('        """\n')
    content_lines.append(f"        return self.graphql_client.execute(gql(query_string), variables)['{request_name}']")
    content_lines.append("")

    content = "\n".join(content_lines)

    return content


def generate_python_classes(schema: GraphQLSchema, output_directory: str = "graphql_client") -> None:
    # Generate types (objects, input types, enums)
    for type_name, graphql_type in schema.type_map.items():
        if type_name.startswith("__"):
            continue

        if isinstance(graphql_type, (GraphQLObjectType, GraphQLInputObjectType, GraphQLEnumType)):
            types_directory = f"{output_directory}/types"

            if not os.path.exists(types_directory):
                os.makedirs(types_directory)

            type_class_content = get_type_class_content(graphql_type, types_directory)
            write_content_to_file(f"{types_directory}/{underscore(graphql_type.name)}.py", type_class_content)

    # Generate queries
    query_type = schema.get_type("Query")
    if query_type and hasattr(query_type, "fields"):
        queries_directory = f"{output_directory}/queries"

        if not os.path.exists(queries_directory):
            os.makedirs(queries_directory)

        for query_name, query_field in query_type.fields.items():
            query_class_content = get_request_class_content(query_name, query_field)
            write_content_to_file(f"{queries_directory}/{underscore(query_name)}.py", query_class_content)

    # Generate mutations
    mutation_type = schema.get_type("Mutations")
    if mutation_type and hasattr(mutation_type, "fields"):
        mutations_directory = f"{output_directory}/mutations"

        if not os.path.exists(mutations_directory):
            os.makedirs(mutations_directory)

        for mutation_name, mutation_field in mutation_type.fields.items():
            mutation_class_content = get_request_class_content(mutation_name, mutation_field, "mutation")
            write_content_to_file(f"{mutations_directory}/{underscore(mutation_name)}.py", mutation_class_content)


def try_call(description: str, callable_func: Callable, *args, **kwargs):
    try:
        print(f"{description}...", end=" ")

        result = callable_func(*args, **kwargs)

        print(Fore.GREEN + "Done" + Style.RESET_ALL)

        return result
    except Exception as e:
        print(Fore.RED + "Fail" + Style.RESET_ALL)
        print(e)
        exit()


if __name__ == "__main__":
    init_colorama()

    schema = try_call(f"Fetching GraphQL schema from {endpoint_url}", fetch_graphql_schema, endpoint_url)
    try_call("Generating Python classes", generate_python_classes, schema)
