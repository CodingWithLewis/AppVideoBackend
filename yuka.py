def format_product(food_item, user_id, barcode):
    print(barcode)
    nutriments = {}
    nutriments.setdefault("calcium", food_item["nutriments"].get("calcium", 0))
    nutriments.setdefault(
        "calcium_100g", food_item["nutriments"].get("calcium_100g", 0)
    )
    nutriments.setdefault(
        "calcium_serving", food_item["nutriments"].get("calcium_serving", 0)
    )
    nutriments.setdefault(
        "calcium_unit", food_item["nutriments"].get("calcium_unit", "g")
    )
    nutriments.setdefault(
        "calcium_value", food_item["nutriments"].get("calcium_value", 0)
    )
    nutriments.setdefault(
        "carbohydrates", food_item["nutriments"].get("carbohydrates", 0)
    )
    nutriments.setdefault(
        "carbohydrates_100g", food_item["nutriments"].get("carbohydrates_100g", 0)
    )
    nutriments.setdefault(
        "carbohydrates_serving", food_item["nutriments"].get("carbohydrates_serving", 0)
    )
    nutriments.setdefault(
        "carbohydrates_unit", food_item["nutriments"].get("carbohydrates_unit", "g")
    )
    nutriments.setdefault(
        "carbohydrates_value", food_item["nutriments"].get("carbohydrates_value", 0)
    )
    nutriments.setdefault("cholesterol", food_item["nutriments"].get("cholesterol", 0))
    nutriments.setdefault(
        "cholesterol_100g", food_item["nutriments"].get("cholesterol_100g", 0)
    )
    nutriments.setdefault(
        "cholesterol_serving", food_item["nutriments"].get("cholesterol_serving", 0)
    )
    nutriments.setdefault(
        "cholesterol_unit", food_item["nutriments"].get("cholesterol_unit", "g")
    )
    nutriments.setdefault(
        "cholesterol_value", food_item["nutriments"].get("cholesterol_value", 0)
    )
    nutriments.setdefault("energy", food_item["nutriments"].get("energy", 0))
    nutriments.setdefault("energy-kcal", food_item["nutriments"].get("energy-kcal", 0))
    nutriments.setdefault(
        "energy-kcal_100g", food_item["nutriments"].get("energy-kcal_100g", 0)
    )
    nutriments.setdefault(
        "energy-kcal_serving", food_item["nutriments"].get("energy-kcal_serving", 0)
    )
    nutriments.setdefault(
        "energy-kcal_unit", food_item["nutriments"].get("energy-kcal_unit", "g")
    )
    nutriments.setdefault(
        "energy-kcal_value", food_item["nutriments"].get("energy-kcal_value", 0)
    )
    nutriments.setdefault("energy_100g", food_item["nutriments"].get("energy_100g", 0))
    nutriments.setdefault(
        "energy_serving", food_item["nutriments"].get("energy_serving", 0)
    )
    nutriments.setdefault(
        "energy_unit", food_item["nutriments"].get("energy_unit", "g")
    )
    nutriments.setdefault(
        "energy_value", food_item["nutriments"].get("energy_value", 0)
    )
    nutriments.setdefault("fat", food_item["nutriments"].get("fat", 0))
    nutriments.setdefault("fat_100g", food_item["nutriments"].get("fat_100g", 0))
    nutriments.setdefault("fat_serving", food_item["nutriments"].get("fat_serving", 0))
    nutriments.setdefault("fat_unit", food_item["nutriments"].get("fat_unit", "g"))
    nutriments.setdefault("fat_value", food_item["nutriments"].get("fat_value", 0))
    nutriments.setdefault("fiber", food_item["nutriments"].get("fiber", 0))
    nutriments.setdefault("fiber_100g", food_item["nutriments"].get("fiber_100g", 0))
    nutriments.setdefault(
        "fiber_serving", food_item["nutriments"].get("fiber_serving", 0)
    )
    nutriments.setdefault("fiber_unit", food_item["nutriments"].get("fiber_unit", "g"))
    nutriments.setdefault("fiber_value", food_item["nutriments"].get("fiber_value", 0))
    nutriments.setdefault("iron", food_item["nutriments"].get("iron", 0))
    nutriments.setdefault("iron_100g", food_item["nutriments"].get("iron_100g", 0))
    nutriments.setdefault(
        "iron_serving", food_item["nutriments"].get("iron_serving", 0)
    )
    nutriments.setdefault("iron_unit", food_item["nutriments"].get("iron_unit", "g"))
    nutriments.setdefault("iron_value", food_item["nutriments"].get("iron_value", 0))
    nutriments.setdefault("proteins", food_item["nutriments"].get("proteins", 0))
    nutriments.setdefault(
        "proteins_100g", food_item["nutriments"].get("proteins_100g", 0)
    )
    nutriments.setdefault(
        "proteins_serving", food_item["nutriments"].get("proteins_serving", 0)
    )
    nutriments.setdefault(
        "proteins_unit", food_item["nutriments"].get("proteins_unit", "g")
    )
    nutriments.setdefault(
        "proteins_value", food_item["nutriments"].get("proteins_value", 0)
    )
    nutriments.setdefault("salt", food_item["nutriments"].get("salt", 0))
    nutriments.setdefault("salt_100g", food_item["nutriments"].get("salt_100g", 0))
    nutriments.setdefault(
        "salt_serving", food_item["nutriments"].get("salt_serving", 0)
    )
    nutriments.setdefault("salt_unit", food_item["nutriments"].get("salt_unit", "g"))
    nutriments.setdefault("salt_value", food_item["nutriments"].get("salt_value", 0))
    nutriments.setdefault(
        "saturated-fat", food_item["nutriments"].get("saturated-fat", 0)
    )
    nutriments.setdefault(
        "saturated-fat_100g", food_item["nutriments"].get("saturated-fat_100g", 0)
    )
    nutriments.setdefault(
        "saturated-fat_serving", food_item["nutriments"].get("saturated-fat_serving", 0)
    )
    nutriments.setdefault(
        "saturated-fat_unit", food_item["nutriments"].get("saturated-fat_unit", "g")
    )
    nutriments.setdefault(
        "saturated-fat_value", food_item["nutriments"].get("saturated-fat_value", 0)
    )
    nutriments.setdefault("sodium", food_item["nutriments"].get("sodium", 0))
    nutriments.setdefault("sodium_100g", food_item["nutriments"].get("sodium_100g", 0))
    nutriments.setdefault(
        "sodium_serving", food_item["nutriments"].get("sodium_serving", 0)
    )
    nutriments.setdefault(
        "sodium_unit", food_item["nutriments"].get("sodium_unit", "g")
    )
    nutriments.setdefault(
        "sodium_value", food_item["nutriments"].get("sodium_value", 0)
    )
    nutriments.setdefault("sugars", food_item["nutriments"].get("sugars", 0))
    nutriments.setdefault("sugars_100g", food_item["nutriments"].get("sugars_100g", 0))
    nutriments.setdefault(
        "sugars_serving", food_item["nutriments"].get("sugars_serving", 0)
    )
    nutriments.setdefault(
        "sugars_unit", food_item["nutriments"].get("sugars_unit", "g")
    )
    nutriments.setdefault(
        "sugars_value", food_item["nutriments"].get("sugars_value", 0)
    )
    nutriments.setdefault("trans-fat", food_item["nutriments"].get("trans-fat", 0))
    nutriments.setdefault(
        "trans-fat_100g", food_item["nutriments"].get("trans-fat_100g", 0)
    )
    nutriments.setdefault(
        "trans-fat_serving", food_item["nutriments"].get("trans-fat_serving", 0)
    )
    nutriments.setdefault(
        "trans-fat_unit", food_item["nutriments"].get("trans-fat_unit", "g")
    )
    nutriments.setdefault(
        "trans-fat_value", food_item["nutriments"].get("trans-fat_value", 0)
    )
    nutriments.setdefault("brand_owner", food_item.get("brand_owner", ""))
    nutriments.setdefault("image_url", food_item.get("image_url", ""))
    nutriments.setdefault("product_name", food_item.get("product_name", ""))

    nutriments["scanned_by"] = user_id
    nutriments["barcode"] = barcode

    nutriments.setdefault(
        "negatives",
        food_item["nutriscore"]["2023"]["data"]["components"].get("negative", 0),
    )
    nutriments.setdefault(
        "positives",
        food_item["nutriscore"]["2023"]["data"]["components"].get("positive", 0),
    )
    nutriments.setdefault("score", food_item["nutriscore"]["2023"]["grade"].upper())

    return nutriments
