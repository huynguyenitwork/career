## encode query string trong .net core 2.1 – lỗi thường gặp

### vấn đề

khi build url thủ công cho rest api, nếu query param chứa:

* dấu cách
* tiếng việt
* ký tự đặc biệt (`| & ? + %`)

nếu encode sai chuẩn → server hiểu sai, filter lệch, hoặc trả 400 khó debug.

---

### hai kiểu encode khác nhau (rất dễ nhầm)

#### 1. webutility.urlencode (form encoding)

* chuẩn: `application/x-www-form-urlencoded`
* dấu cách `" "` → `+`

ví dụ:

```
"MH | QSR"
→ MH+%7C+QSR
```

phù hợp:

* html form submit
* body dạng form

không phù hợp:

* rest api
* build url thủ công

---

#### 2. uri.escapedatastring (uri encoding)

* chuẩn: rfc 3986
* dấu cách `" "` → `%20`

ví dụ:

```
"MH | QSR"
→ MH%20%7C%20QSR
```

phù hợp:

* query string cho rest api
* url viết tay
* search/filter param

---

### lựa chọn đúng cho .net core 2.1

* encode query param cho api
  → **uri.escapedatastring**
* encode dữ liệu form
  → **webutility.urlencode**

---

### cách dùng khuyến nghị

```csharp
var encodedValue = Uri.EscapeDataString(value);
var url = $"api/resource?search={encodedValue}&limit=1";
```

---

### nguyên tắc an toàn

* chỉ encode **giá trị param**, không encode toàn bộ url
* không encode hai lần
* thấy dấu `+` trong query string api → kiểm tra lại encode

---

### câu chốt

> rest api cần `%20`, không cần `+`.
> form là form, url là url.

---
