# wbs 20/80 cho task 09-12-2025 – sync luồng giá & combo

## 1. output chính

– hiểu rõ luồng giá–combo từ code → rk7 → sale data.
– vẽ sơ đồ luồng hoàn chỉnh để anh hiệp + team xem và đồng bộ cách làm.
– chốt phạm vi chỉnh sửa, tránh xử lý sai hoặc thiếu.

---

## 2. 20% quan trọng nhất (cần làm ngay)

đây là phần quyết định 80% kết quả:

1. **xác định chính xác phạm vi code liên quan đến giá & combo.**
   (nếu xác định sai phạm vi = tốn công về sau.)

2. **làm rõ cơ chế combo trên rk7 (điều kiện, nguyên liệu, cách tạo combo).**
   (phần này quyết định logic business.)

→ chỉ cần nắm vững hai phần này là đã hiểu 70–80% luồng.

---

## 3. wbs chi tiết (gọn theo 20/80)

### a. trọng tâm – 20% then chốt

1. rà code để định vị phạm vi liên quan: file, class, service, mapping.
2. check combo trên rk7: cách tạo, kiểu combo, dữ liệu sinh ra.
3. ghi nhanh 1 sơ đồ thô (5–10 phút) để nhìn ra missing.

*thời gian ước tính:* **1h30 – 2h**

---

### b. thực thi chính

1. đi sâu logic xử lý giá – combo trong code.
2. theo dõi data flow: master data → luồng giá → combo → sale data.
3. vẽ sơ đồ luồng hoàn chỉnh theo trình tự (as-is).

*thời gian ước tính:* **2h – 3h**

---

### c. hoàn thiện

1. đối chiếu lại với rk7 để đảm bảo sơ đồ đúng thực tế.
2. kiểm tra rủi ro: thiếu mapping? thiếu case? lệch logic?

*thời gian:* **30–45 phút**

---

### d. bàn giao / sync với anh hiệp

1. gửi sơ đồ luồng + note phạm vi + rủi ro.
2. chốt xem cần chỉnh lại phần nào trước khi bắt tay vào dev.

*thời gian:* **15–20 phút**

---

# 4. tổng thời gian dự kiến

**khoảng: 4 giờ – 6 giờ**
tuỳ độ phức tạp code + combo nhiều loại hay ít.

---

# 5. bản báo cáo daily mẫu (ngắn – đẹp – đúng việc)

**hôm nay:**
– hoàn thành xác định phạm vi code + check combo trên rk7.
– đã có sơ đồ luồng thô.

**ngày mai:**
– hoàn thiện sơ đồ chính + mapping data.
– sync với anh hiệp phần thiếu.

**risk:**
– chưa rõ combo loại x/y nếu trên hệ thống có.
– cần confirm logic phụ nếu có điều kiện đặc biệt.

---