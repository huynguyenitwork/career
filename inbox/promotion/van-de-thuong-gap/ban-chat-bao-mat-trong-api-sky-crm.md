## tài liệu ngắn: bản chất bảo mật trong api này

### 1. api đang dùng kiểu bảo mật gì?

api sử dụng **jwt bearer authentication** theo chuẩn **oauth2 / openid connect**.

dấu hiệu:

* Có `UseAuthentication()` + `UseAuthorization()`
* client gửi header:

  ```
  Authorization: Bearer <token>
  ```
* token có cấu trúc `header.payload.signature`
* ký bằng **RS256** (RSA)

identity provider: **Keycloak**.

---

### 2. token gửi lên là gì?

token bạn gửi là:

> **access token**
> **định dạng: JWT**

hai khái niệm khác tầng:

* *Access token* → nói về **vai trò** (dùng để gọi API)
* *JWT* → nói về **hình thức đóng gói**

không mâu thuẫn, là cùng một thứ.

---

### 3. token này không phải là gì?

* không phải api key
* không phải username/password
* không phải token mã hoá (không decrypt được)

jwt **chỉ ký, không mã hoá** → ai cũng decode được payload.

---

### 4. credential cần dùng khi gọi api

**chỉ cần access token hợp lệ**.

không gửi:

* username
* password
* client secret

user/pass **chỉ dùng lúc login với idp**, không bao giờ dùng ở api layer.

---

### 5. api xử lý request thế nào?

Luồng chuẩn:

1. `UseAuthentication()`

   * Đọc Bearer token
   * Verify chữ ký, hạn dùng, issuer
   * Gắn `HttpContext.User`

2. `UseAuthorization()`

   * kiểm tra `[Authorize]`, role, policy
   * cho qua hoặc chặn (401 / 403)

endpoint có `[Authorize]` → **bắt buộc có token**
endpoint không có → public.

---

## tình huống áp dụng thực tế

**tình huống:**
client gửi request kèm:

```
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

**kết quả:**

* api xác thực token (JWT Bearer)
* không hỏi lại user/pass
* phân quyền dựa trên role trong token
* token hợp lệ → xử lý
* token sai / hết hạn → 401 hoặc 403

---

## token được sinh ra bằng cách nào? (auth flow)

### flow chuẩn (đơn giản hoá cho dev)

```
[user] 
  ↓ login
[keycloak]
  ↓ cấp
[access token (jwt)]
  ↓ gửi bearer
[asp.net api]
```

chi tiết hơn:

1. user login (ui / postman / tool nội bộ)
2. keycloak xác thực user
3. keycloak phát **access token (JWT)**
4. client gọi api với:

   ```
   Authorization: Bearer <access_token>
   ```

**api không biết user/pass.**
**api chỉ biết token.**

### sơ đồ auth flow 1 trang (cho team)

```
User
 └─ login
    └─ Keycloak (Realm)
        ├─ xác thực user
        ├─ gán role
        └─ phát Access Token (JWT)
               ↓
Client / Frontend / Tool
 └─ gọi API
    └─ Authorization: Bearer <token>
           ↓
ASP.NET API
 ├─ UseAuthentication
 │   └─ verify chữ ký + exp + iss
 ├─ HttpContext.User
 └─ UseAuthorization
     └─ check [Authorize] / Role / Policy
```

---

### một câu chốt hạ

> api không tin mật khẩu.
> api chỉ tin **token đã được ký bởi Identity Provider**.

bước tiếp theo hợp lý nhất là:

* rà lại mapping role từ Keycloak → ASP.NET
* hoặc viết sơ đồ auth flow 1 trang cho team dùng chung

Ngắn – đúng – đủ để đi tiếp.
