
## inbound – những gì **bắt buộc phải có** để engine ra quyết định

tư duy nền: **promotion engine không cần biết thế giới**, nó chỉ cần **ảnh chụp khoảnh khắc checkout**. snapshot càng sạch, quyết định càng chuẩn.

### 1. thông tin định danh & truy vết (để không bị mù)

đây là lớp “hô hấp”, thiếu là chết ngạt:

* `bill_id` – định danh bill (log, trace, audit)
* `pos_id / store_id` – bán ở đâu
* `channel` – pos / web / app (nhiều promo phụ thuộc kênh)
* `timestamp` – thời điểm checkout (giờ vàng, giờ đen)

không có mấy thứ này thì promo có trúng cũng không biết vì sao.

---

### 2. danh sách item trong bill (trái tim của bài toán)

promotion tính trên **thứ đang bán**, không phải thứ sẽ bán:

mỗi item cần tối thiểu:

* `product_id / sku_id`
* `quantity`
* `unit_price` (giá gốc, chưa promo)
* `category / collection` (nếu có)
* `brand` (nếu promo theo hãng)

nguyên tắc 20/80: **đưa cái mà rule có thể đọc**, đừng đưa catalog đầy đủ như dump database.

---

### 3. tổng quan bill (để rule tính ngưỡng)

* `subtotal` – tổng tiền trước khuyến mãi
* `item_count` – tổng số lượng
* `currency`

rất nhiều rule kiểu:

* “đơn trên 500k”
* “mua ≥ 3 sản phẩm”
  không có lớp này là rule mù số học.

---

### 4. thông tin khách hàng (nếu có, không bắt buộc)

promotion engine **không quản lý khách hàng**, nhưng **được quyền biết khách là ai**:

* `customer_id` (hoặc anonymous)
* `customer_tier` (member / vip / new)
* `first_purchase` (boolean)

thiếu thì promo cá nhân hóa không chạy, nhưng engine vẫn sống.

---

### 5. context đặc biệt (chỉ khi có)

* `coupon_code` – user nhập tay
* `payment_method` – ví điện tử, thẻ, tiền mặt
* `delivery_method` – pickup / ship

cái này đúng kiểu: **không phải lúc nào cũng có, nhưng có là dùng liền**.

---

## outbound – promotion engine trả gì cho pos?

triết lý: **engine ra quyết định, pos thi hành**. không tranh quyền.

### 1. trạng thái quyết định

```json
{
  "status": "applied" | "no_promo" | "failed"
}
```

pos nhìn cái này là biết đi tiếp hay fallback.

---

### 2. kết quả khuyến mãi (nếu áp dụng)

* `discount_total`
* `discount_breakdown` (theo item hoặc theo rule)
* `gifts` (nếu có)
* `final_total`

quan trọng: **final_total chỉ là đề xuất**, pos vẫn là nơi chốt hiển thị.

---

### 3. metadata cho hiển thị & debug

* `applied_promotions`: `[ { promo_id, name } ]`
* `reason` (nếu không áp dụng hoặc failed)

cái này cứu đời lúc cskh hỏi:
“ủa sao đơn này không được giảm?”

---

### 4. nguyên tắc vàng của response

* **không side-effect**
* **không thay đổi bill**
* **không ghi db nghiệp vụ**
* **không yêu cầu pos làm lại request**

engine nói xong là… buông tay. thiền.

---

## tóm lại bằng một câu cho po & dev cùng hiểu

> promotion engine chỉ cần **bill snapshot + customer context + thời điểm**, và chỉ trả lại **quyết định khuyến mãi + số tiền**.
> mọi thứ ngoài ra là gánh nặng nghiệp lực.
