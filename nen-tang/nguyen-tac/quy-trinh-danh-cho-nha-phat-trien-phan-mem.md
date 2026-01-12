**1. chuẩn bị nguyên vật liệu (đừng đụng code vội)**
đây là lúc phân biệt thợ với người gõ phím.

mục tiêu: hiểu đúng bài toán trước khi giải.
làm gì:

- chốt **mục tiêu kinh doanh / nghiệp vụ**: hệ thống này tồn tại để làm gì, ai dùng, sai thì mất gì.
- khoanh **phạm vi tối thiểu (mvp)**: làm đủ xài, không làm cho đã tay.
- rà **input / output / rule chính**: data vào từ đâu, ra cho ai, lệch là vỡ.
- quyết định nhanh stack, convention, naming ngay từ đầu.

nguyên tắc sống còn:

> chưa rõ bài toán thì code càng nhanh càng chết sớm.

---

**2. dựng thô (lên khung, chạy được là thắng)**
đây là giai đoạn thô ráp, xấu nhưng phải chạy.

mục tiêu: có thứ **chạy end-to-end** càng sớm càng tốt.
làm gì:

- dựng skeleton project, folder, layer.
- mock data, fake service cũng được.
- flow chính chạy qua được: api → service → db → response.
- ưu tiên **happy path**, bỏ qua edge case.

nguyên tắc:

> chạy được quan trọng hơn chạy đẹp.

---

**3. làm mịn (tối ưu, chỉnh hình, bơm não)**
lúc này mới thể hiện đẳng cấp kỹ sư.

mục tiêu: code dễ đọc, dễ sửa, khó vỡ.
làm gì:

- refactor: tách hàm, đặt tên lại, bỏ duplication.
- thêm validate, logging, error handling.
- tối ưu query, cache, transaction.
- viết test cho logic lõi (không test mấy thứ vô hồn).

nguyên tắc:

> code đọc như văn xuôi, người sau mở vào không chửi thầm.

---

**4. đóng gói (chuẩn bị cho đời thật)**
đây là lúc nghĩ cho hệ thống, không phải cho mình.

mục tiêu: deploy được, vận hành được, rollback được.
làm gì:

- config env, secret, feature flag.
- script migrate, seed, rollback.
- health check, monitoring cơ bản.
- tài liệu usage ngắn gọn, đúng chỗ.

nguyên tắc:

> dev xong mà ops không xài được = chưa xong.

---

**5. bàn giao (kết thúc có trách nhiệm)**
rất nhiều dự án chết ở đây vì… ngại nói.

mục tiêu: người khác tiếp quản không hoảng loạn.
làm gì:

- bàn giao flow tổng thể + điểm dễ nổ.
- ghi rõ assumption, limitation.
- chốt trạng thái: done, known issue, next step.

nguyên tắc:

> dự án tốt là dự án rời tay vẫn sống.

---

**tóm gọn 1 dòng cho não bận rộn**
hiểu bài toán → chạy được sớm → làm mịn có chọn lọc → sẵn sàng deploy → bàn giao tử tế.

đây là khung xương. áp vô backend, frontend, data hay infra đều dùng được. khác nhau chỉ ở “nguyên vật liệu”, không khác ở tư duy.
