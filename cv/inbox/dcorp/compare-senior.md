## senior backend: business complexity vs technical complexity
### mục tiêu
nhiều người cho rằng một senior backend giỏi là người tối ưu hiệu năng, xử lý hàng triệu request hoặc xây dựng hệ thống cực lớn.
thực tế điều này chỉ đúng với một nhóm công ty nhất định.
đa số senior backend trong doanh nghiệp đang giải quyết **business complexity** nhiều hơn **technical complexity**.
mục tiêu của tài liệu này là phân biệt hai loại bài toán và hiểu khi nào mỗi loại trở thành trọng tâm.
## hai loại complexity
### business complexity
độ phức tạp đến từ **nghiệp vụ**.
câu hỏi thường gặp là:
* quy trình nghiệp vụ hoạt động như thế nào?
* dữ liệu nào hợp lệ?
* khi nào được phép thực hiện hành động?
* nếu nhiều hệ thống cùng tham gia thì ai là nguồn dữ liệu đúng?
* nếu xảy ra lỗi thì business mong muốn xử lý như thế nào?
  trọng tâm không phải viết code khó.
  trọng tâm là biến quy định của doanh nghiệp thành hệ thống hoạt động đúng.
### technical complexity
độ phức tạp đến từ **hệ thống kỹ thuật**.
câu hỏi thường gặp là:
* làm sao giảm latency?
* làm sao scale?
* cache ở đâu?
* index như thế nào?
* queue ra sao?
* chia microservice thế nào?
* chịu được bao nhiêu request?
  trọng tâm là làm hệ thống chạy nhanh hơn, ổn định hơn và mở rộng tốt hơn.
## hiểu lầm phổ biến
nhiều người nghĩ cv senior phải có các thành tích như:
* tăng performance 200%
* giảm latency 50%
* xử lý 10 triệu request/ngày
* tối ưu sql
  đây đều là ví dụ của **technical complexity**.
  thực tế rất nhiều senior trong các doanh nghiệp như:
* erp
* pos
* ngân hàng
* bảo hiểm
* logistics
* healthcare
* manufacturing
  không gặp các bài toán này hàng ngày.
  thứ họ giải quyết chủ yếu là **business complexity**.
## ví dụ business complexity
một hệ thống đồng bộ giữa pos và sap.
đây không phải bài toán "làm nhanh hơn".
đây là bài toán:
* giá nào được đồng bộ?
* promotion nào hợp lệ?
* nếu sap từ chối dữ liệu thì xử lý ra sao?
* retry bao nhiêu lần?
* khi nào được rollback?
* dữ liệu nào là nguồn sự thật?
* nếu đồng bộ trùng thì sao?
* ai được phép sửa dữ liệu?
* trạng thái nào được chuyển tiếp?
  phần lớn thời gian senior dùng để trả lời các câu hỏi này.
## ví dụ technical complexity
một hệ thống thương mại điện tử phục vụ hàng chục triệu người dùng.
các bài toán sẽ là:
* cache
* sharding
* indexing
* async processing
* load balancing
* distributed lock
* rate limiting
* queue
* horizontal scaling
  ở đây business khá đơn giản.
  độ khó nằm ở hạ tầng.
