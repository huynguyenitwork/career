# thiết kế bảng discount cho hệ thống bán hàng (pos/skycrm)

#tag: #design-table #mapping-n-n #3nf #rule-engine

---

## mục tiêu quyết định

- giảm bug logic khi áp dụng discount
- scale được nhiều rule phức tạp
- query đủ nhanh cho runtime order

---

## chiến lược chọn

- **3nf + tách rule thành bảng riêng + mapping n-n**
- loại:
  - nhét tất cả vào 1 bảng discount → loại (không scale rule)
  - json rule → loại (không query/filter/index được)

---

## thiết kế sai (để loại)

- bảng `discounts`
  - `id`
  - `name`
  - `apply_store_ids` = "1,2,3"
  - `apply_product_ids` = "10,11"
  - `condition_json`

- vấn đề:
  - không index được → query chậm
  - update sai lệch → anomaly
  - không reuse rule

---

## thiết kế chọn (áp dụng nguyên tắc)

### bảng chính

- `discounts`
  - `id` (pk)
  - `name`
  - `type`
  - `created_at`

### dimension

- `stores`
- `products`
- `categories`

### mapping (n-n)

- `discount_store_mappings`
  - `discount_id`
  - `store_id`

- `discount_product_mappings`
  - `discount_id`
  - `product_id`

---

### rule engine tách riêng

- `discount_rules`
  - `id`
  - `discount_id`
  - `rule_type` (min_bill, buy_x_get_y,...)

- `discount_rule_buys`
  - `rule_id`
  - `product_id`
  - `quantity`

- `discount_rule_gets`
  - `rule_id`
  - `discount_percent`

---

## chứng minh phù hợp (theo tiêu chí loại)

### 1. tránh anomaly

- update product áp dụng discount:
  - chỉ insert vào mapping
  - không sửa string → không sai lệch

→ đạt mục tiêu consistency

---

### 2. scale rule

- thêm rule mới:
  - chỉ thêm record `discount_rules`
  - không đổi schema

→ không phá hệ thống

---

### 3. query runtime

- case: check discount theo store + product
  - join qua mapping + index fk

- index:
  - `discount_id`, `store_id`, `product_id`

→ query O(log n), không scan string

---

### 4. reuse logic

- 1 rule dùng nhiều discount:
  - tách rule riêng → reuse được

→ giảm duplication

---

### 5. tradeoff rõ ràng

- tăng số bảng → chấp nhận
- đổi lại:
  - logic rõ
  - debug dễ
  - scale được

→ payoff > cost → giữ

---

## kết luận (ra quyết định)

- chọn:
  - normalize + mapping + rule table

- bỏ:
  - json rule
  - multi-value column
  - hardcode logic trong 1 bảng

---

## check nhanh trước khi implement

- có query nào cần full scan không → nếu có → thêm index
- rule mới có cần đổi schema không → nếu có → thiết kế sai
- có field nào chứa nhiều giá trị không → nếu có → tách

---
