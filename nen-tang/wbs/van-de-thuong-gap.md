# các vấn đề thường gặp khi làm wbs và cách xử lý

## 1. bệnh "chia quá chi tiết"

người mới hay cố chia wbs thành 10–20 đầu việc nhỏ tí như: mở file, đọc hàm, note lại,… làm wbs trở thành danh sách lặt vặt.

**giải pháp:**
gộp lại thành 3–5 khối lớn:
– hiểu phạm vi
– hiểu luồng
– tạo output
– đối chiếu/review
→ càng lớn càng tốt, miễn đúng hướng.

---

## 2. bệnh "không biết cái nào là 20% quan trọng nhất"

wbs viết ra nhiều nhưng không biết đâu là việc tạo 80% kết quả → ngốn thời gian, po khó nắm tiến độ.

**giải pháp:**
xác định 1–2 câu trả lời then chốt:
"muốn task giải được, tôi bắt buộc phải hiểu cái gì?"
→ đó chính là 20%.
đưa lên đầu, ghi rõ, làm trước.

---

## 3. bệnh "bỏ qua việc vẽ sơ đồ thô sớm"

không vẽ sơ đồ từ đầu → làm 2 ngày rồi mới thấy bị sai hướng → delay.

**giải pháp:**
vẽ sơ đồ thô trong 10 phút ngay từ ngày 1.
không cần đẹp, chỉ cần nhìn ra mảnh ghép còn thiếu.

---

## 4. bệnh "ước lượng sai do là người mới"

nhiều người ảo tưởng tốc độ của bản thân hoặc copy estimate từ senior → trễ timeline.

**giải pháp:**
luôn cộng thêm "buffer người mới" 30–50% khi phải:
– setup môi trường
– đọc luồng chưa có tài liệu
– vẽ sơ đồ
– phân tích dữ liệu thực tế
po rất dễ chấp nhận vì minh bạch.

---

## 5. bệnh "wbs không có mục tiêu đầu ra rõ ràng"

wbs ghi toàn hành động mà không ghi **output** nên po không biết bạn đang tiến triển ra sao.

**giải pháp:**
luôn bắt đầu wbs bằng 2–3 output cuối cùng, ví dụ:
– hiểu luồng giá–combo trọn vẹn
– vẽ sơ đồ as-is hoàn chỉnh
– xác định phạm vi code chính xác
→ làm wbs có định hướng, po đọc 10s là hiểu.

---

## 6. bệnh "không track tiến độ theo phần trăm – chỉ liệt kê việc làm"

daily kiểu: "hôm nay em đọc code, xem rk7, ghi chú thêm."
→ po đọc xong không biết bạn chạy nhanh hay chậm.

**giải pháp:**
luôn có 1 dòng tỷ lệ tiến độ:
– 30% phần hiểu luồng
– 70% mapping combo
– 90% sơ đồ luồng
→ vừa rõ ràng vừa tạo cảm giác kiểm soát công việc.

---

## 7. bệnh "không nêu rủi ro"

làm phần khó nhưng không báo sớm các chỗ mờ → cuối tuần bị kẹt → po không happy.

**giải pháp:**
daily luôn có 1 dòng risk:
– rule combo loại b chưa rõ
– môi trường rk7 sinh dữ liệu khác dự kiến
→ po thấy là biết bạn có trách nhiệm.

---

## 8. bệnh "wbs không bám timeline thực tế"

có người gom tất cả việc vào 1 ngày → y như siêu nhân.
nhưng thực tế: setup môi trường + đọc code + test combo + vẽ sơ đồ… không bao giờ gói gọn một ngày.

**giải pháp:**
chia theo ngày (2–3 ngày), đúng sức người mới:
– ngày 1: setup + test combo + xác định phạm vi
– ngày 2: đào logic + test rộng + 70% sơ đồ
– ngày 3: hoàn thiện + đối chiếu + sync
→ po nhìn vào là thấy plan êm.

---

## 9. bệnh "quên đặt ưu tiên"

dễ sa đà vào phần ít quan trọng như format sơ đồ, đẹp hay không, màu gì…

**giải pháp:**
chỉ làm đẹp khi hiểu đúng 100%.
ưu tiên: đúng → đủ → đẹp.

---

## 10. bệnh "wbs không linh hoạt với sự thật"

khi làm mới thấy phức tạp hơn → nhưng không dám báo → dẫn đến mismatch kỳ vọng.

**giải pháp:**
nếu thấy lệch, cập nhật wbs theo ngày.
po thích cập nhật hơn là im lặng.

---

## tóm gọn lại theo tinh thần 20/80

wbs tốt không phải wbs nhiều đầu việc.
wbs tốt là wbs chỉ cần nhìn 10 giây là po hiểu:
– bạn đang ở đâu
– bạn đang tập trung vào cái gì
– bao lâu thì xong
– rủi ro nằm ở đâu

---

nếu bạn muốn, mình viết cho bạn **bản template wbs 20/80 chuẩn cho dev mới**, copy-paste 1 phát là dùng được cho mọi task, từ đọc code tới dev hay fix bug.
