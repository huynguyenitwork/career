# kiến trúc xử lý promotion sync (skytransfer → skycrm → rk7)

## 1. mục tiêu hệ thống

- nhận dữ liệu khuyến mại từ `skytransfer`
- validate dữ liệu nhiều lớp
- chuẩn hóa thành domain promotion
- convert sang format `rk7`
- chọn route sync (`direct` hoặc `refagent`)
- thực thi sync qua background job
- đảm bảo mở rộng dễ khi thêm loại promotion hoặc rule

toàn bộ flow được thiết kế bằng **pipeline + các design pattern tách trách nhiệm rõ ràng**

---

# 2. tổng quan flow hệ thống

```
skytransfer
   ↓
skycrm inbound api
   ↓
validation pipeline
   ↓
domain resolve pipeline
   ↓
integration pipeline
   ↓
enqueue promotion sync job
   ↓
background sync pipeline
   ↓
rk7
```

---

# 3. context object xuyên pipeline

mọi pipeline step đều thao tác trên một object chung:

```
PromotionContext
```

các field chính:

```
rawPayload
discountType
discountVariant
promotionDomain
rk7Payload
syncStrategy
validationErrors
```

vai trò:

- giữ state xuyên suốt pipeline
- tránh truyền nhiều object rời rạc
- giúp step chỉ tập trung vào logic của nó

---

# 4. design pattern sử dụng

| problem                 | pattern        | mục tiêu                           |
| ----------------------- | -------------- | ---------------------------------- |
| discount type creation  | factory method | tạo handler cho từng loại discount |
| discount rule variation | strategy       | xử lý các rule discount khác nhau  |
| payload mapping         | adapter        | convert domain model → rk7 xml     |
| sync route              | strategy       | chọn route sync                    |
| validation              | pipeline       | validate tuần tự và tách bước      |

---

# 5. pipeline layer 1 — inbound validation

mục tiêu: loại bỏ payload lỗi trước khi vào domain logic.

## các bước

```
schemaValidationStep
requiredFieldValidationStep
dataTypeValidationStep
promotionTimeValidationStep
discountTypeDetectionStep
discountVariantDetectionStep
businessRuleValidationStep
duplicatePromotionValidationStep
rk7ConstraintValidationStep
```

## giải thích

- `schemaValidationStep`
  kiểm tra cấu trúc json payload

- `requiredFieldValidationStep`
  đảm bảo các field bắt buộc tồn tại

- `dataTypeValidationStep`
  validate number, enum, datetime

- `promotionTimeValidationStep`
  kiểm tra logic thời gian

```
startTime < endTime
```

- `discountTypeDetectionStep`
  xác định loại discount trong 5 loại

- `discountVariantDetectionStep`
  xác định biến thể rule

- `businessRuleValidationStep`
  validate rule domain

ví dụ

```
discountPercent ≤ 100
```

- `duplicatePromotionValidationStep`
  tránh tạo promotion trùng

- `rk7ConstraintValidationStep`
  kiểm tra rule có tương thích rk7 không

pattern sử dụng:

```
pipeline pattern
```

---

# 6. pipeline layer 2 — domain resolve

mục tiêu: convert payload thành domain model chuẩn.

## các bước

```
discountFactoryStep
discountStrategyResolveStep
buildDomainPromotionStep
```

---

## discountFactoryStep

pattern:

```
factory method
```

flow:

```
discountType
   ↓
DiscountHandlerFactory
   ↓
IDiscountHandler
```

handlers:

```
OrderDiscountHandler
ItemDiscountHandler
ComboDiscountHandler
VoucherDiscountHandler
ConditionalDiscountHandler
```

mỗi handler xử lý logic riêng cho loại discount.

---

## discountStrategyResolveStep

pattern:

```
strategy
```

vì mỗi discount type có nhiều rule khác nhau.

strategies ví dụ:

```
PercentageDiscountStrategy
AmountDiscountStrategy
BuyXGetYStrategy
BundleDiscountStrategy
TimeLimitedDiscountStrategy
```

