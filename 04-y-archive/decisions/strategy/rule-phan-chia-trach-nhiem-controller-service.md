# rule phân chia trách nhiệm

#tag: #rule #service #controller #constraint

## câu hỏi
- nếu **ecom → gọi api của skytransfer** thì **validation phải chạy ở controller của skytransfer** vì validation là **request-time constraint** → phải fail ngay khi request tới?

---

## 1. controller (sync boundary)

- xử lý **mọi thứ cần quyết định ngay trong request**
- mục tiêu: **fail sớm + bảo vệ hệ thống**

**được phép**

- validate schema (type, required, format)
- auth / signature / api key
- idempotency check
- rate limit
- map request → dto
- gọi service
- trả http response

**không được phép**

- business logic
- xử lý dài
- gọi external service phức tạp
- retry logic

---

## 2. service (business orchestration)

- xử lý **logic của domain**

**được phép**

- business rule validation
- quyết định flow xử lý
- gọi repository
- gọi external service
- publish event / queue

**không được phép**

- xử lý http
- parse request
- auth logic

---

## 3. worker / background (async)

- xử lý **việc không cần kết quả ngay**

**được phép**

- task lâu (api timeout)
- queue/retry fail
- integration unstable
- notification
- settlement

**không được phép**

- validate input request
- auth

---

# rule quyết định sync vs async

- **sync**
  - client cần kết quả ngay
  - request quyết định flow tiếp theo

  ví dụ
  - create transfer request
  - verify token
  - check state

---

- **async**
  - client chỉ cần acknowledge
  - xử lý có thể chạy sau

  ví dụ
  - gọi bank gateway
  - gửi webhook
  - settlement

---

# flow đúng cho skytransfer

```
ecom
 ↓
skytransfer controller
   validate request
   auth
   idempotency
 ↓
service
   business rule
   create transfer
   publish event
 ↓
queue
 ↓
worker
   call bank
   update status
```

---

# rule kiểm tra kiến trúc

- request sai → **reject ngay tại controller**
- request hợp lệ → **mới vào service**
- worker **không bao giờ validate request**

---

# nguyên tắc tổng quát

- controller = **request gate**
- service = **business brain**
- worker = **async executor**