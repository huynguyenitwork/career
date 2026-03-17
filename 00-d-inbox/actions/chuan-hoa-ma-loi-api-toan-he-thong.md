# tài liệu chuẩn hoá mã lỗi api toàn hệ thống (phiên bản hoàn chỉnh)

mục tiêu của tài liệu này:

- thống nhất cách định nghĩa và sử dụng mã lỗi cho toàn bộ microservice
- giúp dev đọc log → hiểu ngay lỗi nằm ở service nào và ở layer nào
- giúp monitoring / alert phân biệt lỗi api, business logic và background job
- đảm bảo hệ thống mở rộng nhiều service mà không lo trùng mã lỗi

tài liệu áp dụng cho tất cả service: platform, order, store, payment, pos, notification, user và các service mới sau này.

---

# 1. quy ước mã lỗi

định dạng chuẩn:

```
{domain}-{category}-{number}
```

ví dụ:

```
ord-nf-001
```

ý nghĩa:

- **domain** → service phát sinh lỗi
- **category** → loại lỗi chuẩn của hệ thống
- **number** → id lỗi

nguyên tắc:

- không sửa error code sau khi public api
- mỗi error code chỉ có một meaning
- chỉ thêm code mới, không tái sử dụng
- http status phải theo category chuẩn

---

# 2. runtime layer của lỗi

mỗi lỗi phải xác định **layer phát sinh trong runtime**.

| layer      | ý nghĩa                               |
| ---------- | ------------------------------------- |
| controller | lỗi khi nhận request api              |
| service    | lỗi logic nghiệp vụ khi xử lý request |
| worker     | lỗi background service / async job    |

---

## controller

lỗi xảy ra khi:

- request schema sai
- thiếu parameter
- auth fail
- rate limit

ví dụ:

```
ord-val-001
sys-auth-001
sys-rate-001
```

---

## service

lỗi xảy ra khi:

- business rule fail
- entity không tồn tại
- domain state conflict
- synchronous integration fail

ví dụ:

```
ord-nf-001
ord-cfl-001
pay-sys-001
```

---

## worker (background service)

lỗi xảy ra khi:

- queue job fail
- retry job fail
- external integration fail
- scheduled job fail
- webhook delivery fail

ví dụ:

```
pay-dep-001
ntf-timeout-001
ntf-sys-001
```

---

# 3. bảng category chuẩn toàn hệ thống

| category | tên chuẩn                      | ý nghĩa                          | subtype điển hình                                          |
| -------- | ------------------------------ | -------------------------------- | ---------------------------------------------------------- |
| val      | validation                     | request không hợp lệ             | required, format, range, enum, length, conditional, schema |
| nf       | not_found                      | resource / config không tồn tại  | resource_missing, config_missing                           |
| cfl      | conflict                       | trạng thái business không hợp lệ | state_conflict, duplicate, already_exists                  |
| dep      | dependency_failure             | service phụ thuộc lỗi            | downstream_error, service_unavailable                      |
| timeout  | request_timeout                | downstream timeout               | gateway_timeout, service_timeout                           |
| integ    | integration_failure            | lỗi contract / mapping           | payload_mapping, contract_mismatch                         |
| rate     | rate_limited                   | vượt giới hạn request            | throttled, quota_exceeded                                  |
| auth     | authentication / authorization | lỗi xác thực hoặc quyền          | token_invalid, permission_denied                           |
| sys      | internal_error                 | lỗi nội bộ hệ thống              | null_reference, unexpected_exception                       |

---

# 4. bảng khung mã lỗi chuẩn toàn hệ thống

## bảng khung mã lỗi

