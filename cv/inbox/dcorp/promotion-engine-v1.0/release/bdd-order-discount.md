## mục tiêu
- hiểu luồng/contract api/giao tiếp/trách nhiệm giữa các service
- các kịch bản happy case của order discount
- nắm được api contract/field contract/validation rules/behavior spec/test matrix của order discount
## mapping contract (spec → hành vi hệ thống)
1. skytransfer layer
	* nhận webhook từ ecom lưu dữ liệu thô
	* validate cấu trúc dữ liệu (schema)
	* kiểm tra rule nghiệp vụ
	* loại bỏ trạng thái không hợp lệ sớm
2. skycrm layer
	* lưu promotion dạng master data
	* trở thành nguồn dữ liệu chính (source of record)
	* gởi dữ liệu xuống refagent hoặc rk7 (tùy cấu hình hệ thống)
3. refagent layer
	* chuyển đổi payload sang format của rk7
	* thực thi đồng bộ xuống rk7
	* xử lý cơ chế retry khi lỗi
4. rk7 layer
	* chỉ nhận promotion đã đơn giản hóa
	* trả về refcode và refid sau khi lưu thành công
## schema
### schema 4
- scheme type: giảm giá đơn hàng
- scheme option: giảm giá đơn hàng theo %
- scheme example: giảm xx % trên tổng hóa đơn
- promotion example: giảm 15% trên tổng hóa đơn
### schema 5
- scheme type: giảm giá đơn hàng
- scheme option: giảm giá đơn hàng theo vnđ
- scheme example: giảm xxx vnd cho hoá đơn xxx vnd
- promotion example: voucher 100k cho hoá đơn 1.000.000đ
### schema 6
- scheme type: giảm giá đơn hàng
- scheme option: giảm giá đơn hàng theo vnđ
- scheme example: giảm xxx% tối đa xxxvnd
- promotion example: giảm 30% trên đơn hàng tối đa 100k
## api definition

```txt
type:: skytransfer-opd
group:: order-discount
action:: create/update/delete

name:: sync open discount promotion
method:: post
endpoint:: /ecom/webhook/sync-promotion
```
### request payload skytransfer
```json
{
  "name": "auto opd stg 20260312095509",
  "code": "opd-20260302090347",
  "status": "ACTIVE",
  "description": "auto opd stg 20260312095509",
  "startTime": "2026-02-10T10:00:00+0300",
  "endTime": "02/14/2026 10:00:00 AM",
  "promotionType": "ORDER_DISCOUNT",
  "tenantId": "0192fda4-ba1b-76ef-bb1a-64c043a8e4a4",
  "eventType": "created",
  "storesSelection": "STORE_PREREQUISITE",
  "entitledStores": [
    "TPC_068_EST_HCM",
    "TPC_053_SVH_HCM"
  ],
  "applicableValueType":"PERCENT",
  "applicableValueValueAmount":null,
  "applicableValueValuePercent": 15,
  "applicableValueValueLimitMaxAmount":null,
  "applicableConditionType":"NO_APPLICABLE",
  "applicableConditionValue":null,
  "productsSelection":"COLLECTION_PREREQUISITE",
  "entitledCollections": ["XXX", "YYY"],
  "entitledCombos": null,
  "entitledProducts": null,
  "entitledVariants": null,
  "isCombinedProductDiscount":false,
  "isCombinedOrderDiscount":false,
  
  "isConfigAppliedTogetherWithSpecialProducts": true,
  "configAppliedTogetherWithSpecialProductsType": "DO_NOT_APPLIED_ALONG_WITH_PRODUCTS",
  "configAppliedTogetherWithSpecialProductsValueIsCombo": true,
  "configAppliedTogetherWithSpecialProductsValueIsVariant": true
}
```
### field contract

