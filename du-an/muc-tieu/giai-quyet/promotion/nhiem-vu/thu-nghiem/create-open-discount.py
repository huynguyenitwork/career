class PromotionSyncError(Exception):
    pass


# ===== Mock data access / API layer =====


def find_discount(name, sapcode):
    """
    return None nếu chưa tồn tại
    return dict nếu có
    """
    return None  # giả sử chưa có


def is_discount_different(existing, incoming):
    return True


def update_discount(discount):
    print("Update discount")


def create_discount(discount, discount_type):
    print("Create discount")


def find_discount_type(name, sapcode):
    return None


def create_discount_type(discount_type):
    # giả lập gọi API
    return {"id": 123, "name": discount_type["name"]}


# ===== Core business flow =====


def sync_promotion(promotion):
    print("== Trigger sync promotion ==")

    discount = promotion["discount"]

    # 1. Check discount tồn tại
    existing_discount = find_discount(discount["name"], discount["sapcode"])

    if existing_discount:
        # 2. Check khác biệt
        if not is_discount_different(existing_discount, discount):
            update_discount(discount)
            return "UPDATED"
    else:
        print("Discount not exists → create flow")

    # 3. Ensure discount type
    discount_type = ensure_discount_type(discount["type"])

    # 4. Create discount
    try:
        create_discount(discount, discount_type)
    except Exception as ex:
        raise PromotionSyncError("Create discount failed") from ex

    print("== Sync success ==")
    return "CREATED"


def ensure_discount_type(discount_type):
    existing_type = find_discount_type(discount_type["name"], discount_type["sapcode"])

    if existing_type:
        return existing_type

    # tạo mới
    try:
        created = create_discount_type(discount_type)
        return created
    except Exception as ex:
        raise PromotionSyncError("Create discount type failed") from ex


promotion_payload = {
    "discount": {
        "name": "SALE_11_11",
        "sapcode": "SAP001",
        "type": {"name": "ORDER_DISCOUNT", "sapcode": "DT01"},
    }
}

result = sync_promotion(promotion_payload)
print("Result:", result)
