# spec mapping thuộc tính khuyến mại

#tag: #discount #discount-rule #mapping #db-level

> mục tiêu:
>
> - giảm dư thừa schema
> - tái sử dụng bảng mapping hiện có
> - có khung quyết định rõ cho field mới trong tương lai
> - tách giai đoạn "thiết kế rule" và "thực thi engine" [milvus](https://milvus.io/ai-quick-reference/what-are-the-best-practices-for-designing-relational-database-schemas)

---

## 1. bối cảnh & scope

- hệ thống hiện có các bảng chính:
  - "Discounts", "DiscountRules"
  - các bảng mapping: "ConceptMappings", "RegionMappings", "StoreMappings", "DiscountRuleMappings"
  - các bảng rule phụ: "DiscountBillTimes", "DiscountExclusionCategories", "DiscountExclusionDishes", "DiscountCombinations"…
- chuẩn bị thêm 16 thuộc tính cấu hình khuyến mại (payload từ bên ngoài), cần quyết định:
  - field nào được lưu
  - lưu ở bảng nào
  - field nào bỏ / block
- tài liệu này chỉ nói về **thiết kế mapping & schema**, chưa mô tả chi tiết code engine.

---

## 2. nguyên tắc thiết kế (db-level)

| mã     | nguyên tắc                                                                                                                        | dùng để làm gì                                                                                                                                                   |
| ------ | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| r-db-1 | 1 fact chỉ lưu 1 chỗ, không nhân bản meaning                                                                                      | tránh trùng lặp flag/điều kiện ở nhiều bảng [milvus](https://milvus.io/ai-quick-reference/what-are-the-best-practices-for-designing-relational-database-schemas) |
| r-db-2 | field phụ thuộc hoàn toàn vào pk của bảng → mới thêm cột; nếu phụ thuộc entity khác → dùng bảng riêng                             | chọn giữa thêm cột vào "Discounts" vs mapping table [stackoverflow](https://stackoverflow.com/questions/10754564/database-design-new-table-versus-new-columns)   |
| r-db-3 | dimension (store, region, shipping type, customer group, …) luôn thể hiện bằng mapping + fk, không lưu thẳng dạng json / enum lặp | tận dụng "RegionMappings", "StoreMappings", "DiscountRuleMappings"                                                                                               |
| r-db-4 | behavior flag chỉ ảnh hưởng engine, không dùng để join/filter → nên ở bảng chính với ít cột bool                                  | quyết định field nào được "nâng cấp" thành cột thật                                                                                                              |
| r-db-5 | config aggregate (nhiều field chỉ có nghĩa khi đi chung) → tách bảng riêng                                                        | tránh rải cột lẻ khắp bảng                                                                                                                                       |
| r-db-6 | field business chưa chốt meaning / phạm vi → block, không serialize                                                               | tránh "rác schema", không đoán trước [linkedin](https://www.linkedin.com/advice/0/how-can-you-design-database-schema-meets-business)                             |

---

## 3. phân loại chuẩn field

### 3.1. loại field

| loại             | tiêu chí                                                                            | xử lý chung                                                                 |
| ---------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| default          | biểu diễn trạng thái mặc định: all / no_limit / always_on; không tạo nhánh runtime  | không lưu, engine hardcode behavior mặc định                                |
| dimension filter | giá trị là 1 dimension rõ ràng có thể join (store/region/shipping/customer group/…) | dùng mapping table (RegionMappings, StoreMappings, DiscountRuleMappings, …) |
| behavior flag    | bật/tắt logic áp dụng, không dùng để filter theo entity                             | lưu vào bảng chính (Discounts/DiscountRules) hoặc derive vào flag tổng      |
| config aggregate | 2+ field chỉ có nghĩa khi đi chung, cấu hình riêng                                  | gom vào 1 bảng config riêng                                                 |
| undefined        | chưa chốt meaning hoặc tương lai mới dùng                                           | block payload, không lưu                                                    |

### 3.2. mapping loại → chiến lược db

| loại             | chiến lược db                                                                                                         |
| ---------------- | --------------------------------------------------------------------------------------------------------------------- |
| default          | không tạo cột / bảng; engine coi như luôn "bật" / "all" / "no_limit"                                                  |
| dimension filter | reuse mapping table hiện có; nếu cần entity mới (shipping type) → biểu diễn qua mapping tên/enum, không tạo cột extra |
| behavior flag    | nếu chưa có flag tổng → có thể thêm 1–2 cột; nếu đã có flag tổng (CombineAny) → derive runtime, không thêm cột        |
| config aggregate | tạo 1 bảng riêng, pk = (Id), fk tới DiscountId; các field con (type, isCombo, isVariant…) là cột của bảng này         |
| undefined        | không đụng schema; validation chặn tại API boundary                                                                   |

---

## 4. rule mapping cho 16 field

### 4.1. bảng quyết định chiến lược mapping

| field                                                  | mô tả business                                                       | phân loại                         | quyết định db                                | lưu ở đâu                     | rule thực thi (ý nghĩa)                                                                                                                                                             |
| ------------------------------------------------------ | -------------------------------------------------------------------- | --------------------------------- | -------------------------------------------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| shippingTypeSelection                                  | phạm vi loại đơn (dinein/takeaway/delivery), "all" = mọi loại        | dimension filter (có default all) | không lưu khi = "all"; nếu chọn subset → map | DiscountRuleMappings          | - nếu payload = "all": không query mapping theo shipping<br>- nếu payload là subset: tạo record DiscountRuleMappings với EntityName = "ShippingType", EntityId = enum shipping type |
| customersSelection                                     | áp dụng toàn bộ khách hàng, hiện không phân nhóm                     | default                           | không lưu                                    | -                             | engine hiểu mặc định: apply cho mọi khách; nếu tương lai có nhóm khách → thêm dimension mới + mapping riêng                                                                         |
| productsSelection                                      | áp dụng toàn bộ sản phẩm                                             | default                           | không lưu                                    | -                             | engine hiểu mặc định: all products; giới hạn bằng DiscountRuleBuys/Gets + DiscountExclusion\* nếu cần                                                                               |
| entitledSpecialVariants                                | danh sách variant đặc biệt (chưa chốt meaning)                       | undefined                         | block                                        | -                             | nếu payload có field này → reject, log "feature_not_supported"; không tạo bảng/cột                                                                                                  |
| entitledShippingTypes                                  | danh sách shipping types cụ thể được áp dụng                         | dimension filter                  | map                                          | DiscountRuleMappings          | mỗi shipping type được entitled → 1 record trong DiscountRuleMappings (DiscountId/RuleId tùy mức áp dụng, EntityName = "ShippingType")                                              |
| limitByWeekdays                                        | giới hạn theo ngày/giờ trong tuần, hiện mô tả "không giới hạn"       | default                           | không thêm cột; dùng bảng có sẵn khi cần     | DiscountBillTimes             | hiện tại: không tạo record → hiểu là no limit; nếu sau này cấu hình limit → sinh record vào DiscountBillTimes                                                                       |
| excludeSpecialDates                                    | loại trừ ngày đặc biệt, hiện "không loại"                            | default                           | không tạo bảng                               | -                             | khi có use case thật → tạo bảng DiscountExcludedDates(DiscountId, Date), hiện chưa                                                                                                  |
| applicableConditionType                                | loại điều kiện kích hoạt (chưa dùng, "không có điều kiện")           | default                           | không thêm cột                               | -                             | khi build condition engine → promote thành cột của DiscountRules                                                                                                                    |
| applicableConditionValue                               | giá trị điều kiện (ngưỡng tiền, số khách…)                           | default                           | không thêm cột                               | -                             | đi cùng applicableConditionType; chưa có type nên không lưu                                                                                                                         |
| isCombinedProductDiscount                              | cho phép/không cho combine với discount sản phẩm khác                | behavior flag                     | derive                                       | Discounts.CombineAny          | logic tổng hợp ở engine, không thêm cột: nếu bất kỳ isCombined\* = false → CombineAny = false cho discount đó                                                                       |
| isCombinedShipmentDiscount                             | cho phép/không cho combine với discount ship                         | behavior flag                     | derive                                       | Discounts.CombineAny          | same trên                                                                                                                                                                           |
| isCombinedOrderDiscount                                | cho phép/không cho combine với discount order khác                   | behavior flag                     | derive                                       | Discounts.CombineAny          | same trên                                                                                                                                                                           |
| isConfigAppliedTogetherWithSpecialProducts             | có bật config áp dụng cùng sản phẩm đặc biệt không                   | config aggregate                  | điều khiển việc có/không có record config    | DiscountSpecialProductConfigs | nếu false → không có record DiscountSpecialProductConfigs cho discount; nếu true → yêu cầu phải có tối thiểu 1 record config                                                        |
| configAppliedTogetherWithSpecialProductsType           | loại config (EXCLUDED_PRODUCTS/DO_NOT_APPLIED_ALONG_WITH_PRODUCTS/…) | config aggregate                  | cột trong bảng config                        | DiscountSpecialProductConfigs | lưu dạng enum/int để engine biết kiểu xử lý                                                                                                                                         |
| configAppliedTogetherWithSpecialProductsValueIsCombo   | config này áp dụng cho combo?                                        | config aggregate                  | cột trong bảng config                        | DiscountSpecialProductConfigs | bool: true nếu áp combo                                                                                                                                                             |
| configAppliedTogetherWithSpecialProductsValueIsVariant | config này áp dụng cho variant?                                      | config aggregate                  | cột trong bảng config                        | DiscountSpecialProductConfigs | bool: true nếu áp variant                                                                                                                                                           |

---

## 5. bảng / cột cần tạo (từ rule mapping)

### 5.1. bảng mới

```sql
create table "DiscountSpecialProductConfigs" (
    "Id" serial4 primary key,
    "DiscountId" int4 not null,
    "ConfigType" int4 not null,
    "IsCombo" bool not null,
    "IsVariant" bool not null
    -- fk:
    -- foreign key ("DiscountId") references "Discounts"("Id") on delete cascade
);


create table "ShippingTypes" (
  "Id" serial4 primary key,
  "Name" varchar(100) not null,          -- ví dụ: 'Dine-in', 'Takeaway', 'Delivery'
  "Code" varchar(40) null,               -- ví dụ: 'DINEIN', 'TAKEAWAY', 'DELIVERY'
  "GuidString" varchar(36) not null,
  "OrganizationId" int4 not null,
  "Status" int4 not null,                -- 1=active, 0=inactive (tùy convention hiện tại)
  "RefId" int4 not null                  -- nếu cần tham chiếu sang hệ thống khác, giống GuestTypes
);
```

- mục đích:
  - gom nhóm config "áp dụng cùng sản phẩm đặc biệt" vào 1 aggregate.
  - dễ mở rộng thêm cột khác nếu business yêu cầu, không đụng "Discounts".

### 5.2. tái sử dụng bảng mapping

- dùng "DiscountRuleMappings" cho shipping type:
  - `EntityName` = "ShippingType"
  - `EntityId` = giá trị enum cho DINEIN / TAKEAWAY / DELIVERY
- không tạo bảng mapping shipping mới.

### 5.3. cột **không** tạo lúc này

- **không** thêm cột:
  - applicableConditionType / applicableConditionValue
  - isCombinedProductDiscount / isCombinedShipmentDiscount / isCombinedOrderDiscount
- lý do: rule mapping quyết định:
  - condition engine chưa build → default.
  - combine behavior đã có "CombineAny" trong "Discounts".

---

## 6. rule thực thi tổng quát (ràng buộc cho dev)

> phần này là meta-rule, để mọi người implement đồng nhất; chi tiết engine có thể nằm ở spec khác, nhưng phải tuân theo các rule này. [camunda](https://camunda.com/blog/2025/02/decision-tables-for-automating-business-rules/)

| mã      | rule                                                                                                              | ý nghĩa                                                                   |
| ------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| r-run-1 | chỉ query mapping (RegionMappings/StoreMappings/DiscountRuleMappings) nếu field tương ứng trong payload ≠ default | tránh join thừa, giảm nhánh logic                                         |
| r-run-2 | nếu Discounts.CombineAny = false → reject apply thêm discount khác trên cùng order                                | enforce rule combine ở 1 chỗ duy nhất                                     |
| r-run-3 | không load "DiscountSpecialProductConfigs" nếu không có record cho DiscountId                                     | feature config aggregate = optional, không tạo nhánh rỗng                 |
| r-run-4 | nếu payload có field loại "undefined" (vd: entitledSpecialVariants) → fail early với lỗi chuẩn                    | ép business quyết định trước khi dev đụng schema                          |
| r-run-5 | không sử dụng field default để branch runtime (shippingTypeSelection="all"…)                                      | mọi nhánh đều dựa trên mapping/table, không dựa string literal từ payload |

---

## 7. thứ tự thực hiện (roadmap)

| bước | hành động                                                                                 | output                                                                                                                         |
| ---- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 1    | chốt bảng rule mapping 16 field (section 4)                                               | md này được coi là "contract" giữa po + dev                                                                                    |
| 2    | derive ddl từ rule                                                                        | script tạo "DiscountSpecialProductConfigs" + (optional) fk; không alter "Discounts"/"DiscountRules" cho field default/behavior |
| 3    | implement validation layer                                                                | chặn field "undefined", bỏ qua field "default" không map                                                                       |
| 4    | implement mapping shipping qua "DiscountRuleMappings"                                     | chấp nhận/ghi "entitledShippingTypes", derive từ "shippingTypeSelection" khi ≠ all                                             |
| 5    | implement combine logic dựa trên "CombineAny"                                             | 3 field isCombined\* chỉ dùng ở payload/UI, không chạm db                                                                      |
| 6    | sau khi engine ổn định, nếu cần → spec riêng cho condition engine (applicableCondition\*) | nhưng phải quay lại update tài liệu mapping này trước khi alter schema                                                         |

---

## 8. nguyên tắc reuse cho field mới (template)

khi xuất hiện field mới trong payload, phải làm theo thứ tự:

1. mô tả business ngắn: "field này quyết định cái gì, ở level nào (discount/order/item/shipping…)".
2. gán vào 1 trong 5 loại: default / dimension filter / behavior flag / config aggregate / undefined.
3. apply rule loại đó để quyết định:
   - có lưu không
   - lưu ở bảng nào (bảng chính, mapping, hay bảng config riêng).
4. chỉ khi xong 3 bước trên mới được:
   - đề xuất ddl
   - implement runtime.

> không đi qua bước 1–3 → mặc định field đó là "undefined" → block.
