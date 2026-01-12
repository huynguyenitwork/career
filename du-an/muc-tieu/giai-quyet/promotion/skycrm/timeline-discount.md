## Timeline discount (từ lúc có order → ra tiền cuối)

### Bước 1: Xác định “có discount nào tồn tại không”

**Bảng liên quan:** `Discounts`

Hệ thống làm 3 việc rất cơ bản:

* Discount có **đang active** không
* Có nằm trong **thời gian hiệu lực** không
* Có áp dụng cho **kênh bán** hiện tại không (POS / eCom)

Nếu không có bản ghi hợp lệ → **kết thúc**, không cần đi tiếp.

---

### Bước 2: Kiểm tra điều kiện áp dụng

**Bảng liên quan:** `DiscountRules`

Với mỗi discount hợp lệ ở bước 1:

* So bill với rule:

  * Tổng tiền
  * Số lượng món
  * Khung giờ / ngày
  * Điều kiện khác

Rule **không đạt** → discount này bị loại ngay.

Đây là bước **lọc mạnh nhất**.
80% discount rớt ở đây.

---

### Bước 3: Kiểm tra phạm vi áp dụng

**Bảng liên quan:** `DiscountGroups`

Discount còn sống tiếp nếu:

* Thuộc group cho phép
* Phù hợp với cửa hàng / khách hàng / chiến dịch

Bước này trả lời câu hỏi:

> Discount này **có quyền** áp dụng cho order này không?

---

### Bước 4: Kiểm tra có cần coupon hay không

**Bảng liên quan:** `CouponTypes`

Nếu discount yêu cầu coupon:

* Có nhập mã không
* Mã còn hiệu lực không
* Mã có đúng loại không

Không có hoặc sai coupon → discount bị loại.

---

### Bước 5: Loại trừ trước khi tính tiền

**Bảng liên quan:**

* `DiscountExclusionDishes`
* `DiscountExclusionCategories`

Ở bước này **discount vẫn hợp lệ**, nhưng:

* Một số món bị loại khỏi phạm vi giảm
* Một số category không được áp dụng

Quan trọng:

> Discount vẫn chạy, nhưng **giá trị giảm bị thu hẹp**

---

### Bước 6: Xử lý chồng discount

**Bảng liên quan:** `DiscountCombinations`

Nếu có nhiều discount cùng hợp lệ:

* Có cho phép áp dụng chung không
* Nếu không → ưu tiên discount nào
* Có giới hạn mức giảm không

Bước này quyết định:

> Khách được bao nhiêu tiền, hệ thống có lỗ không

---

### Bước 7: Gắn nhãn (không ảnh hưởng logic)

**Bảng liên quan:** `Discount_DiscountTag_Mappings`

Chỉ dùng cho:

* Hiển thị UI
* Báo cáo
* Phân loại marketing

Không tham gia quyết định áp dụng.

---

## Tóm tắt luồng logic cô đọng

```
Order
 ↓
Discounts               (có chương trình không?)
 ↓
DiscountRules           (đủ điều kiện không?)
 ↓
DiscountGroups          (có quyền áp dụng không?)
 ↓
CouponTypes             (có cần mã không?)
 ↓
Exclusions               (trừ món / trừ nhóm)
 ↓
DiscountCombinations    (chồng hay chọn 1)
 ↓
Ra số tiền cuối
```

---

## Ghi chú quan trọng (để thiết kế cho đúng)

* `Discounts + DiscountRules` là **lõi sống còn**
* Exclusion **không loại discount**, chỉ loại phạm vi
* Combination **luôn chạy sau cùng**
* Tag **không bao giờ** được dính vào logic tính tiền