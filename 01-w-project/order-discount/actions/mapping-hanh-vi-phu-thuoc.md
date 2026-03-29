# mapping hành vi + phụ thuộc

#tag: #order-discount #skytransfer-skycrm-api

## dữ liệu skytransfer

### 1. nhóm chọn phạm vi áp dụng (scope)

- `productsSelection` → quyết định **nhóm field nào được dùng**
  - = "ALL" → bỏ qua toàn bộ `entitled*`
  - = "COLLECTION_PREREQUISITE" → dùng `entitledCollections`
  - = "PRODUCT_PREREQUISITE" → dùng `entitledProducts`
  - = "VARIANT_PREREQUISITE" → dùng `entitledVariants` hoặc `entitledSpecialVariantIds`

- `entitledCollections` → chỉ có hiệu lực khi `productsSelection = COLLECTION_PREREQUISITE`
- `entitledCombos` → chỉ có hiệu lực khi có logic combo riêng (implicit phụ thuộc `isConfigAppliedTogetherWithSpecialProductsValueIsCombo = true`)
- `entitledProducts` → chỉ có hiệu lực khi `productsSelection = PRODUCT_PREREQUISITE`
- `entitledVariants` → chỉ có hiệu lực khi `productsSelection = VARIANT_PREREQUISITE`
- `entitledSpecialVariantIds` → override/augment `entitledVariants` (ưu tiên cao hơn nếu cùng tồn tại)

---

### 2. nhóm điều kiện áp dụng (condition)

- `applicableConditionType` → quyết định có cần `applicableConditionValue` hay không
  - = "NO_APPLICABLE" → ignore `applicableConditionValue`
  - = "QUANTITY_ORDER" | "AMOUNT_ORDER" | "AMOUNT_ORDER_ITEM" → bắt buộc có `applicableConditionValue`
- `applicableConditionValue` → chỉ có ý nghĩa khi `applicableConditionType != NO_APPLICABLE`

---

### 3. nhóm loại discount (stacking behavior)

- `isCombinedProductDiscount`
  - = true → discount này có thể chạy cùng discount sản phẩm khác
  - ảnh hưởng conflict resolution với `configAppliedTogetherWithSpecialProductsType`

- `isCombinedOrderDiscount`
  - = true → discount này có thể chạy cùng discount cấp order
  - độc lập với product nhưng conflict khi tổng hợp cuối

---

### 4. nhóm config special products (core logic phụ thuộc chéo nhiều nhất)

- `isConfigAppliedTogetherWithSpecialProducts`
  - = false → bỏ qua toàn bộ `configAppliedTogetherWithSpecialProducts*`
  - = true → kích hoạt các field dưới

- `configAppliedTogetherWithSpecialProductsType`
  - chỉ có hiệu lực khi `isConfigAppliedTogetherWithSpecialProducts = true`
  - = "EXCLUDED_PRODUCTS" → loại trừ list sản phẩm trong scope
  - = "DO_NOT_APPLIED_ALONG_WITH_PRODUCTS" → không apply nếu có sản phẩm đó trong order

- `configAppliedTogetherWithSpecialProductsValueIsCombo`
  - = true → `entitledCombos` trở thành nguồn dữ liệu chính
  - = false → ignore `entitledCombos`

- `configAppliedTogetherWithSpecialProductsValueIsVariant`
  - = true → `entitledVariants` / `entitledSpecialVariantIds` được dùng
  - = false → ignore variant-level

---

## dependency graph rút gọn (loại nhiễu)

- `productsSelection` → quyết định dùng `entitled*` nào
- `applicableConditionType` → quyết định dùng `applicableConditionValue`
- `isConfigAppliedTogetherWithSpecialProducts` → bật/tắt toàn bộ config special
- khi bật:
  - `configAppliedTogetherWithSpecialProductsType` → quyết định rule conflict
  - `ValueIsCombo` → dùng `entitledCombos`
  - `ValueIsVariant` → dùng `entitledVariants` / `entitledSpecialVariantIds`

---

## loại bỏ ngay (giảm nhiễu)

