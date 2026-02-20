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
