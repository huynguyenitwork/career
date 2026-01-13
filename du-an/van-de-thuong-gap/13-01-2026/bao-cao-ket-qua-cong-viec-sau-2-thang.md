# kết quả công việc

* nhanh chóng nắm bắt domain và các luồng nghiệp vụ cốt lõi của hệ thống, đặc biệt là các luồng đồng bộ phức tạp
* tham gia trực tiếp vào giai đoạn **xây nền và phát triển logic backend**, tập trung vào việc hiểu đúng và kiểm chứng các luồng nghiệp vụ trước khi triển khai sâu
* phối hợp chủ yếu với **pm và backend**, làm rõ yêu cầu, xác định phạm vi kỹ thuật và thống nhất hướng tiếp cận phù hợp với thực tế hệ thống
* các hạng mục hiện đang trong giai đoạn phát triển và kiểm chứng, **chưa có task deploy production** do:
  * thời gian tham gia còn ngắn
  * yêu cầu nghiệp vụ có độ khó cao và thay đổi
  * cần ưu tiên thông và ổn định luồng nghiệp vụ trước khi vận hành thật

---

# những gì đã làm được (> expectation)

* chủ động phân tích hệ thống ở mức **end-to-end** (ecom → skytransfer / skycloud → refagent → rk7), thay vì chỉ xử lý từng task riêng lẻ
* đã triển khai và demo thành công các luồng create / update / delete open discount từ ecom → skytransfer → skycloud, hoàn thiện mapping dữ liệu (date, type, store selection), thống nhất hướng command-driven và đặt nền sẵn sàng cho bước đồng bộ tiếp theo sang rk7
* làm rõ và hệ thống lại các luồng đồng bộ chính: store, product, price, combo, promotion/open discount, tạo nền cho phát triển và mở rộng sau này
* thực hiện dev test và validation cho nhiều kịch bản đại diện, qua đó:
  * xác định rõ thứ tự xử lý
  * quan sát hành vi queue
  * phát hiện sớm các rủi ro tiềm ẩn nhưng chưa gây business impact
* nghiên cứu và thử nghiệm các hướng **refactor và tối ưu**, hiện đang ở giai đoạn đánh giá và chuẩn bị, chưa đưa vào vận hành để tránh ảnh hưởng tiến độ nghiệp vụ chính
* giữ nhịp làm việc ổn định trong bối cảnh yêu cầu chưa cố định và kiến trúc đang được điều chỉnh

---

# những gì chưa làm được (< expectation)

* chưa có hạng mục nào được deploy lên môi trường production trong giai đoạn này
* chưa phối hợp với frontend do phạm vi công việc hiện tại tập trung hoàn toàn vào backend và các luồng đồng bộ nghiệp vụ
* các đề xuất cải tiến kỹ thuật mới dừng ở mức nghiên cứu và thử nghiệm, cần thêm thời gian và độ ổn định của hệ thống để triển khai chính thức

---

# những điểm mạnh & điểm cần tiếp tục cải thiện

## điểm mạnh

* khả năng tiếp cận nhanh hệ thống mới và hiểu sâu nghiệp vụ phức tạp
* tư duy cẩn trọng, ưu tiên làm đúng và bền thay vì làm nhanh nhưng tiềm ẩn rủi ro và làm lại
* giao tiếp rõ ràng với pm về rủi ro kỹ thuật, mức độ phức tạp và thời gian cần thiết cho từng hạng mục
* chủ động phát hiện và ghi nhận vấn đề sớm để theo dõi, thay vì xử lý muộn khi đã ảnh hưởng vận hành

## điểm cần tiếp tục cải thiện

* cần thêm thời gian để chuyển từ giai đoạn **xây nền và kiểm chứng** sang **tăng tốc triển khai** khi nghiệp vụ đã ổn định hơn
* cần chọn thời điểm phù hợp để hiện thực hóa các cải tiến kỹ thuật đã nghiên cứu nhằm tối ưu vận hành dài hạn

---

# những thuận lợi & khó khăn trong quá trình làm việc

## thuận lợi

* pm trao đổi rõ ràng, sẵn sàng làm rõ yêu cầu và định hướng khi có thay đổi
* được tập trung xử lý các bài toán nghiệp vụ cốt lõi, phù hợp với kinh nghiệm backend và integration
* môi trường cho phép kiểm chứng, thử nghiệm và điều chỉnh hướng tiếp cận trước khi commit sâu

## khó khăn

* yêu cầu nghiệp vụ có độ phức tạp cao và thay đổi trong quá trình phát triển
* thời gian tham gia chưa đủ dài để đưa toàn bộ các cải tiến vào môi trường vận hành và đánh giá hiệu quả thực tế
* các mảng công việc trong team tương đối độc lập ở giai đoạn này, ít phát sinh nhu cầu hỗ trợ chéo