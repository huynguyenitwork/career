chú thích:
- chưa rõ mục đích của nghiệp vụ, kết quả đầu ra cần gì, yêu cầu về nghiệp vụ gì để có được yêu cầu về kỹ thuật: giống như là em chưa biết điểm đến là gì anh bảo em tới Hoàng Hoa Thám trong khi có Hoàng Hoa Thám ở quận Bình Thạnh, ở quận Bình Tân. anh đánh đố em rồi
- POS cần gì ở promotion enginee (input/output là gì ở mức nghiệp vụ)
---

## điều kiện bắt buộc để dev triển khai được

dev **chỉ bắt đầu implement** khi po xác nhận rõ các điểm sau:

1. **mục tiêu nghiệp vụ**
   promotion dùng để làm gì? (chốt bill, đồng bộ giá, giữ khách, xả hàng…)

2. **thời điểm kích hoạt**
   pos gọi promotion khi nào? (add item / tạm tính / chốt bill)

3. **phạm vi & điều kiện áp dụng**
   áp dụng theo bill, sản phẩm hay user?
   có giới hạn số lần, thời gian, cửa hàng không?

4. **rule ưu tiên & xung đột**
   nhiều promotion cùng lúc xử lý thế nào?
   có cộng dồn hay không?

5. **input nghiệp vụ tối thiểu**
   pos cần gửi những dữ liệu gì để tính promotion?
   (bill, items, user, store, time…)

6. **output mong muốn**
   promotion trả lại cho pos cái gì?
   (giảm tiền, quà tặng, flag, message…)

7. **xử lý khi không đủ điều kiện**
   không áp được promotion thì hệ thống phản hồi thế nào?

---

### nguyên tắc triển khai

* po chịu trách nhiệm **xác nhận nghiệp vụ**
* dev chịu trách nhiệm **thiết kế & triển khai kỹ thuật**
* thiếu bất kỳ mục nào trên → **chưa đủ điều kiện code**

---

### câu chốt chuẩn dev senior (dùng để gửi po)

> “khi 7 điểm trên được xác nhận, em sẽ chịu trách nhiệm toàn bộ phần kỹ thuật và tiến độ.”

ngắn, rõ, không drama.
có checklist này, bạn không còn là dev “đi tìm yêu cầu”, mà là dev **điều khiển tốc độ dự án**.
