# promotion engine – trách nhiệm & xử lý sự cố (20/80)

## 1. promotion engine cần làm gì? (trách nhiệm cốt lõi)

**promotion engine là decision service**, nhiệm vụ duy nhất là **ra quyết định khuyến mãi tại thời điểm checkout**.

### promotion engine phải làm

* nhận **billcontext** (snapshot dữ liệu)
* đánh giá điều kiện promotion
* tính **discount / gift**
* trả **kết quả quyết định**
* ghi **log decision** để truy vết

### promotion engine không được làm

* không lưu bill
* không sync dữ liệu
* không quản lý workflow
* không retry nghiệp vụ
* không ảnh hưởng thanh toán

> nguyên tắc: **context vào → decision ra → kết thúc**

---

## 2. giao thức pos ↔ promotion engine & xử lý khi lỗi

### giao thức sử dụng

* **api đồng bộ (http hoặc grpc)**
* pos **chờ kết quả ngay** để hiển thị giá cho người dùng

### thời điểm gọi

```
user tạo/chỉnh bill
→ pos build billcontext
→ gọi promotion engine
→ nhận kết quả
→ hiển thị giá
```

---

## 3. nếu gọi promotion engine thất bại thì sao?

### nguyên tắc sống còn

> **promotion engine lỗi → pos vẫn bán hàng bình thường**

### cách xử lý đúng

* timeout / 5xx / network lỗi → **bỏ promotion**
* pos fallback về **giá gốc**
* không block checkout
* không retry nghiệp vụ tại pos

promotion engine chỉ cần trả:

```json
{ "status": "failed", "reason": "timeout" }
```

---

## 4. có nên đặt promotion engine chung với sync service?

**không nên.**

### lý do

* promotion engine: realtime, low latency, user-facing
* sync service: background, retry, stateful

trộn chung sẽ:

* gây nghẽn checkout
* khó kiểm soát lỗi
* rủi ro lan sự cố

nếu buộc chung codebase:

* tách module
* tách thread pool
* tách sla

---

## 5. checklist 20/80 cần quan tâm khi triển khai

* api đồng bộ
* timeout < 300ms
* pos có fallback
* engine stateless
* log có bill_id
* không retry nghiệp vụ

---

## 6. 1 dòng kết luận

> promotion engine chỉ chịu trách nhiệm **tính khuyến mãi**, nếu lỗi thì **pos bán giá gốc**, hệ thống không được dừng.