## senior backend thực sự giải quyết những gì
thực tế công việc của senior backend thường chia thành năm nhóm.
| nhóm            | mục tiêu                          | ví dụ                                                   |
| --------------- | --------------------------------- | ------------------------------------------------------- |
| business        | hệ thống làm đúng nghiệp vụ       | workflow, validation, approval, promotion, pricing      |
| integration     | nhiều hệ thống làm việc cùng nhau | api, erp, sap, payment, pos, webhook                    |
| reliability     | hệ thống vận hành ổn định         | retry, idempotency, monitoring, logging, alert          |
| maintainability | hệ thống dễ bảo trì               | clean architecture, module hóa, coding standard, review |
| performance     | hệ thống chạy nhanh               | cache, index, sql tuning, async, queue                  |
performance chỉ là **một trong năm nhóm**.
không phải toàn bộ công việc của senior.
## thứ tự ưu tiên trong đa số doanh nghiệp
nếu quan sát các jd senior backend hiện nay, đa số sẽ ưu tiên theo thứ tự:
| ưu tiên | năng lực          |
| ------- | ----------------- |
| 1       | hiểu nghiệp vụ    |
| 2       | thiết kế solution |
| 3       | thiết kế api      |
| 4       | validation        |
| 5       | integration       |
| 6       | logging           |
| 7       | monitoring        |
| 8       | retry             |
| 9       | error handling    |
| 10      | security          |
| 11      | testing           |
| 12      | performance       |
điều này phản ánh nhu cầu thực tế của doanh nghiệp.
một hệ thống chạy rất nhanh nhưng sai nghiệp vụ vẫn là một hệ thống thất bại.
## khi nào business complexity quan trọng hơn
thường gặp ở:
* erp
* crm
* pos
* ngân hàng
* bảo hiểm
* logistics
* bệnh viện
* chính phủ
* quản lý doanh nghiệp
  đặc trưng:
* nhiều quy trình
* nhiều luật nghiệp vụ
* nhiều vai trò
* nhiều hệ thống tích hợp
* dữ liệu phải chính xác
## khi nào technical complexity quan trọng hơn
thường gặp ở:
* google
* meta
* netflix
* cloudflare
* shopee
* tiktok
* các nền tảng internet quy mô rất lớn
  đặc trưng:
* lưu lượng cực lớn
* yêu cầu latency thấp
* hạ tầng phân tán
* chi phí vận hành rất cao
* khả năng mở rộng là yếu tố sống còn
## so sánh
| khía cạnh            | business complexity     | technical complexity    |
| -------------------- | ----------------------- | ----------------------- |
| câu hỏi chính        | hệ thống làm đúng chưa? | hệ thống chạy tốt chưa? |
| trọng tâm            | nghiệp vụ               | kỹ thuật                |
| độ khó               | luật business           | hạ tầng                 |
| lỗi phổ biến         | sai quy trình           | chậm, nghẽn, quá tải    |
| thành công           | đúng nghiệp vụ          | nhanh và ổn định        |
| người làm việc nhiều | ba, po, qa, khách hàng  | dev, devops, sre        |
## cv senior nên thể hiện điều gì
một cv tốt không nhất thiết phải toàn thành tích về performance.
quan trọng hơn là chứng minh được khả năng giải quyết vấn đề phù hợp với bối cảnh doanh nghiệp.
ví dụ:
**business complexity**
* thiết kế workflow đồng bộ dữ liệu.
* chuẩn hóa validation.
* thiết kế approval flow.
* chuẩn hóa promotion.
* xử lý reconciliation.
* thiết kế lifecycle của order.
  **integration**
* tích hợp sap.
* tích hợp payment.
* tích hợp webhook.
* tích hợp pos.
  **reliability**
* retry.
* idempotency.
* monitoring.
* logging.
* alerting.
* audit log.
  **maintainability**
* clean architecture.
* coding standard.
* module hóa.
* code review.
* mentoring.
  **performance**
* cache.
* index.
* sql tuning.
* async processing.
## kết luận
senior backend không được đánh giá bằng việc luôn tối ưu hiệu năng hay xử lý hàng triệu request.
giá trị lớn nhất của senior là **giải quyết đúng loại complexity mà doanh nghiệp đang gặp**.
* doanh nghiệp truyền thống thường cần người giải quyết **business complexity**.
* doanh nghiệp internet quy mô lớn thường cần người giải quyết **technical complexity**.
* một senior toàn diện hiểu cả hai, nhưng biết ưu tiên đúng vấn đề mới là điều tạo ra giá trị.