- không bao giờ dùng đồng thời `entitledProducts`, `entitledCollections`, `entitledVariants` → chọn 1 theo `productsSelection`
- nếu `isConfigAppliedTogetherWithSpecialProducts = false` → bỏ toàn bộ 4 field config phía dưới
- nếu `applicableConditionType = NO_APPLICABLE` → bỏ `applicableConditionValue`

---

## bước tiếp theo

- vẽ 3 flow riêng:
  - scope resolve (productsSelection)
  - condition check
  - special config override

- chạy test case:
  - mỗi flow chỉ bật 1 nhánh → tránh conflict ẩn

## cây quyết định

```
discount
├── scope_resolve (productsSelection)
│   ├── "ALL"
│   │   └── ignore: entitledCollections, entitledProducts, entitledVariants, entitledSpecialVariantIds
│   │
│   ├── "COLLECTION_PREREQUISITE"
│   │   └── use: entitledCollections
│   │
│   ├── "PRODUCT_PREREQUISITE"
│   │   └── use: entitledProducts
│   │
│   └── "VARIANT_PREREQUISITE"
│       ├── base: entitledVariants
│       └── override: entitledSpecialVariantIds (priority > entitledVariants)
│
├── condition_check (applicableConditionType)
│   ├── "NO_APPLICABLE"
│   │   └── ignore: applicableConditionValue
│   │
│   └── "QUANTITY_ORDER" | "AMOUNT_ORDER" | "AMOUNT_ORDER_ITEM"
│       └── require: applicableConditionValue
│
├── stacking_behavior
│   ├── isCombinedProductDiscount
│   │   └── affect: conflict_resolution(product-level)
│   │
│   └── isCombinedOrderDiscount
│       └── affect: conflict_resolution(order-level)
│
└── special_config (isConfigAppliedTogetherWithSpecialProducts)
    ├── false
    │   └── ignore:
    │       - configAppliedTogetherWithSpecialProductsType
    │       - configAppliedTogetherWithSpecialProductsValueIsCombo
    │       - configAppliedTogetherWithSpecialProductsValueIsVariant
    │       - entitledCombos
    │
    └── true
        ├── configAppliedTogetherWithSpecialProductsType
        │   ├── "EXCLUDED_PRODUCTS"
        │   │   └── behavior: exclude from scope_resolve result
        │   │
        │   └── "DO_NOT_APPLIED_ALONG_WITH_PRODUCTS"
        │       └── behavior: block discount if match exists in order
        │
        ├── value_source_switch
        │   ├── configAppliedTogetherWithSpecialProductsValueIsCombo = true
        │   │   └── use: entitledCombos
        │   │
        │   └── configAppliedTogetherWithSpecialProductsValueIsVariant = true
        │       ├── base: entitledVariants
        │       └── override: entitledSpecialVariantIds
        │
        └── note
            └── nếu cả combo=false và variant=false → config vô nghĩa → loại
```

### trường hợp configAppliedTogetherWithSpecialProductsType

```
configAppliedTogetherWithSpecialProductsType
├── "EXCLUDED_PRODUCTS"
│   └── hành vi: loại sản phẩm khỏi phạm vi áp dụng discount
│       ├── scope_resolve result: {A, B, C, D}
│       └── EXCLUDED_PRODUCTS = {B, D}
│           → kết quả áp dụng discount: {A, C}
│
└── "DO_NOT_APPLIED_ALONG_WITH_PRODUCTS"
    └── hành vi: chặn toàn bộ discount nếu đơn có sản phẩm trùng
        ├── đơn hàng: {A, B, C}
        └── DO_NOT_APPLIED_ALONG_WITH_PRODUCTS = {B, D}
            → kết quả: discount không áp dụng cho cả đơn hàng
```

## dữ liệu crm

### rule

- cần dùng lại toàn bộ các cấu hình và dữ liệu từ ecom vì có lọc sản phẩm theo loại đặc biệt (combo/variant)

## bdd gherkin

### feature: phân giải phạm vi discount

**mục tiêu:** xác định đúng các sản phẩm áp dụng theo `productsSelection`

