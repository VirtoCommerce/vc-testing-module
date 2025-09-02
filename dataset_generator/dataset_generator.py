import random
from typing import Any, Dict

import pandas as pd
import yaml
from faker import Faker

fake = Faker()

with open("dataset_generator/electronics_store.yaml", "r") as file:
    config = yaml.safe_load(file)["categories"]


def generate_products(
    category_name: str, category_config: Dict[str, Any], num_products: int
) -> pd.DataFrame:
    products = []
    for _ in range(num_products):
        brand = random.choice(list(category_config["brands"].keys()))
        brand_data = category_config["brands"][brand]

        if category_name == "Laptops":
            model = random.choice(brand_data["models"])
        else:
            model = random.choice(brand_data)

        product_name = f"{brand} {model}"
        price = round(
            random.uniform(
                category_config["pricing"]["min"], category_config["pricing"]["max"]
            ),
            2,
        )

        product = {
            "Product Name": product_name,
            "Category": category_name,
            "Price": price,
        }

        if category_name == "Laptops":
            # Add common specs
            for spec, values in category_config["common_specs"].items():
                product[spec] = random.choice(values)

            # Add brand-specific specs
            for spec, values in brand_data["specs"].items():
                product[spec] = random.choice(values)
        else:
            for spec, values in category_config["specs"].items():
                product[spec] = random.choice(values)

        products.append(product)

    return pd.DataFrame(products)


all_products = []
for category_name, category_config in config.items():
    products_df = generate_products(category_name, category_config, 30)
    all_products.append(products_df)

final_df = pd.concat(all_products, ignore_index=True)
final_df.to_json("dataset_generator/products_dataset.json", orient="records", indent=4)

print("Dataset generated successfully!")
