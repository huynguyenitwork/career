# tài liệu chuẩn hoá mã lỗi api toàn hệ thống

mục tiêu của tài liệu này:

- thống nhất cách định nghĩa và sử dụng mã lỗi cho toàn bộ microservice
- giúp dev đọc log → hiểu ngay lỗi nằm ở domain nào, loại lỗi gì
- giúp hệ thống monitoring / alert hoạt động ổn định khi hệ thống mở rộng

tài liệu này dùng cho: platform, order, store, payment, pos, notification, user và các service mới sau này.

---

# quy ước mã lỗi

định dạng chuẩn:

```
{domain}-{category}-{number}
```

ví dụ:

```
ord-nf-001
```

ý nghĩa:

- domain → service phát sinh lỗi
- category → loại lỗi chuẩn của hệ thống
- number → id lỗi, không thay đổi sau khi public api

nguyên tắc:

- không sửa error code sau khi release
- mỗi error code chỉ có 1 meaning
- chỉ thêm code mới, không tái sử dụng
- http status phải theo category chuẩn

---

# bảng khung mã lỗi chuẩn toàn hệ thống

bảng dưới đây là **bảng gốc dùng cho toàn bộ service**.

| domain (cha)               | category (con) | http status | retry | quy tắc dùng                                    | ví dụ error code    |
| -------------------------- | -------------- | ----------- | ----- | ----------------------------------------------- | ------------------- |
| sys (platform / infra)     | val            | 400         | no    | request sai ở layer gateway / shared validation | sys-val-001         |
| sys (platform / infra)     | auth           | 401 / 403   | no    | lỗi auth platform / token / permission          | sys-auth-001        |
| sys (platform / infra)     | rate           | 429         | yes   | rate limit toàn hệ thống                        | sys-rate-001        |
| sys (platform / infra)     | dep            | 503         | yes   | database / redis / kafka / external infra down  | sys-dep-001         |
| sys (platform / infra)     | integ          | 502         | yes   | lỗi giao tiếp giữa service (contract / mapping) | sys-integ-001       |
| sys (platform / infra)     | timeout        | 504         | yes   | downstream timeout ở infra layer                | sys-timeout-001     |
| sys (platform / infra)     | unavailable    | 503         | yes   | platform đang bảo trì / degrade                 | sys-unavailable-001 |
| sys (platform / infra)     | sys            | 500         | no    | lỗi hệ thống chưa phân loại                     | sys-sys-001         |
| ord (order service)        | val            | 400         | no    | request tạo / update order sai rule             | ord-val-001         |
| ord (order service)        | nf             | 404         | no    | order không tồn tại                             | ord-nf-001          |
| ord (order service)        | cfl            | 409         | no    | state order không hợp lệ                        | ord-cfl-001         |
| ord (order service)        | dep            | 503         | yes   | agent / service phụ thuộc không hoạt động       | ord-dep-001         |
| ord (order service)        | timeout        | 504         | yes   | gọi service khác khi xử lý order bị timeout     | ord-timeout-001     |
| ord (order service)        | sys            | 500         | no    | lỗi logic nội bộ order                          | ord-sys-001         |
| sto (store service)        | val            | 400         | no    | request store invalid                           | sto-val-001         |
| sto (store service)        | nf             | 404         | no    | store không tồn tại                             | sto-nf-001          |
| sto (store service)        | cfl            | 409         | no    | store đóng / channel disabled                   | sto-cfl-001         |
| sto (store service)        | dep            | 503         | yes   | dependency liên quan store lỗi                  | sto-dep-001         |
| sto (store service)        | sys            | 500         | no    | lỗi nội bộ store service                        | sto-sys-001         |
| pay (payment service)      | val            | 400         | no    | payment request sai                             | pay-val-001         |
| pay (payment service)      | nf             | 404         | no    | payment record không tồn tại                    | pay-nf-001          |
| pay (payment service)      | dep            | 503         | yes   | payment gateway down                            | pay-dep-001         |
| pay (payment service)      | timeout        | 504         | yes   | timeout khi gọi payment provider                | pay-timeout-001     |
| pay (payment service)      | sys            | 500         | no    | lỗi nội bộ payment                              | pay-sys-001         |
| pos (pos / agent gateway)  | nf             | 404         | no    | agent / pos không tồn tại                       | pos-nf-001          |
| pos (pos / agent gateway)  | dep            | 503         | yes   | agent offline                                   | pos-dep-001         |
| pos (pos / agent gateway)  | timeout        | 504         | yes   | timeout khi gọi pos                             | pos-timeout-001     |
| pos (pos / agent gateway)  | sys            | 500         | no    | lỗi xử lý pos                                   | pos-sys-001         |
| usr (user service)         | val            | 400         | no    | dữ liệu user sai                                | usr-val-001         |
| usr (user service)         | nf             | 404         | no    | user không tồn tại                              | usr-nf-001          |
| usr (user service)         | auth           | 401 / 403   | no    | user không có quyền                             | usr-auth-001        |
| usr (user service)         | sys            | 500         | no    | lỗi nội bộ user service                         | usr-sys-001         |
| ntf (notification service) | val            | 400         | no    | payload gửi notification sai                    | ntf-val-001         |
| ntf (notification service) | dep            | 503         | yes   | provider gửi notification lỗi                   | ntf-dep-001         |
| ntf (notification service) | timeout        | 504         | yes   | timeout gửi notification                        | ntf-timeout-001     |
| ntf (notification service) | sys            | 500         | no    | lỗi nội bộ notification                         | ntf-sys-001         |

