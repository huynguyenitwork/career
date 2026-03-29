# db field change handbook

#tag: #use-case #decision-pipeline #phan-loai #design-field
---

## 0. mục tiêu

- giảm quyết định sai khi thêm field
- đảm bảo: **không dư data + không phá query + deploy an toàn**

---

## 1. input bắt buộc (thiếu → reject)

- `"use-case cụ thể"`
  - ví dụ: filter danh sách order theo `status=paid`

- `"query sẽ dùng"`
  - ví dụ: `where status = ?`

- `"tần suất"`
  - read-heavy / write-heavy / rare

---

## 2. decision pipeline

### step 1 — có cần field không

- `"có thể derive từ field khác?"` → có → **không lưu**
- `"có thể reuse field cũ?"` → có → **không thêm**
- `"chỉ để debug/log tạm?"` → có → **không thêm (log system)**

---

### step 2 — phân loại (bắt buộc)

- `"state"` → enum/int/bool
- `"config"` → bảng riêng nếu nhiều giá trị / thay đổi
- `"mapping"` → bảng trung gian (n-n)
- `"derived"` → không lưu
- `"snapshot"` (lưu lịch sử tại thời điểm) → cho phép lưu

→ không classify được → **reject**

---

### step 3 — thiết kế field

#### 3.1 data type

- số nhỏ → `int`
- id lớn → `bigint`
- text ngắn → `varchar(n)`
- không rõ size → `text` (chỉ khi không filter)

→ dùng type lớn hơn cần thiết → **reject**

---

#### 3.2 nullable + default

- business bắt buộc → `NOT NULL`
- optional → nullable + xử lý ở code
- default phải có nghĩa business
  - `status = 0` (không rõ nghĩa) → **reject**

---

#### 3.3 naming

- format: `snake_case`
- rõ nghĩa business
  - `is_active` ✔
  - `flag1` ✘

---

### step 4 — index decision

- có trong `WHERE / JOIN / ORDER BY` >20% query → **index**
- low-cardinality (boolean, enum ít giá trị) → **cân nhắc**
- write-heavy table → hạn chế index

→ không justify index → **chưa add**

---

### step 5 — impact check

- `"query cũ bị ảnh hưởng?"`
- `"full table scan xuất hiện?"`
- `"write latency tăng?"`

→ không đo được → **reject**

---

### step 6 — anti-pattern (dính 1 → reject)

- 1 field chứa nhiều ý nghĩa
- duplicate data để tiện query
- dùng `json` nhưng vẫn filter/query bên trong
- config nhét vào table chính
- enum nhưng lưu string dài

---

### step 7 — migration plan (bắt buộc)

#### 7.1 forward

- add column (nullable)
- deploy code đọc optional
- backfill data
- add constraint (NOT NULL / index)

#### 7.2 rollback

- remove usage code
- giữ column (không drop ngay)

→ không có rollback → **reject**

---

### step 8 — test

- insert/update với data lớn (≥10k rows)
- `EXPLAIN` query
  - index scan ✔
  - seq scan ✘ (nếu query chính)

---

## 3. output chuẩn (template)

```md
### field proposal

- table: orders
- field: status
- type: smallint
- nullable: no
- default: 0 (pending)

### use-case

- filter order theo status

### query

- select \* from orders where status = ?

### index

- yes (vì filter chính)

### impact

- tăng write cost nhẹ (1 index)
- giảm scan từ full → index scan

### migration

- add nullable column
- deploy code đọc optional
- backfill status
- set not null + add index

### rollback

- ignore field trong code
```

---

## 4. tool tự kiểm tra

### schema design

- dbdiagram.io
  - check quan hệ bảng → phát hiện cần tách bảng hay không

---

### query test

- DB Fiddle
  - test query + `EXPLAIN` → biết có scan hay không

---

### lint rule

- SQLFluff
  - check naming + convention

---

### simulate thực tế

- Supabase
  - chạy migration thật + test API

---

## 5. rule loại nhanh (dùng ngay)

- không có query cụ thể → loại
- derive được → loại
- config nhiều biến → tách bảng
- chưa rõ index → chưa add
- chưa có migration plan → không merge

---

## 6. checklist trước khi merge

- có use-case rõ
- có query cụ thể
- có index decision
- có migration + rollback
- chạy `EXPLAIN` không bị full scan

→ thiếu 1 → **block merge**