| tham số                                                | loại                         | yêu cầu | mô tả                                                                                      |
| ------------------------------------------------------ | ---------------------------- | ------- | ------------------------------------------------------------------------------------------ |
| name                                                   | String                       | Có      | Tên khuyến mại                                                                             |
| code                                                   | String                       | Có      | Mã khuyến mãi                                                                              |
| status                                                 | String                       | Có      | DRAFT, INACTIVE, ACTIVE ⇔ STOP, EXPIRED ⇒ (Gia hạn ⇒ update endTime)                       |
| description                                            | String                       | Không   | Mô tả chi tiết                                                                             |
| startTime                                              | timestamp/datetime (formats) | Có      | Thời gian bắt đầu                                                                          |
| endTime                                                | timestamp/datetime (formats) | Không   | Thời gian kết thúc                                                                         |
| promotionType                                          | String                       | Có      | Loại khuyến mãi: OPEN_DISCOUNT, ORDER_DISCOUNT                                             |
| tenantId                                               | String                       | Có      | Tenant                                                                                     |
| eventType                                              | String                       | Có      | created, updated, deleted                                                                  |
| storesSelection                                        | String                       | Có      | Cửa hàng áp dụng: STORE_PREREQUISITE, ALL                                                  |
| entitledStores                                         | Array                        | Không   | Dành cho tuỳ chọn cửa hàng cụ thể                                                          |
| applicableValueType                                    | String                       | Có      | Giá trị khuyến mãi: PERCENT, AMOUNT, FREE                                                  |
| applicableValueValueAmount                             | Number                       | Không   | Dành cho tuỳ chọn AMOUNT cụ thể                                                            |
| applicableValueValuePercent                            | Number                       | Không   | Dành cho tuỳ chọn PERCENT cụ thể                                                           |
| applicableValueValueLimitMaxAmount                     | Number                       | Không   | Giới hạn giá trị tối đa                                                                    |
| applicableConditionType                                | String                       | Có      | Điều kiện áp dụng: NO_APPLICABLE, QUANTITY_ORDER, AMOUNT_ORDER, AMOUNT_ORDER_ITEM          |
| applicableConditionValue                               | Number                       | Không   | Giá trị tương ứng với điều kiện áp dụng                                                    |
| productsSelection                                      | String                       | Có      | Sản phẩm áp dụng: ALL, COLLECTION_PREREQUISITE, PRODUCT_PREREQUISITE, VARIANT_PREREQUISITE |
| entitledCollections                                    | Array                        | Không   | Dành cho tuỳ chọn nhóm sản phẩm cụ thể                                                     |
| entitledCombos                                         | Array                        | Không   | Dành cho tuỳ chọn combo cụ thể                                                             |
| entitledProducts                                       | Array                        | Không   | Dành cho tuỳ chọn sản phẩm cụ thể                                                          |
| entitledVariants                                       | Array                        | Không   | Dành cho tuỳ chọn biến thể cụ thể                                                          |
| isCombinedProductDiscount                              | Boolean                      | Có      | Áp dụng đồng thời – Giảm giá sản phẩm                                                      |
| isCombinedOrderDiscount                                | Boolean                      | Có      | Áp dụng đồng thời – Giảm giá đơn hàng                                                      |
| isConfigAppliedTogetherWithSpecialProducts             | Boolean                      | Không   | Cấu hình chung áp dụng các sản phẩm đặc biệt                                               |
| configAppliedTogetherWithSpecialProductsType           | String                       | Không   | EXCLUDED_PRODUCTS, DO_NOT_APPLIED_ALONG_WITH_PRODUCTS                                      |
| configAppliedTogetherWithSpecialProductsValueIsCombo   | Boolean                      | Không   | Áp dụng cho combo                                                                          |
| configAppliedTogetherWithSpecialProductsValueIsVariant | Boolean                      | Không   | Áp dụng cho biến thể                                                                       |
### validation rules
- name là bắt buộc
* code là bắt buộc (định danh duy nhất cho mỗi giảm giá)
* promotionType phải bằng "ORDER_DISCOUNT"
* status là bắt buộc ∈ {ACTIVE, INACTIVE, DRAFT}
* startTime < endTime
- tenantId là bắt buộc
- eventType là bắt buộc
* entitledStores không được để trống khi  storesSelection = store_prerequisite
- applicableValueType là bắt buộc
- applicableValueType = "percent" ⇒ applicableValueValuePercent là bắt buộc
- applicableValueValuePercent ∈ [0, 100]
- applicableValueType = "amount" ⇒ applicableValueValueAmount là bắt buộc
- applicableConditionType là bắt buộc
- productsSelection là bắt buộc
- isCombinedProductDiscount là bắt buộc
- isCombinedOrderDiscount là bắt buộc
- validation business rule:
	- **create**: group (**non-deleted**) + discount (**not-exist**) $\rightarrow$ success
	- **update**: group (**non-deleted**) + discount (**non-deleted**) $\rightarrow$ success
	- **delete**: group (**non-deleted**) + discount (**non-deleted**) $\rightarrow$ allow soft-delete