```gherkin
@order-discount @skytransfer-skycrm-api
feature: phân giải phạm vi discount

  scenario: productsSelection = ALL
    given discount.productsSelection = "ALL"
    when phân giải phạm vi
    then entitledCollections, entitledProducts, entitledVariants, entitledSpecialVariantIds bị bỏ qua

  scenario: productsSelection = COLLECTION_PREREQUISITE
    given discount.productsSelection = "COLLECTION_PREREQUISITE"
    when phân giải phạm vi
    then chỉ dùng entitledCollections

  scenario: productsSelection = PRODUCT_PREREQUISITE
    given discount.productsSelection = "PRODUCT_PREREQUISITE"
    when phân giải phạm vi
    then chỉ dùng entitledProducts

  scenario: productsSelection = VARIANT_PREREQUISITE
    given discount.productsSelection = "VARIANT_PREREQUISITE"
    when phân giải phạm vi
    then dùng entitledVariants làm base
    and nếu tồn tại entitledSpecialVariantIds thì override entitledVariants
```

---

### feature: kiểm tra điều kiện discount

**mục tiêu:** xác thực điều kiện áp dụng

```gherkin
@order-discount @skytransfer-skycrm-api
feature: kiểm tra điều kiện discount

  scenario: applicableConditionType = NO_APPLICABLE
    given discount.applicableConditionType = "NO_APPLICABLE"
    when đánh giá điều kiện
    then applicableConditionValue bị bỏ qua

  scenario: applicableConditionType yêu cầu giá trị
    given discount.applicableConditionType in ["QUANTITY_ORDER", "AMOUNT_ORDER", "AMOUNT_ORDER_ITEM"]
    when đánh giá điều kiện
    then applicableConditionValue là bắt buộc
```

---

### feature: hành vi kết hợp discount

**mục tiêu:** xác định xung đột và khả năng chạy cùng các discount khác

```gherkin
@order-discount @skytransfer-skycrm-api
feature: hành vi kết hợp discount

  scenario: isCombinedProductDiscount = true
    given discount.isCombinedProductDiscount = true
    when kiểm tra xung đột
    then discount có thể chạy cùng các discount cấp product khác

  scenario: isCombinedOrderDiscount = true
    given discount.isCombinedOrderDiscount = true
    when kiểm tra xung đột
    then discount có thể chạy cùng các discount cấp order khác
```

---

### feature: config sản phẩm đặc biệt

**mục tiêu:** xử lý logic phức tạp của các config special

```gherkin
@order-discount @skytransfer-skycrm-api
feature: config sản phẩm đặc biệt

  scenario: special config tắt
    given discount.isConfigAppliedTogetherWithSpecialProducts = false
    when phân giải special config
    then bỏ qua:
      - configAppliedTogetherWithSpecialProductsType
      - configAppliedTogetherWithSpecialProductsValueIsCombo
      - configAppliedTogetherWithSpecialProductsValueIsVariant
      - entitledCombos

  scenario: loại trừ sản phẩm
    given discount.isConfigAppliedTogetherWithSpecialProducts = true
    and discount.configAppliedTogetherWithSpecialProductsType = "EXCLUDED_PRODUCTS"
    when phân giải special config
    then các sản phẩm trong danh sách exclude bị loại khỏi scope_resolve

  scenario: không áp dụng khi có sản phẩm khác
    given discount.isConfigAppliedTogetherWithSpecialProducts = true
    and discount.configAppliedTogetherWithSpecialProductsType = "DO_NOT_APPLIED_ALONG_WITH_PRODUCTS"
    when phân giải special config
    then discount bị chặn nếu tồn tại sản phẩm trong order

  scenario: combo override
    given discount.isConfigAppliedTogetherWithSpecialProducts = true
    and discount.configAppliedTogetherWithSpecialProductsValueIsCombo = true
    when phân giải special config
    then dùng entitledCombos làm nguồn chính

  scenario: variant override
    given discount.isConfigAppliedTogetherWithSpecialProducts = true
    and discount.configAppliedTogetherWithSpecialProductsValueIsVariant = true
    when phân giải special config
    then dùng entitledVariants làm base
    and nếu tồn tại entitledSpecialVariantIds thì override entitledVariants

  scenario: special config vô nghĩa
    given discount.isConfigAppliedTogetherWithSpecialProducts = true
    and discount.configAppliedTogetherWithSpecialProductsValueIsCombo = false
    and discount.configAppliedTogetherWithSpecialProductsValueIsVariant = false
    when phân giải special config
    then config bị bỏ qua
```