| domain | category    | layer      | http status | retry | quy tắc dùng                 |
| ------ | ----------- | ---------- | ----------- | ----- | ---------------------------- |
| sys    | val         | controller | 400         | no    | request schema sai           |
| sys    | auth        | controller | 401 / 403   | no    | token / permission lỗi       |
| sys    | rate        | controller | 429         | yes   | rate limit                   |
| sys    | dep         | service    | 503         | yes   | dependency lỗi               |
| sys    | integ       | service    | 502         | yes   | service contract lỗi         |
| sys    | timeout     | service    | 504         | yes   | downstream timeout           |
| sys    | unavailable | service    | 503         | yes   | platform degrade             |
| sys    | sys         | service    | 500         | no    | lỗi nội bộ                   |
| ord    | val         | controller | 400         | no    | request order sai            |
| ord    | nf          | service    | 404         | no    | order không tồn tại          |
| ord    | cfl         | service    | 409         | no    | order state conflict         |
| ord    | dep         | service    | 503         | yes   | dependency order lỗi         |
| ord    | timeout     | service    | 504         | yes   | order timeout                |
| ord    | sys         | service    | 500         | no    | lỗi nội bộ order             |
| sto    | val         | controller | 400         | no    | request store sai            |
| sto    | nf          | service    | 404         | no    | store không tồn tại          |
| sto    | cfl         | service    | 409         | no    | store disabled               |
| sto    | dep         | service    | 503         | yes   | dependency store lỗi         |
| sto    | sys         | service    | 500         | no    | lỗi nội bộ store             |
| pay    | val         | controller | 400         | no    | request payment sai          |
| pay    | nf          | service    | 404         | no    | payment record không tồn tại |
| pay    | dep         | worker     | 503         | yes   | payment gateway lỗi          |
| pay    | timeout     | worker     | 504         | yes   | gateway timeout              |
| pay    | sys         | service    | 500         | no    | lỗi nội bộ payment           |
| pos    | nf          | service    | 404         | no    | pos không tồn tại            |
| pos    | dep         | worker     | 503         | yes   | pos offline                  |
| pos    | timeout     | worker     | 504         | yes   | timeout gọi pos              |
| pos    | sys         | service    | 500         | no    | lỗi nội bộ pos               |
| usr    | val         | controller | 400         | no    | request user sai             |
| usr    | nf          | service    | 404         | no    | user không tồn tại           |
| usr    | auth        | controller | 401 / 403   | no    | user không đủ quyền          |
| usr    | sys         | service    | 500         | no    | lỗi nội bộ user              |
| ntf    | val         | controller | 400         | no    | payload notification sai     |
| ntf    | dep         | worker     | 503         | yes   | provider notification lỗi    |
| ntf    | timeout     | worker     | 504         | yes   | gửi notification timeout     |
| ntf    | sys         | worker     | 500         | no    | worker lỗi                   |

## bảng viết tắt domain (service code)
| domain | service              | ý nghĩa                             |
| ------ | -------------------- | ----------------------------------- |
| sys    | platform / system    | lỗi chung của platform hoặc hạ tầng |
| ord    | order service        | xử lý đơn hàng                      |
| sto    | store service        | quản lý cửa hàng                    |
| pay    | payment service      | xử lý thanh toán                    |
| pos    | pos / agent gateway  | giao tiếp với pos hoặc agent        |
| usr    | user service         | quản lý user / account              |
| ntf    | notification service | gửi notification (sms, email, push) |

---

# 5. mapping category → layer

| category | layer mặc định   |
| -------- | ---------------- |
| val      | controller       |
| auth     | controller       |
| rate     | controller       |
| nf       | service          |
| cfl      | service          |
| integ    | service          |
| dep      | service / worker |
| timeout  | service / worker |
| sys      | service / worker |

---

# 6. response api chuẩn

response lỗi api:

```json
{
  "error": {
    "code": "ord-nf-001",
    "layer": "service",
    "category": "not_found",
    "httpStatus": 404,
    "retryable": false,
    "message": "order not found",
    "traceId": "trace-id-from-system"
  }
}
```

---

# 7. quy tắc bắt buộc khi phát triển

mọi service mới phải:

1. đăng ký domain trước khi release
2. khai báo error code trong error registry
3. không hardcode http error trong controller
4. throw exception chuẩn của hệ thống
5. log theo error code
6. khai báo **runtime layer của lỗi**

---

# 8. mở rộng hệ thống sau này

khi thêm service mới:

bước 1 — đăng ký domain

```
dlv → delivery service
```

bước 2 — dùng category chuẩn

```
dlv-nf-001
dlv-dep-001
```

không tạo category mới nếu không thật sự cần.

---

# 9. lợi ích của chuẩn này

chuẩn này giúp hệ thống:

- scale lên nhiều microservice mà không lo trùng mã lỗi
- dev debug production nhanh
- monitoring phân biệt lỗi api / business / worker
- alert chính xác theo loại lỗi

---

# 11. các trường hợp validation

## bảng phân loại validation

### tổng quát

