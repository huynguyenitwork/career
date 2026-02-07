# hướng dẫn mermaid flowchart — chuẩn dev dùng hằng ngày

## mục tiêu sử dụng
- vẽ flow backend nhanh → đọc hiểu trong < 2 phút
- sửa logic không đập layout
- version control được, không lệ thuộc tool vẽ

---

## phạm vi cố ý giữ lại
- flowchart tb
- node: entry / process / decision / api / error / note
- connect: -->, -.->  
- subgraph
- classDef + class
→ ngoài các mục này: **loại**

---

## quy ước cốt lõi (bất di bất dịch)

- flow: **top → bottom**
- decision: **1 câu hỏi / 2 nhánh**
- error / retry: **đẩy sang phải**
- note: **giải thích rule, không tham gia logic**
- id: dùng cho sửa code, text: dùng cho người đọc

---

## khai báo tối thiểu bắt buộc

### flow header
- dùng `flowchart TB`
- không đổi hướng nếu không có lý do rõ

### node chuẩn
- entry: `(["..."])`
- process: `["..."]`
- decision: `{"...?"}`
- api: `["api: ..."]`
- error / retry: `["error: ..."]`

---

## nối luồng (chỉ giữ 2 loại)

- `-->` : luồng chính
- `-.->` : note / phụ / async

→ `---`, fancy arrow: **loại**

---

## decision chuẩn dev

- mỗi decision hỏi **1 điều kiện**
- nhánh đặt tên ngắn: `có` / `không`
- kết thúc nhánh càng sớm càng tốt

mẫu bắt buộc:
```mermaid
x{"tồn tại?"}
x -- có --> next
x -- không --> handle
