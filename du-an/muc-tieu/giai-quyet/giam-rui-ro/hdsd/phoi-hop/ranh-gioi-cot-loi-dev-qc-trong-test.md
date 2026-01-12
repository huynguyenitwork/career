## hiểu đơn giản thế này cho nhẹ đầu

một câu duy nhất để nhớ:

**qc lo "đúng với người dùng".**
**dev lo "hệ thống không tự làm bậy".**

qc và dev **không giành việc của nhau**, mỗi bên giữ một mảnh đất.

---

## phần của qc – đừng giành

qc tập trung vào những thứ **người dùng nhìn thấy và cảm nhận**.

qc test:

* đi đúng luồng không?
* làm đúng yêu cầu không?
* kết quả hiển thị có đúng không?

ví dụ:

* mua hàng có áp đúng khuyến mãi không
* store bị tắt thì người dùng có bị chặn không
* tổng tiền có đúng như mô tả không

nói ngắn gọn:
**qc đảm bảo "làm đúng cái cần làm".**

dev không cần test lại mấy thứ này, vì test cũng không sâu bằng qc.

---

## phần của dev – nên chủ động test

dev test những tình huống **ít ai để ý nhưng rất dễ gây sự cố**.

dev hỏi những câu kiểu:

* nếu dữ liệu sai thì sao?
* nếu thiếu thông tin thì chuyện gì xảy ra?
* nếu hệ thống khác không trả lời thì có làm bậy không?

ví dụ rất đời:

* store đã bị tắt nhưng job vẫn chạy âm thầm
* hệ thống báo "xong rồi" nhưng thực ra không ai nhận
* chạy lại một lần nữa có bị tính gấp đôi không

nói gọn:
**dev đảm bảo "không làm sai khi mọi thứ không hoàn hảo".**

---

## cách phân ranh cực nhanh (khỏi cãi)

nếu câu hỏi là:

* "người dùng thấy có đúng không?" → **qc**
* "hệ thống có tự gây lỗi không?" → **dev**

qc nhìn từ **bên ngoài**.
dev nhìn vào **bên trong**.

---

## vì sao dev cần test mấy case "lạ đời" này?

vì ngoài đời:

* dữ liệu hay thiếu
* hệ thống hay trễ
* mọi thứ hiếm khi đẹp như tài liệu

80% sự cố thật ngoài production đến từ:

* những tình huống ít ai nghĩ tới
* những lúc "đáng lẽ không xảy ra"

nên dev test mấy case đó là:

* để giảm rủi ro
* để đỡ gọi nhau lúc nửa đêm
* để hệ thống sống sót khi đời trở mặt

---

## cách nói để không đụng chạm qc

nói thế này là đúng bài:

* "case này em test để tránh rủi ro hệ thống, không liên quan nghiệp vụ."
* "luồng này qc cover rồi, em không test lại."

không ai bị giẫm chân.
không ai bị ôm trách nhiệm hộ người khác.

---

## chốt hạ nhẹ nhàng

qc giữ cho sản phẩm **đúng và đẹp**.
dev giữ cho hệ thống **không chết và không làm bậy**.

hai vai khác nhau, nhưng cùng mục tiêu:
**đừng để khách hàng là người đầu tiên phát hiện lỗi**.

đó là cách làm việc tỉnh táo, đỡ đau đầu, và đi đường dài được.
