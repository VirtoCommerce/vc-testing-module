import os


def resolve_imports(graphql_file_path, base_dir="graphql_requests\\fragments"):
    """
    Resolves GraphQL fragment imports in a given .graphql file and returns the full query string.
    :param graphql_file_path: The path to the .graphql file.
    :param base_dir: The base directory containing all fragment files.
    :return: The full GraphQL query string with resolved imports.
    """

    resolved_fragments = []

    def resolve_file(file_path):
        if file_path in resolved_fragments:
            return ""

        resolved_fragments.append(file_path)

        full_path = os.path.join(base_dir, file_path)

        with open(full_path, "r") as f:
            lines = f.readlines()

        result = []

        for line in lines:
            if line.startswith("#import"):
                import_file = line.split('"')[1]
                result.append(resolve_file(import_file))
            else:
                result.append(line.strip())

        return "\n".join(result)

    return resolve_file(graphql_file_path)
