from typing import Any

import pytest


def build_seo_path(product: dict, dataset: dict) -> str:
    """Build full SEO path from category hierarchy + product semantic URL."""
    categories_by_id = {c["id"]: c for c in dataset["categories"]}
    parts = []
    category_id = product["categoryId"]
    while category_id:
        cat = categories_by_id[category_id]
        parts.append(cat["seoInfos"][0]["semanticUrl"])
        category_id = cat.get("parentId")
    parts.reverse()
    parts.append(product["seoInfos"][0]["semanticUrl"])
    return "/".join(parts)


_ADDRESS_FIELD_MAP = {
    "city": "city",
    "street": "line1",
    "postal_code": "postalCode",
}


def resolve_search_keyword(items: list[dict[str, Any]], case_id: str) -> str:
    """Extract a search keyword from GraphQL location data for the given test case."""
    if case_id == "full_name":
        return items[0]["name"]

    if case_id == "partial_name":
        return items[0]["name"].split()[0]

    if case_id in _ADDRESS_FIELD_MAP:
        field = _ADDRESS_FIELD_MAP[case_id]
        for loc in items:
            value = (loc.get("address") or {}).get(field)
            if value:
                return value
        pytest.skip(f"No location with '{case_id}' found in GraphQL data")

    if case_id == "special_char":
        for loc in items:
            if any(ch in loc["name"] for ch in "-'.&()"):
                return loc["name"]
        pytest.skip("No location with special characters found in GraphQL data")

    if case_id == "whitespace":
        return f"  {items[0]['name']}  "

    pytest.fail(f"Unknown search case: {case_id}")
