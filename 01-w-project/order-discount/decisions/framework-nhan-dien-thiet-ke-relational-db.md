# framework nhận diện thiết kế relational db

#tag: #thiet-ke #csdl-quan-he #rdbms #framework #design #decision

## mục tiêu

- giảm anomaly (insert/update/delete)
- giảm dư thừa
- scale rule + query theo use-case thật

---

# 0. rule bắt buộc (fail 1 cái → làm lại)

- không field chứa nhiều giá trị ("a,b,c", json để query) → tách
- không lưu data suy ra được → bỏ
- không thiết kế khi chưa có query chính → dừng
- thêm feature mà phải sửa schema → thiết kế sai

---

# 1. phân loại dữ liệu (bước đầu tiên)

| loại           | nhận diện                 | hành động               |
| -------------- | ------------------------- | ----------------------- |
| entity         | có id riêng, sống độc lập | tách bảng               |
| attribute      | mô tả entity              | giữ trong bảng          |
| relation n-n   | nhiều–nhiều               | mapping table           |
| rule/logic     | có điều kiện (if/else)    | bảng rule               |
| enum/dimension | tập nhỏ, ổn định          | bảng riêng / enum       |
| transaction    | phát sinh liên tục        | bảng riêng, append-only |

> nếu 1 field không phân loại được → dừng thiết kế

---

# 2. chuẩn hoá nhanh (loại dư thừa)

## test phụ thuộc

- field có phụ thuộc hoàn toàn vào pk không?
- field có phụ thuộc vào field khác không?
- field có thể suy ra từ field khác không?

## hành động

- phụ thuộc không hoàn toàn → tách (2nf)
- phụ thuộc bắc cầu → tách (3nf)
- suy ra được → bỏ

---

# 3. thiết kế shape theo query (bắt buộc)

## define 3 query chính

- query #1:
  - filter:
  - join:
  - sort:

- query #2:
- query #3:

## hành động

- field trong where → index
- field join → fk + index
- query xuyên nhiều bảng → cân nhắc denormalize (sau)

---

# 4. tách bảng theo biến động

| tình huống                  | hành động        |
| --------------------------- | ---------------- |
| field thay đổi thường xuyên | tách bảng        |
| cần lịch sử                 | bảng log/version |
| ít thay đổi                 | giữ chung        |

---

# 5. thiết kế relation

## 1-n

- fk ở bảng n

## n-n

- mapping table:
  - id (optional)
  - a_id
  - b_id
- index: (a_id), (b_id)

## anti-pattern (loại ngay)

- `a_ids = "1,2,3"`

---

# 6. rule engine (nếu có logic)

## nhận diện

- có điều kiện: min_bill, time_range, combo,...

## thiết kế

- rules table:
  - id
  - parent_id
  - rule_type

- rule detail tables:
  - theo từng loại rule

## anti-pattern

- json rule
- hardcode logic vào code + db không lưu

---

# 7. index strategy (theo use-case)

| use-case     | index       |
| ------------ | ----------- |
| where =      | btree       |
| range (>, <) | btree       |
| like %abc%   | gin/trigram |
| join fk      | index fk    |

## rule

- không index mọi cột
- mỗi index phải phục vụ query thật

---

# 8. fk & consistency

| tình huống | hành động       |
| ---------- | --------------- |
| cần strict | fk + constraint |
| high write | validate ở app  |

## cascade

- delete child theo parent → cascade
- giữ child → restrict

---

# 9. normalize vs denormalize

## default

- luôn normalize (>= 3nf)

## chỉ denormalize khi

- query chậm thực tế
- có cơ chế sync

## không làm

- duplicate data mà không sync

---

# 10. naming

- table: plural (`discounts`)
- column: snake_case
- fk: `{table}_id`

---

# 11. audit

- mặc định:
  - created_at
  - updated_at

- mapping đơn giản → có thể bỏ

---

# flow 5 phút (áp dụng ngay)

1. list tất cả field
2. phân loại (entity / relation / rule / attribute)
3. tách bảng:
   - entity
   - n-n
   - rule
4. test phụ thuộc → loại dư thừa
5. define 3 query → add index
6. check:
   - có multi-value field? → tách
   - có data suy ra? → bỏ
   - thêm feature có cần đổi schema? → nếu có → sai

---

# ví dụ tối giản

## input

- discount:
  - name
  - store_ids
  - product_ids
  - min_bill
  - percent

## phân loại

- discount → entity
- store_ids → n-n
- product_ids → n-n
- min_bill → rule
- percent → rule

## output

- discounts
- discount_store_mappings
- discount_product_mappings
- discount_rules

---

# checklist trước khi commit

- [ ] không field chứa nhiều giá trị
- [ ] không lưu data suy ra
- [ ] pk rõ ràng
- [ ] fk hoặc enforce logic
- [ ] index theo query thật
- [ ] thêm feature không cần đổi schema
- [ ] không json nếu cần query

---

# anti-pattern (loại nhanh)

- nhét tất cả vào 1 bảng
- dùng json thay vì bảng
- multi-value column
- không index theo query
- duplicate data không sync

---

# chốt

- bắt đầu từ:
  - phân loại dữ liệu
  - phụ thuộc
  - query thật

→ làm đúng 3 cái này → đúng 80%

