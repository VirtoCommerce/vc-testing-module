import os


def main():
    scripts_folder = "./scripts"
    graphql_types_folder = "./graphql_types"

    os.system(f"python {scripts_folder}/generate_graphql_schema.py")

    if os.path.exists(f"{scripts_folder}/schema.graphql"):
        if not os.path.exists(graphql_types_folder):
            os.mkdir(graphql_types_folder)

        os.system("graphql2python generate --config ./graphql2python.yaml")

        os.remove(f"{scripts_folder}/schema.graphql")
    else:
        print(f"File {scripts_folder}/schema.graphql not found")


if __name__ == "__main__":
    main()