| nhóm kiểm tra             | mô tả                          | ví dụ                        | layer      | http code |
| ------------------------- | ------------------------------ | ---------------------------- | ---------- | --------- |
| field existence           | field có tồn tại trong request | thiếu `email`                | controller | 400       |
| type validation           | kiểu dữ liệu đúng              | `age` phải là number         | controller | 400       |
| format validation         | format hợp lệ                  | email/url/uuid               | controller | 400       |
| length validation         | độ dài hợp lệ                  | name max 255                 | controller | 400       |
| enum validation           | giá trị nằm trong enum         | `status ∈ {active,inactive}` | controller | 400       |
| range validation (schema) | range cơ bản                   | `page >= 0`                  | controller | 400       |
| authentication            | xác thực request               | api key/token sai            | controller | 401       |
| authorization             | kiểm tra quyền                 | user không có role           | controller | 403       |
| rate limit                | quá số request                 | quá 100 req/min              | controller | 429       |
| idempotency               | request bị lặp                 | duplicate request id         | controller | 409       |
| resource existence        | resource tồn tại               | userId không tồn tại         | service    | 404       |
| business rule             | logic nghiệp vụ                | `% > 100`                    | service    | 422       |
| cross-field validation    | rule phụ thuộc nhiều field     | type=`%` cần percent         | service    | 422       |
| domain constraint         | giới hạn domain                | balance không đủ             | service    | 422       |
| state validation          | trạng thái hợp lệ              | order đã cancel              | service    | 409       |
| uniqueness                | unique trong domain            | email đã tồn tại             | service    | 409       |
| workflow constraint       | bước workflow sai              | approve khi chưa submit      | service    | 409       |
| integration validation    | dữ liệu từ hệ khác             | bank account invalid         | service    | 422       |
| external service fail     | service ngoài lỗi              | payment gateway fail         | background | 502       |
| external timeout          | api ngoài timeout              | bank timeout                 | background | 504       |
| async processing fail     | job async lỗi                  | queue job fail               | background | 500       |
| retry exceeded            | retry quá limit                | retry job quá 5 lần          | background | 500       |
| system error              | lỗi hệ thống                   | null pointer                 | system     | 500       |

### tóm tắt

| nhóm               | kiểm tra                          | layer      | http      |
| ------------------ | --------------------------------- | ---------- | --------- |
| request shape      | field, type, format, length, enum | controller | 400       |
| access control     | auth, permission                  | controller | 401 / 403 |
| request protection | rate limit, idempotency           | controller | 429 / 409 |
| resource existence | resource tồn tại                  | service    | 404       |
| business rule      | logic nghiệp vụ                   | service    | 422       |
| state conflict     | trạng thái domain sai             | service    | 409       |
| async integration  | external api fail / timeout       | background | 502 / 504 |
| system error       | bug / crash                       | system     | 500       |

---

# bảng rule nhanh (decision rule)

| câu hỏi                      | nếu yes | layer      | http code   |
| ---------------------------- | ------- | ---------- | ----------- |
| request parse được không     | không   | controller | 400         |
| user đã xác thực chưa        | chưa    | controller | 401         |
| user có quyền không          | không   | controller | 403         |
| request quá giới hạn         | có      | controller | 429         |
| resource tồn tại không       | không   | service    | 404         |
| logic nghiệp vụ hợp lệ không | không   | service    | 422         |
| state domain hợp lệ không    | không   | service    | 409         |
| xử lý async thất bại         | có      | background | 500/502/504 |

---

# rule layer tổng quát

| layer             | trách nhiệm                    |
| ----------------- | ------------------------------ |
| controller        | request validation + security  |
| service           | business logic + domain rule   |
| background worker | async processing + integration |

---

# pipeline chuẩn của hệ thống

```
client
 ↓
controller
  schema validation
  auth
 ↓
service
  business rule
  domain state
 ↓
event / queue
 ↓
background worker
  integration
  retry
```

---

# rule phân biệt nhanh schema vs business

| đặc điểm                     | schema | business |
| ---------------------------- | ------ | -------- |
| kiểm tra từng field riêng lẻ | ✓      |          |
| kiểm tra format/type         | ✓      |          |
| phụ thuộc nhiều field        |        | ✓        |
| phụ thuộc domain             |        | ✓        |
| phụ thuộc state hệ thống     |        | ✓        |

---

# rule 1 dòng để nhớ

```
controller → request hợp lệ
service → nghiệp vụ hợp lệ
worker → xử lý async
```

