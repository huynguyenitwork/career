# chung

---

**GET**
**Ý nghĩa:** Lấy dữ liệu
**Khi dùng:** Khi chỉ cần xem (list, detail), **không làm thay đổi gì**

---

**POST**
**Ý nghĩa:** Tạo mới
**Khi dùng:** Khi cần sinh ra một bản ghi mới

---

**PUT**
**Ý nghĩa:** Cập nhật
**Khi dùng:** Khi cần sửa dữ liệu đã tồn tại (thường là sửa toàn bộ)

---

**PUT (status / field riêng)**
**Ý nghĩa:** Cập nhật một phần quan trọng
**Khi dùng:** Khi chỉ đổi trạng thái, bật/tắt, hành động nhanh

---

**DELETE**
**Ý nghĩa:** Xóa
**Khi dùng:** Khi dữ liệu không còn dùng nữa (thường là xóa mềm)

---

**Chốt 1 câu để nhớ:**
=> *Xem thì GET · Tạo thì POST · Sửa thì PUT · Bật/tắt thì PUT riêng · Bỏ thì DELETE.*

# ví dụ
Nhìn hình là một **REST API chuẩn cho resource `Discount`**. Hiểu nhanh – dùng đúng – khỏi lăn tăn.

Tư duy gốc: **REST = làm gì với *resource***, không phải “gọi hàm”.
`/discounts` là **tập** · `/discounts/{id}` là **một phần tử cụ thể**.

---

### 1. `GET /discounts`

**Ý nghĩa:** Lấy danh sách discount
**Khi dùng:**

* Màn hình list
* Search / filter / paging
* Không làm thay đổi dữ liệu

→ *Hỏi thông tin, không động chạm gì hết.*

---

### 2. `GET /discounts/{id}`

**Ý nghĩa:** Lấy chi tiết 1 discount
**Khi dùng:**

* Xem detail
* Load data trước khi edit

→ *Muốn biết rõ một đứa cụ thể.*

---

### 3. `POST /discounts`

**Ý nghĩa:** Tạo mới discount
**Khi dùng:**

* Create form
* Clone từ template

→ *Sinh ra cái mới.*
POST = **create**, không tranh cãi.

---

### 4. `PUT /discounts`

**Ý nghĩa:** Cập nhật toàn bộ discount
**Khi dùng:**

* Edit form → lưu lại toàn bộ object
* Client gửi đủ data

→ *Ghi đè trạng thái mới.*
PUT = **update full**.

---

### 5. `PUT /discounts/status/{id}`

**Ý nghĩa:** Cập nhật **một phần nhỏ** (status)
**Khi dùng:**

* Enable / Disable
* Activate / Deactivate
* Action nhanh, không cần gửi cả object

→ *Động tác phẫu thuật chính xác, không mổ toàn thân.*

(Chuẩn REST tuyệt đối thì dùng `PATCH`, nhưng `PUT status` là thực tế rất hay gặp.)

---

### 6. `DELETE /discounts`

**Ý nghĩa:** Xóa discount (thường là soft delete)
**Khi dùng:**

* Không còn dùng nữa
* Ẩn khỏi hệ thống

→ *Cho về dĩ vãng.*

---

## Quy tắc để nhớ nhanh

* **Xem** → `GET`
* **Tạo** → `POST`
* **Sửa nhiều thứ** → `PUT`
* **Sửa 1 thuộc tính quan trọng** → `PUT /status` (hoặc `PATCH`)
* **Xóa** → `DELETE`

