# wbs 20/80 cho task 09-12-2025 – sync luồng giá & combo (người mới)

## vấn đề thường gặp
người mới nên cần thời gian đọc hiểu, kiểm thử có thời gian tập trung hơn xử lý dễ về sau

## 1. output chính

– hiểu trọn luồng giá–combo từ code → rk7 → sale data.
– tự dựng môi trường rk7 để tự test combo hoạt động.
– vẽ sơ đồ luồng hoàn chỉnh, dễ sync với anh hiệp và team.
– xác định đúng phạm vi code cần nắm và cần sửa.

---

## 2. 20% quan trọng nhất (ưu tiên trong 2 ngày đầu)

1. thiết lập xong môi trường rk7 để tự tay tạo combo → quan sát data.
2. định vị đúng phạm vi code giá–combo và hiểu luồng chạy chính.
3. vẽ được sơ đồ thô để nhìn ra các mảnh ghép còn mờ.

→ khi 3 phần này rõ, bạn đã chiếm 70–80% độ hiểu.

---
mình chỉnh lại toàn bộ wbs để phù hợp **đúng thực tế của một người mới**, có thêm phần **thiết lập môi trường rk7**, **tự test luồng tạo combo**, **tự vẽ sơ đồ**, và thời gian trải dài **2–3 ngày** để đạt mức hiểu sâu.

mình cũng viết lại theo tinh thần “gọn – thật – báo cáo được ngay”.

---

## 3. wbs chi tiết (đã điều chỉnh theo tốc độ người mới)

### a. ngày 1 – trọng tâm (20% then chốt)

1. **thiết lập môi trường rk7**: cấu hình, quyền, kết nối.
2. **tạo thử combo trên rk7**:
   – tạo combo cơ bản
   – xem nguyên liệu được map ra sao
   – xem dữ liệu sale data sinh ra thế nào
3. **định vị phạm vi code chính** (service, mapping, handler).
4. ghi nhanh sơ đồ thô “code → rk7 → sale data”.

*thời gian ước tính:* **3–4h (vì bạn mới)**

---

### b. ngày 2 – thực thi chính

1. đi sâu luồng xử lý giá–combo trong code (flow, mapping, rule).
2. test nhiều case hơn trong rk7 để tìm hành vi bất thường.
3. vẽ sơ đồ as-is chi tiết hơn (khớp code + rk7).
4. ghi lại chỗ nào chưa hiểu để hỏi anh hiệp.

*thời gian:* **4–5h**

---

### c. ngày 3 – hoàn thiện

1. đối chiếu sơ đồ với dữ liệu thực tế từ rk7 → sale data.
2. bổ sung các nhánh rủi ro, mapping dễ sai, rule đặc biệt.
3. tối ưu lại sơ đồ cho dễ đọc (1 trang hoặc 2 layout).
4. chuẩn bị note + điểm hỏi anh hiệp.

*thời gian:* **3–4h**

---

### d. sync / bàn giao

1. gửi sơ đồ + note + những điều còn mờ.
2. chốt phạm vi sửa và bước dev tiếp theo.
3. lên timeline dev.

*thời gian:* **30 phút**

---

# 4. tổng thời gian thực tế (người mới)

**≈ 2.5 – 3 ngày**
bao gồm: setup môi trường, tự test combo, hiểu code, vẽ luồng.

→ sau giai đoạn hiểu, phần dev sẽ nhẹ nhàng hơn rất nhiều (30–40%).

---

# 5. daily report mẫu (chuẩn chỉnh – người mới – không vòng vo)

### ngày 1

– đã setup rk7, tạo được combo mẫu.
– quan sát được cấu trúc data sinh ra.
– xác định được phạm vi code giá–combo.
– có sơ đồ thô luồng code → rk7 → sale data.
**risk:** môi trường rk7 có một vài hành vi chưa rõ (ghi chú cụ thể).

### ngày 2

– hiểu sâu hơn logic xử lý giá–combo trong code.
– test thêm x case combo, đã thấy sự khác biệt giữa type a/b.
– hoàn thiện 70% sơ đồ luồng as-is.
**risk:** mapping của combo phức tạp, cần confirm 1–2 rule.

### ngày 3

– sơ đồ luồng hoàn chỉnh, mapping rõ ràng.
– checklist rủi ro đầy đủ.
– chuẩn bị nội dung sync với anh hiệp.
**next:** chốt phạm vi dev + estimate.

---

#6. báo cáo
đã hoàn thành

– nắm được luồng sync product–price ở mức tổng thể, hoàn thiện test sync product.
– xác định đúng phạm vi code xử lý product–price.
– dựng được sơ đồ thô cho bước test price và combo.

việc cần làm

– hoàn thiện test price và đối chiếu dữ liệu rk7 trên giao diện r-keeper.
– hoàn thiện sơ đồ as-is cho luồng product–price (ecom → rk7).
– test combo.


completed

- gained a full understanding of the product–price sync flow and completed the product sync test
- identified the exact code scope related to product–price handling
- created a draft diagram for testing price and combo

next steps

- complete price testing and cross-check rk7 data on the r-keeper interface
- finalize the current-state (as-is) diagram for the product–price flow (from ecom to rk7)
- complete the combo test
