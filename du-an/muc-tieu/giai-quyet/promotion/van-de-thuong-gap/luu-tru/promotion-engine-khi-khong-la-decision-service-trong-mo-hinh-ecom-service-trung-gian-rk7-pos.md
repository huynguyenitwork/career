# promotion engine trong mô hình ecom → service trung gian → rk7 (pos)

## 1. promotion engine có phải là decision service không?

### giải thích

**không.**
trong mô hình này, **promotion engine không phải decision service**.

**decision cuối cùng (áp hay không, giảm bao nhiêu tiền)** nằm ở:

* rk7 / pos

**promotion engine chỉ là nơi:**

* chuẩn hoá
* kiểm tra hợp lệ
* truyền đạt luật khuyến mãi

> promotion engine không quyết định tiền,
> nó quyết định **luật nào được phép xuống pos**.

### kết luận
promotion engine
- nó là: a Promotion Orchestration / Validation / Translation Service
- nó KHÔNG PHẢI là: a Decision Service or Pricing Engine
---

## 2. vì sao không để promotion engine quyết định luôn discount?

vì **source of truth của bill là pos**.

nếu promotion engine:

* tự tính tiền
* tự quyết discount

→ sẽ xảy ra:

* lệch số tiền giữa pos và backend
* sai thuế / rounding
* không audit được tại cửa hàng

=> pos là nơi **chịu trách nhiệm kế toán**, nên **pos phải là nơi quyết định cuối**.

---

## 3. promotion engine tồn tại để làm gì nếu không quyết định?

promotion engine trong mô hình này đóng 4 vai trò chính:

### 3.1. phiên dịch giữa ecom và rk7

* ecom định nghĩa promotion theo tư duy marketing
* rk7 hiểu promotion theo tư duy pos

promotion engine:

* nhận promotion từ ecom
* map sang format rk7 hiểu được
* đảm bảo không “nói sai ngôn ngữ”

---

### 3.2. validation & guardrail

promotion engine kiểm tra:

* promotion còn hiệu lực không
* cấu hình có thiếu không
* loại discount này pos có support không

=> sai thì **chặn ở backend**,
=> không đẩy rủi ro xuống pos.

---

### 3.3. chuẩn hoá & quản lý version

promotion engine giúp:

* gắn version cho promotion
* trace được:

  * promotion này từ campaign nào
  * từ ecom hay channel nào
  * rollout lúc nào

pos không cần biết marketing nghĩ gì,
pos chỉ cần biết **discount code + luật hợp lệ**.

---

### 3.4. advisor khi pos gọi ngược để “tính toán”

khi pos gọi service trung gian:

* promotion engine **không trả tiền**
* promotion engine chỉ trả:

  * promotion nào eligible
  * điều kiện có thoả hay không
  * metadata cần thiết

pos:

* là nơi apply
* là nơi tính tiền thật
* là nơi xử lý rounding / tax / stacking

---

## 4. promotion engine có nên lưu logic tính tiền không?

**không nên.**

promotion engine có thể:

* lưu **rule ở mức logic**
* lưu **điều kiện**

nhưng **không nên**:

* tính số tiền cuối cùng
* làm rounding
* xử lý thuế

những thứ đó thuộc về:

* rk7
* pos runtime

---

## 5. promotion engine có phải source of truth của promotion không?

**tuỳ phạm vi, nhưng thường là không.**

* source of truth của **promotion definition**: ecom
* source of truth của **bill & tiền**: rk7 / pos
* promotion engine là **trusted middle layer**

=> nó đảm bảo:

* thông tin đi xuống pos là đúng
* không bị méo
* không vượt capability pos

---

## 6. nếu không có promotion engine thì sao?

hệ quả thường gặp:

* ecom nói chuyện trực tiếp với rk7
* mỗi campaign phải chỉnh tay pos
* rule lẫn lộn
* khó rollback
* pos thành “bãi rác logic marketing”

promotion engine giúp:

* tách marketing khỏi pos
* giữ pos gọn, ổn định
* giảm rủi ro runtime

---

## 7. một câu chốt kiến trúc (khuyên dùng)

> **promotion engine không quyết định giá,
> nó quyết định luật chơi nào được phép áp dụng trên pos.
> pos mới là nơi ra phán quyết cuối cùng cho bill.**

---

## 8. checklist nhanh cho team (20/80)

nếu thấy promotion engine:

* ✕ tính tiền → sai vai
* ✕ override bill → nguy hiểm
* ✓ validate rule → đúng vai
* ✓ map & truyền promotion → đúng vai
* ✓ để pos quyết định → chuẩn kiến trúc