handler sẽ chọn strategy phù hợp.

---

## buildDomainPromotionStep

convert payload thành domain model:

```
PromotionDomainModel
```

domain model này được dùng xuyên suốt phần còn lại của hệ thống.

---

# 7. pipeline layer 3 — integration preparation

mục tiêu: chuẩn bị dữ liệu để sync rk7.

## các bước

```
rk7PayloadMappingStep
syncRouteResolveStep
enqueuePromotionSyncStep
```

---

## rk7PayloadMappingStep

pattern:

```
adapter
```

convert

```
PromotionDomain
   ↓
RK7PromotionXML
```

adapter interface:

```
IRK7PayloadAdapter
```

mục tiêu:

- tách domain model khỏi format rk7
- dễ thay đổi khi rk7 thay format

---

## syncRouteResolveStep

pattern:

```
strategy
```

các strategy:

```
DirectRK7SyncStrategy
RefAgentSyncStrategy
```

logic chọn route:

```
if refagent available
    use refagent
else
    direct rk7
```

---

## enqueuePromotionSyncStep

đưa job vào queue

```
PromotionSyncJob
```

job sẽ xử lý việc gọi rk7.

---

# 8. pipeline layer 4 — background sync

job pipeline chạy độc lập.

## các bước

```
rk7PayloadValidationStep
syncStrategyResolveStep
executePromotionSyncStep
fallbackDirectSyncStep
syncResultLoggingStep
```

---

## rk7PayloadValidationStep

validate payload lần cuối trước khi gọi external system.

---

## syncStrategyResolveStep

resolve lại route sync.

```
DirectRK7SyncStrategy
RefAgentSyncStrategy
```

---

## executePromotionSyncStep

gọi api

```
rk7 xml api
```

---

## fallbackDirectSyncStep

nếu

```
refagent queue fail
```

fallback:

```
direct rk7
```

---

## syncResultLoggingStep

log

```
success
failure
retry
```

---

# 9. pipeline contract

mọi step implement interface chung:

```
IPipelineStep<TContext>
```

method:

```
Execute(context, next)
```

flow thực thi:

```
Step1
  ↓
Step2
  ↓
Step3
```

pipeline runner build từ:

```
IEnumerable<IPipelineStep>
```

được inject tự động qua DI container.

---

# 10. cấu trúc thư mục

```
promotion

context
 └─ PromotionContext

pipeline
 ├─ IPipelineStep
 └─ PipelineRunner

validation
 ├─ SchemaValidationStep
 ├─ RequiredFieldValidationStep
 ├─ BusinessRuleValidationStep
 └─ RK7ConstraintValidationStep

domain
 ├─ DiscountHandlerFactory
 ├─ DiscountHandlers
 └─ DiscountStrategies

integration
 ├─ RK7PayloadAdapter
 ├─ SyncStrategies
 └─ EnqueuePromotionSyncStep

job
 ├─ ExecutePromotionSyncStep
 ├─ FallbackDirectSyncStep
 └─ SyncResultLoggingStep
```

---

# 11. flow hoàn chỉnh

```
skytransfer
   ↓
skycrm inbound api
   ↓
validation pipeline
   ↓
domain resolve pipeline
   ↓
integration pipeline
   ↓
enqueue job
   ↓
background sync pipeline
   ↓
rk7
```

---

# 12. quy mô pipeline thực tế

thường ổn định nhất:

```
validation pipeline ≈ 7–9 step
domain pipeline ≈ 3 step
integration pipeline ≈ 3 step
job pipeline ≈ 4 step
```

tổng:

```
~17 pipeline step
```

đây là quy mô bình thường cho hệ thống **promotion integration**.

---

# 13. lợi ích kiến trúc

mở rộng rất dễ:

- thêm loại discount
  → thêm handler

- thêm rule discount
  → thêm strategy

- thêm validation
  → thêm pipeline step

- thay đổi integration route
  → thêm strategy