### response contract skytransfer
#### success
```json
{
  "syncTaskId": 16,
  "data": 337,
  "status": "success",
  "success": true,
  "httpStatusCode": 200,
  "error": null,
  "message": "skytransfer gọi đồng bộ sang crm thành công, chờ gởi"
}
```
#### error
```json
{
  "success": false,
  "httpStatusCode": 400,
  "error": "TRANSFER-VAL-008",
  "message": "startTime phải nhỏ hơn endTime"
}
```

## as-is flow
### gherkin (behavior spec) order discount

```gherkin
Feature: Quản lý và Đồng bộ Promotion từ Ecom sang SkyCRM (Open Discount)

  # TẦNG 1: KIỂM SOÁT ĐIỀU KIỆN ĐẦU VÀO (VALIDATION LAYER)
  # Mục tiêu: SkyTransfer chặn các request không hợp lệ trước khi gửi sang SkyCRM

  Scenario Outline: 1.1 - Validate thông tin chung và cấu hình hệ thống
    Given SkyTransfer nhận được yêu cầu đồng bộ từ Ecom
    When SkyTransfer kiểm tra dữ liệu <trường dữ liệu> có giá trị <giá trị>
    And cấu hình hệ thống <config>
    Then Kết quả là <kết quả> với mã lỗi "<mã lỗi>" và thông báo "<thông báo>"

    Examples: 
      | trường dữ liệu  | giá trị    | config       | kết quả    | mã lỗi           | thông báo                                                          |
      | --------------- | ---------- | ------------ | ---------- | ---------------- | ------------------------------------------------------------------ |
      | name            | rỗng       | Đầy đủ       | Thất bại   | TRANSFER-VAL-001 | name không được rỗng                                               |
      | code            | rỗng       | Đầy đủ       | Thất bại   | TRANSFER-VAL-002 | code không được rỗng                                               |
      | status          | rỗng       | Đầy đủ       | Thất bại   | TRANSFER-VAL-003 | status không được rỗng                                             |
      | promotionType   | rỗng       | Đầy đủ       | Thất bại   | TRANSFER-VAL-004 | promotionType không được rỗng                                      |
      | tenantId        | rỗng       | Đầy đủ       | Thất bại   | TRANSFER-VAL-005 | tenantId không được rỗng                                           |
      | eventType       | rỗng       | Đầy đủ       | Thất bại   | TRANSFER-VAL-006 | eventType không được rỗng                                          |
      | storesSelection | rỗng       | Đầy đủ       | Thất bại   | TRANSFER-VAL-007 | storesSelection không được rỗng                                    |
      | startTime       | >= endTime | Đầy đủ       | Thất bại   | TRANSFER-VAL-008 | startTime phải nhỏ hơn endTime                                     |
      | Hợp lệ          | Hợp lệ     | Thiếu OrgId  | Thất bại   | TRANSFER-NF-002  | masterDataOrganizationId chưa được khai báo trong bảng parameter   |
      | Hợp lệ          | Hợp lệ     | Thiếu GrName | Thất bại   | TRANSFER-NF-003  | skyCRMApiDiscountGroupName chưa được khai báo trong bảng parameter |
      | Hợp lệ          | Hợp lệ     | Thiếu GrCode | Thất bại   | TRANSFER-NF-004  | skyCRMApiDiscountGroupCode chưa được khai báo trong bảng parameter |
      | Hợp lệ          | Hợp lệ     | Đầy đủ       | Thành công | none             | Cho phép xử lý tiếp sang Scenario 1.2                              |

  Scenario Outline: 1.2 - Validate chuyên biệt cho loại Order Discount
    Given SkyTransfer nhận được yêu cầu đồng bộ với promotionType là "order_discount"
    When SkyTransfer kiểm tra trường <trường dữ liệu> có giá trị <giá trị>
    Then Kết quả là Thất bại với mã lỗi "<mã lỗi>" và thông báo "<thông báo>"

    Examples: 
      | trường dữ liệu            | giá trị | mã lỗi           | thông báo                                 |
      | ------------------------- | ------- | ---------------- | ----------------------------------------- |
      | applicableConditionType   | rỗng    | TRANSFER-VAL-013 | applicableConditionType không được rỗng   |
      | productsSelection         | rỗng    | TRANSFER-VAL-014 | productsSelection không được rỗng         |
      | isCombinedProductDiscount | rỗng    | TRANSFER-VAL-015 | isCombinedProductDiscount không được rỗng |
      | isCombinedOrderDiscount   | rỗng    | TRANSFER-VAL-016 | isCombinedOrderDiscount không được rỗng   |
      | Hợp lệ                    | Hợp lệ  | none             | Cho phép xử lý tiếp sang SkyCRM           |

# TẦNG 2: XỬ LÝ NGHIỆP VỤ VÀ PHẢN HỒI REAL-TIME (BUSINESS LAYER)
  # Mục tiêu: SkyTransfer điều phối dựa trên hành động, mã định danh và trạng thái thực thể tại SkyCRM

  Scenario Outline: 2.1 - Điều phối dựa trên ma trận trạng thái sang SkyCRM và phản hồi kết quả cho Ecom
    Given Một request Promotion đã vượt qua bước validate tại SkyTransfer
    And Ecom gửi yêu cầu với hành động <hành động> với groupId là <groupId>
    And Trạng thái thực thể tại SkyCRM là Group:<trạng thái group> và Discount:<trạng thái discount>
    When SkyTransfer thực hiện gửi yêu cầu sang SkyCRM
    Then SkyCRM phản hồi quyết định xử lý là <quyết định> và mã lỗi "<lỗi crm>" (nếu có)
    And SkyTransfer trả kết quả về cho Ecom là "<thông báo ecom>"

    Examples: 
      | hành động | groupId | trạng thái group | trạng thái discount | quyết định        | lỗi crm        | thông báo ecom                              |
      | --------- | ------- | ---------------- | ------------------- | ----------------- | -------------- | ------------------------------------------- |
      | chung     | invalid | any              | any                 | reject            | SKYCRM-NF-001  | OrganizationId {0} không tồn tại            |
      | create    | valid   | not-exist        | not-exist           | reject            | SKYCRM-NF-002  | Discount group gensapcode {0} không tồn tại |
      | create    | valid   | non-deleted      | not-exist           | allow             | none           | Thành công                                  |
      | create    | valid   | non-deleted      | non-deleted         | reject_duplicate  | SKYCRM-VAL-002 | Discount với gensapcode {0} đã tồn tại      |
      | create    | valid   | non-deleted      | soft-deleted        | reject            | SKYCRM-VAL-003 | Discount với gensapcode {0} đã bị xóa       |
      | create    | valid   | soft-deleted     | not-exist           | reject            | SKYCRM-VAL-001 | Discount group gensapcode {0} đã bị xóa     |
      | update    | valid   | not-exist        | any                 | reject            | SKYCRM-NF-002  | Discount group gensapcode {0} không tồn tại |
      | update    | valid   | soft-deleted     | non-deleted         | reject            | SKYCRM-VAL-001 | Discount group gensapcode {0} đã bị xóa     |
      | update    | valid   | non-deleted      | non-deleted         | allow             | none           | Thành công                                  |
      | update    | valid   | non-deleted      | not-exist           | reject            | SKYCRM-NF-003  | Discount với gensapcode {0} không tồn tại   |
      | update    | valid   | non-deleted      | soft-deleted        | reject            | SKYCRM-VAL-003 | Discount với gensapcode {0} đã bị xóa       |
      | delete    | valid   | not-exist        | any                 | noop-or-reject    | SKYCRM-NF-002  | Discount group gensapcode {0} không tồn tại |
      | delete    | valid   | soft-deleted     | non-deleted         | noop              | SKYCRM-VAL-001 | Discount group gensapcode {0} đã bị xóa     |
      | delete    | valid   | non-deleted      | non-deleted         | allow-soft-delete | none           | Thành công                                  |
      | delete    | valid   | non-deleted      | soft-deleted        | noop              | SKYCRM-VAL-003 | Discount với gensapcode {0} đã bị xóa       |
      | delete    | valid   | non-deleted      | not-exist           | noop-or-reject    | SKYCRM-NF-003  | Discount với gensapcode {0} không tồn tại   |

  Scenario Outline: 2.2 - Validation nghiệp vụ chuyên biệt tại SkyCRM cho Order Discount
    Given Một request Promotion loại "ORDER_DISCOUNT" gửi sang SkyCRM
    When SkyCRM thực hiện kiểm tra logic giá trị cho trường <trường dữ liệu>
    Then SkyCRM từ chối xử lý với mã lỗi <mã lỗi> và thông báo "<thông báo>"

    Examples: 
      | trường dữ liệu                      | mã lỗi         | thông báo                                                                    |
      | ----------------------------------- | -------------- | ---------------------------------------------------------------------------- |
      | ValidationValueType                 | SKYCRM-VAL-004 | ApplicableValueType không được rỗng                                          |
      | ValidationPercentRange              | SKYCRM-VAL-005 | ApplicableValuePercent phải nằm trong khoảng 0-100                           |
	  | ValidationPercentValue              | SKYCRM-VAL-006 | ApplicableValueType = PERCENT bắt buộc khi applicableValuePercent có giá trị |
	  | ValidationAmountValue               | SKYCRM-VAL-007 | ApplicableValueType = AMOUNT bắt buộc khi applicableValueAmount có giá trị   |
	  | ValidationApplicableProduct         | SKYCRM-VAL-011 | ApplicableProduct không được rỗng                                            |
	  | ValidationApplicableConditionType   | SKYCRM-VAL-012 | ApplicableConditionType không được rỗng                                      |
	  | ValidationIsCombinedOrderDiscount   | SKYCRM-VAL-013 | IsCombinedOrderDiscount không được rỗng                                      |
	  | ValidationIsCombinedProductDiscount | SKYCRM-VAL-014 | IsCombinedProductDiscount không được rỗng                                    |

  # TẦNG 3: XỬ LÝ NGẦM (BACKGROUND SYNC) XUỐNG RK7 & REFAGENT
  # Mục tiêu: SC tự động đẩy dữ liệu xuống downstream, hỗ trợ retry, không block Ecom
  Scenario Outline: Giám sát thực thi Background Job và cơ chế Retry xuống RK7/Refagent
    Given SkyCRM đã chốt quyết định thành công (Ecom đã nhận kết quả 200)
    And SkyCRM bắt đầu tạo Background Job đẩy dữ liệu xuống <hệ thống đích> (tại cấu hình kết nối SkyCRM)
    When Quá trình thực thi ngầm xảy ra lỗi
    Then Hệ thống thực hiện ghi nhận log với Mã lỗi <mã lỗi> và thông báo "<thông báo lỗi>"
    And Kích hoạt cơ chế Retry tự động (áp dụng với Refagent tùy cấu hình 3-5 lần)

    Examples:
      | hệ thống đích | mã lỗi           | thông báo lỗi                                 |
      | ------------- | ---------------- | --------------------------------------------- |
      | RK7           | none             | không kết nối được rk7 lỗi: {ex.Message}      |
      | RK7           | none             | RK7 lỗi xảy ra khi SaveDiscount: {ex.Message} |
      | Refagent      | REFAGENT-VAL-001 | payload không được rỗng                       |
      | Refagent      | REFAGENT-VAL-002 | DiscountItem không được rỗng                  |
      | Refagent      | REFAGENT-VAL-003 | DiscountTypeItem không được rỗng              |
      | Refagent      | REFAGENT-NF-001  | không tạo được SetRefDataJob {0}              |
      | Refagent      | REFAGENT-VAL-004 | actName không được hỗ trợ {0}                 |
      | Refagent      | REFAGENT-VAL-005 | tham số request không hợp lệ {0}              |
      | Refagent      | REFAGENT-SYS-001 | queue đầy, không thể enqueue job {0}          |
      | Refagent      | REFAGENT-SYS-002 | lỗi xử lý SetRefData {0}                      |
      | Refagent      | REFAGENT-VAL-006 | Discount group gensapcode {0} đã bị xóa       |
      | Refagent      | REFAGENT-NF-002  | Discount group gensapcode {0} không tồn tại   |
      | Refagent      | REFAGENT-VAL-007 | Discount với gensapcode {0} đã tồn tại        |
      | Refagent      | REFAGENT-VAL-008 | Discount với gensapcode {0} đã bị xóa         |
      | Refagent      | REFAGENT-NF-003  | Discount với gensapcode {0} không tồn tại     |
```
### test matrix (coverage spec) order discount

