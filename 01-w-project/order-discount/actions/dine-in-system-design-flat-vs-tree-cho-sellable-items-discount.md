# dine-in system design: flat vs tree cho sellable items & discount

#tag: #dine-in #flat #tree

## mục tiêu

- chốt nhanh thiết kế cho dine-in: **flat tối đa nhưng không lock**
- mỗi quyết định đều gắn với: giảm query, giảm validate, không mất khả năng mở rộng

---

## 1. phạm vi hệ thống dine-in

- giữ:
  - `tables` → định danh phiên ăn (mỗi bàn = 1 context order)
  - `orders` → lifecycle (open → paid)
  - `order_items` → snapshot món đã gọi
  - `dishes` → đơn vị bán trực tiếp cho khách
  - `payments` → tính tiền
  - `discounts` → rule giảm giá

- loại:
  - delivery / shipping → không có hành vi vận chuyển
  - external source → không sync menu/order
  - driver / trạng thái giao hàng → không tồn tại trong dine-in

→ ý nghĩa: **giảm toàn bộ dimension không ảnh hưởng bill tại bàn**

---

## 2. abstraction cốt lõi

- vấn đề:
  - product / variant / combo là **tree (nguồn dữ liệu)**
  - dine-in cần **gọi món nhanh (flat)**

- giải:
  - tạo lớp `dishes`:
    - đại diện **đơn vị bán cuối cùng**
    - không quan tâm cấu trúc bên dưới

- cấu trúc:
  - `dishes`
    - id
    - name
    - price
    - source_type (product | variant | combo)
    - source_id

→ ý nghĩa:

- UI + POS chỉ dùng `dishes`
- logic phức tạp giữ ở `source`

---

## 3. order_items = snapshot (bắt buộc)

- vấn đề:
  - nếu join ngược product → sai giá khi data thay đổi

- giải:
  - snapshot tại thời điểm order

- cấu trúc:
  - `order_items`
    - dish_id
    - name
    - price
    - quantity
    - discount_applied

→ ý nghĩa:

- đảm bảo bill không bị ảnh hưởng bởi thay đổi sau đó
- giảm query (không cần join)

---

## 4. discount design cho dine-in

- mục tiêu:
  - apply nhanh, không lookup nhiều tầng

- thiết kế:
  - `discount_dish_mapping`
    - discount_id
    - dish_id

- loại bỏ:
  - category-based discount
  - collection-based discount

→ chỉ giữ nếu thực sự có rule dùng

---

## 5. flat vs tree (rule quyết định)

- flat khi:
  - entity không ảnh hưởng:
    - giá cuối
    - lựa chọn của user

- giữ tree khi:
  - có logic cần validate

---

## 6. áp dụng cụ thể

### flat

- `dishes`
  - flatten toàn bộ product/variant/combo
  - chỉ giữ dữ liệu đủ để bán

- `order_items`
  - snapshot hoàn toàn

- `discount mapping`
  - direct dish

---

### giữ tree

- `combo_components`
  - lý do:
    - user chọn món con
    - validate số lượng

- `modifiers`
  - lý do:
    - thay đổi giá theo option
    - multi select

---

## 7. kiến trúc tối thiểu

- tables
- orders
- order_items
- dishes
- discounts
- discount_dish_mapping

→ đủ để:

- gọi món
- tính tiền
- giảm giá

---

## 8. anti-pattern

- dùng `dishes` làm nguồn dữ liệu duy nhất
  → mất khả năng rebuild khi cần

- duplicate discount logic (dine-in vs channel khác)
  → drift logic

- join sâu:
  - order → product → variant
    → tăng latency + bug pricing

---

## 9. checklist quyết định nhanh

- combo?
  - nếu có → giữ tree cho combo

- modifier/topping?
  - nếu có → giữ tree

- discount theo category?
  - nếu có → không flat hoàn toàn

---

## 10. decision output

- nếu:
  - không combo
  - không modifier
  - không category discount

→ chọn:

- full flat:
  - `dishes`
  - `order_items`
  - `discount_dish_mapping`

---

- nếu có ≥1:

→ chọn hybrid:

- `dishes` (để order nhanh)
- `source tree` (để validate + pricing)

---

## 11. bước tiếp theo (action)

- trả lời 3 câu:
  - combo? (y/n)
  - modifier? (y/n)
  - category discount? (y/n)

- nếu all = no:
  - implement full flat ngay

- nếu có:
  - giữ source tree
  - thêm mapping `dishes → source`

---

## kết luận

- dine-in = bài toán **tốc độ + đơn giản**
- giải đúng:
  - **flat ở layer bán**
  - **tree ở layer cấu hình**

- sai lầm lớn nhất:
  - cố unify mọi thứ thành 1 layer
