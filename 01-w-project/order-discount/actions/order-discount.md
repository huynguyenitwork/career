# open discount

## schema-4: giảm % trên tổng hóa đơn

### payload

{
  "name": "Giảm giá đơn hàng theo %",
  "code": "RK7PROMO3",
  "description": "Giảm xx % trên tổng hóa đơn",
  "startTime": "2025-09-30T17:00:00.000Z",
  "endTime": null,
  "limitByWeekdays": false,
  "excludeSpecialDates": false,
  "promotionType": "ORDER_DISCOUNT",
  "storesSelection": "ALL",
  "shippingTypeSelection": "ALL",
  "customersSelection": "ALL",
  "applicableConditionType": "NO_APPLICABLE",
  "applicableConditionValue": null,
  "productsSelection": "ALL",
  "applicableValueType": "PERCENT",
  "applicableValueValueAmount": null,
  "applicableValueValuePercent": 15,
  "applicableValueValueLimitMaxAmount": null,
  "isCombinedProductDiscount": false,
  "isCombinedShipmentDiscount": false,
  "isCombinedOrderDiscount": false,
  "tenantId": "0192fda4-ba1b-76ef-bb1a-64c043a8e4a4",
  "eventType": "created",
  "entitledShippingTypes": null,
  "entitledSaleChannels": null
}

### wbs

| **thứ tự** | **hạng mục công việc**                  | **checklist hành động**                                                                                | **effort (tối thiểu)** | **effort (trung bình)** |
| ---------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------- | ----------------------- |
| **1**      | **xác định yêu cầu & thảo luận**        | xử lý order discount schema 4-6                                                                        | 0h                     | 0h                      |
| **2**      | **lập wbs chi tiết**                    | (phân rã 3 khối: validate / background / tracking) `[schema giảm % trên tổng hóa đơn (order discount]` | 0.25h                  | 0.5h                    |
| **3**      | **logic - validate + lưu raw**          | (validate payload webhook promotion)<br>(lưu raw promotion vào db)                                     | 1.5h                   | 3h                      |
| **4**      | **logic - background xử lý promotion**  | (background service xử lý promotion create/update/delete theo schema mới)                              | 3h                     | 6h                      |
| **5**      | **logic - tracking trạng thái dữ liệu** | (ghi log trạng thái từng giai đoạn xử lý promotion)                                                    | 1h                     | 2h                      |
| **6**      | **performance optimization**            | (kiểm tra bottleneck webhook / worker)                                                                 | 1h                     | 2h                      |
| **7**      | **dev test (dev/staging)**              | (deploy test + chạy luồng ecom → skytransfer end-to-end)                                               | 1h                     | 2h                      |
| **8**      | **pushcode, review, deploy**            | (tạo mr + review + deploy)                                                                             | 1h                     | 2h                      |

**tổng thời gian xử lý**

- tối thiểu: **8.75h (~1.2 ngày)**
- trung bình: **15.5h (~2.2 ngày)**

| **thứ tự** | **hạng mục công việc**                  | **checklist hành động**                                                                | **effort (tối thiểu)** | **effort (trung bình)** | **giữa (min+avg)/2** |
| ---------- | --------------------------------------- | -------------------------------------------------------------------------------------- | ---------------------- | ----------------------- | -------------------- |
| **1**      | **xác định yêu cầu & thảo luận**        | xử lý order discount schema 4-6                                                        | 0h                     | 0h                      | 0h                   |
| **2**      | **lập wbs chi tiết**                    | (phân rã 3 khối: validate / background / tracking) `[schema giảm % trên tổng hóa đơn]` | 0.25h                  | 0.5h                    | 0.375h               |
| **3**      | **logic - validate + lưu raw**          | (validate payload webhook promotion)(lưu raw promotion vào db)                         | 1.5h                   | 3h                      | 2.25h                |
| **4**      | **logic - background xử lý promotion**  | (background service xử lý promotion create/update/delete theo schema mới)              | 3h                     | 6h                      | 4.5h                 |
| **5**      | **logic - tracking trạng thái dữ liệu** | (ghi log trạng thái từng giai đoạn xử lý promotion)                                    | 1h                     | 2h                      | 1.5h                 |
| **7**      | **dev test (dev/staging)**              | (deploy test + chạy luồng ecom → skytransfer end-to-end)                               | 1h                     | 2h                      | 1.5h                 |
| **8**      | **pushcode, review, deploy**            | (tạo mr + review + deploy)                                                             | 1h                     | 2h                      | 1.5h                 |