| id   | case                  | condition                                   | expected                                              |
| ---- | --------------------- | ------------------------------------------- | ----------------------------------------------------- |
| TC01 | hợp lệ                | đầy đủ fields & đúng cấu hình               | success (accept)                                      |
| TC02 | name rỗng             | name = null/empty                           | reject: name không được rỗng                          |
| TC03 | code rỗng             | code = null/empty                           | reject: code không được rỗng                          |
| TC04 | status rỗng           | status = null/empty                         | reject: status không được rỗng                        |
| TC05 | promotionType rỗng    | promotionType = null/empty                  | reject: promotionType không được rỗng                 |
| TC06 | tenantId rỗng         | tenantId = null                             | reject: tenantId không được rỗng                      |
| TC07 | eventType rỗng        | eventType = null                            | reject: eventType không được rỗng                     |
| TC08 | storesSelection rỗng  | storesSelection = null                      | reject: storesSelection không được rỗng               |
| TC09 | sai thời gian         | startTime >= endTime                        | reject: startTime phải nhỏ hơn endTime                |
| TC10 | thiếu orgId           | master data orgId chưa khai báo             | reject: masterDataOrganizationId chưa được khai báo   |
| TC11 | thiếu grName          | crm discount group name chưa khai báo       | reject: skyCRMApiDiscountGroupName chưa được khai báo |
| TC12 | thiếu grCode          | crm discount group code chưa khai báo       | reject: skyCRMApiDiscountGroupCode chưa được khai báo |
| TC13 | lỗi hệ thống          | exception runtime                           | system error                                          |
| TC14 | conditionType rỗng*   | applicableConditionType = null              | reject: applicableConditionType là bắt buộc           |
| TC15 | products rỗng*        | productsSelection = null                    | reject: productsSelection là bắt buộc                 |
| TC16 | combine product rỗng* | isCombinedProductDiscount = null            | reject: isCombinedProductDiscount là bắt buộc         |
| TC17 | combine order rỗng*   | isCombinedOrderDiscount = null              | reject: isCombinedOrderDiscount là bắt buộc           |
| TC18 | chung                 | groupId invalid                             | reject: OrganizationId không tồn tại                  |
| TC19 | create                | group: not-exist / discount: not-exist      | reject: Discount group không tồn tại                  |
| TC20 | create                | group: non-deleted / discount: not-exist    | success: Thành công (allow bootstrap)                 |
| TC21 | create                | group: non-deleted / discount: non-deleted  | reject: Discount đã tồn tại                           |
| TC22 | create                | group: non-deleted / discount: soft-deleted | reject: Discount đã bị xóa                            |
| TC23 | create                | group: soft-deleted / discount: not-exist   | reject: Discount group đã bị xóa                      |
| TC24 | update                | group: not-exist / discount: any            | reject: Discount group không tồn tại                  |
| TC25 | update                | group: soft-deleted / discount: non-deleted | reject: Discount group đã bị xóa                      |
| TC26 | update                | group: non-deleted / discount: non-deleted  | success: Thành công                                   |
| TC27 | update                | group: non-deleted / discount: not-exist    | reject: Discount không tồn tại                        |
| TC28 | update                | group: non-deleted / discount: soft-deleted | reject: Discount đã bị xóa                            |
| TC29 | delete                | group: not-exist / discount: any            | noop-or-reject: Discount group không tồn tại          |
| TC30 | delete                | group: soft-deleted / discount: non-deleted | noop: Discount group đã bị xóa                        |
| TC31 | delete                | group: non-deleted / discount: non-deleted  | success: Thành công (allow soft delete)               |
| TC32 | delete                | group: non-deleted / discount: soft-deleted | noop: Thành công (đã xóa trước đó)                    |
| TC33 | delete                | group: non-deleted / discount: not-exist    | noop-or-reject: Discount không tồn tại                |
## tham khảo
- tài liệu bdd order discount hiện tại ![[ecom-promotion-order.docx]]
- tài liệu mã lỗi ![[error-codes.xlsx]]