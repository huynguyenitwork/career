# ef savechanges vs executesqlcommand (20/80)

## vấn đề

trong các luồng **job / worker / state machine**, `savechanges()` có thể chỉ update lần đầu, các lần sau **không thay đổi db** dù không có lỗi.

---

## nguyên nhân cốt lõi

`SaveChanges()` phụ thuộc vào **ChangeTracker và concurrency**:

* entity phải được track đúng
* ef phải biết giá trị cũ
* không được xung đột rowversion / trigger / job khác

trong khi luồng xử lý nền thường:

* dùng nhiều DbContext
* update trạng thái theo bước (Processing → Done)
* không reload entity giữa các bước

→ ef không đủ thông tin, dẫn tới **0 row affected** và im lặng.

---

## vì sao attach + modified vẫn không đủ?

`Attach + Modified` chỉ yêu cầu ef update, nhưng ef vẫn:

* áp dụng điều kiện WHERE theo state nó tin
* áp dụng concurrency
* không throw exception khi không update được

quyền quyết định cuối vẫn ở ef.

---

## vì sao executesqlcommand hiệu quả?

`ExecuteSqlCommand / ExecuteSqlRaw`:

* bỏ qua changetracker
* gửi lệnh trực tiếp cho db
* trả về số row affected

phù hợp với command-style update và state machine.

---

## quyết định nhanh

dùng `SaveChanges()` khi:

* CRUD, API, form
* entity sống trong một DbContext

dùng `ExecuteSqlCommand` khi:

* update trạng thái
* Job / worker / queue
* nhiều DbContext
* DB là source of truth

---

## kết luận

`SaveChanges()` không sai, nhưng **không phù hợp cho bài toán state machine và xử lý nền**.

với command-style update, **ExecuteSqlCommand là lựa chọn đúng**.