---

# mapping category → hành vi xử lý

bảng này giúp dev quyết định nhanh khi đọc log.

| category | tên chuẩn dùng hệ thống lớn    | ý nghĩa                                                                | hành động              |
| -------- | ------------------------------ | ---------------------------------------------------------------------- | ---------------------- |
| val      | validation                     | lỗi dữ liệu request không hợp lệ (schema / rule / business validation) | sửa request            |
| nf       | not_found                      | resource hoặc entity không tồn tại                                     | kiểm tra data          |
| cfl      | conflict                       | trạng thái business không hợp lệ tại thời điểm thực hiện               | kiểm tra business flow |
| dep      | dependency_failure             | service phụ thuộc hoặc hạ tầng liên quan bị lỗi / không hoạt động      | retry                  |
| timeout  | request_timeout                | request gọi service khác vượt quá thời gian chờ                        | retry + monitor        |
| integ    | integration_failure            | lỗi giao tiếp giữa các service (contract / mapping / message format)   | kiểm tra contract      |
| rate     | rate_limited                   | vượt giới hạn request / throttle                                       | retry sau              |
| auth     | authentication / authorization | chưa xác thực hoặc không đủ quyền                                      | kiểm tra auth          |
| sys      | internal_error                 | lỗi nội bộ chưa phân loại hoặc bug trong service                       | check log / alert      |

---

# quy tắc bắt buộc khi phát triển

mọi service mới phải tuân theo:

1. đăng ký domain trước khi release service
2. mọi lỗi phải khai báo trong error registry
3. không hardcode http error trong controller
4. throw exception chuẩn của hệ thống
5. log theo error code

---

# ví dụ response chuẩn

response api khi lỗi nên theo format sau:

```json
{
  "error": {
    "code": "ord-nf-001",
    "category": "not_found",
    "httpStatus": 404,
    "retryable": false,
    "message": "order not found",
    "traceId": "trace-id-from-system"
  }
}
```

---

# cách mở rộng hệ thống sau này

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

# kết luận

khung này giúp hệ thống:

- scale lên nhiều microservice mà không lo trùng mã lỗi
- debug production nhanh hơn
- alert chính xác theo loại lỗi
- dev mới đọc log hiểu ngay hệ thống

trong thực tế, khi hệ thống lớn hơn nữa, bước tiếp theo nên làm là:

- tự động generate error catalog từ code
- sync error code vào monitoring system
- thống kê top error theo domain

đó là cách các hệ thống lớn giữ error system luôn sạch và dễ vận hành.