### bdd

## scheme-04 — giảm % toàn đơn

### happy path

- given payload hợp lệ với `applicableValueValuePercent = 15`
- when tạo promotion
- then hệ thống lưu thành công
- and discount áp dụng = 15% \* tổng hóa đơn

### validate percent

- given `applicableValueValuePercent <= 0`
- when tạo promotion
- then reject với 400 "percent invalid"
- given `applicableValueValuePercent > 100`
- when tạo promotion
- then reject với 400 "percent vượt ngưỡng"

### validate condition type

- given `applicableConditionType != NO_APPLICABLE`
- when tạo promotion
- then reject vì scheme-04 không cho condition

### validate combine flag

- given `isCombinedOrderDiscount = true`
- when tạo promotion
- then reject vì scheme này không cho combine

---

## scheme-05 — giảm vnđ theo điều kiện đơn

### happy path

- given `applicableConditionValue = 1_000_000`
- and `applicableValueValueAmount = 100_000`
- when đơn hàng >= 1_000_000
- then giảm 100_000

### validate condition bắt buộc

- given `applicableConditionType != AMOUNT_ORDER`
- when tạo promotion
- then reject vì thiếu điều kiện đơn
- given `applicableConditionValue <= 0`
- when tạo promotion
- then reject "condition invalid"

### validate value amount

- given `applicableValueType = AMOUNT`
- and `applicableValueValueAmount <= 0`
- when tạo promotion
- then reject

### validate percent mode (nếu dùng %)

- given `applicableValueType = PERCENT`
- and `applicableValueValuePercent = null`
- when tạo promotion
- then reject

### validate special product config

- given `isConfigAppliedTogetherWithSpecialProducts = true`
- and thiếu `configAppliedTogetherWithSpecialProductsType`
- when tạo promotion
- then reject
- given config type = "EXCLUDED_PRODUCTS"
- when tính discount
- then loại product trong list khỏi base tính toán

### validate conflict config

- given vừa exclude vừa apply cùng product
- when tạo promotion
- then reject vì conflict rule

---

## scheme-06 — giảm % có max cap

### happy path

- given `percent = 30`
- and `maxAmount = 100_000`
- when đơn = 1_000_000
- then discount = min(30% \* 1_000_000, 100_000) = 100_000

### validate percent

- given `percent <= 0 or > 100`
- when tạo promotion
- then reject

### validate max cap

- given `applicableValueValueLimitMaxAmount <= 0`
- when tạo promotion
- then reject

### validate combine flags

- given combine flags = true
- when áp dụng promotion
- then cho phép stack với product + shipment + order

### validate logic cap

- given percent tính ra < max
- when apply
- then dùng giá trị percent
- given percent tính ra > max
- when apply
- then clamp về max

---

## cross-scheme guard (áp dụng chung)

- given `startTime > endTime`
- when tạo promotion
- then reject
- given `endTime = null`
- when tạo promotion
- then chấp nhận (infinite)
- given `promotionType != ORDER_DISCOUNT`
- when dùng schema này
- then reject
- given thiếu field bắt buộc theo scheme
- when validate
- then fail fast tại controller

---

## loại bỏ nhiễu (quan trọng)

- không test UI → chỉ test behavior tính toán + rule
- không test store/shipping nếu = "ALL"
- không test tenantId (infra concern)

---

## bước tiếp theo

- map mỗi scenario → 1 test case
- gom validate fail → 1 table-driven test
- implement test trước → ép design pipeline rõ rule
