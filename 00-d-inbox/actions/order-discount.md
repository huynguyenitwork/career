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
