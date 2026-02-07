# tư duy phát triển phần mềm – bản quyết định nhanh

## 1. khóa vấn đề trước khi code
- ghi 1 câu: "bài toán đang giải là gì" → không viết được → dừng
- liệt kê "làm" / "không làm" → mọi thứ ngoài scope → loại
- chọn 1 pain point chính → còn lại → hoãn
- chốt tiêu chí xong việc (kpi/okr) → không đo được → loại

## 2. khóa dữ liệu & luồng
- liệt kê input / output tối thiểu → dư → cắt
- vẽ luồng dữ liệu 1 chiều từ vào → ra → vòng lặp phức tạp → loại
- đánh dấu dependency cứng → cái nào không bắt buộc → tách

## 3. khóa rủi ro trước deadline
- liệt kê rủi ro theo 2 trục: "xác suất cao" hoặc "ảnh hưởng lớn"
- chỉ giữ top 3 rủi ro → phần còn lại → chấp nhận
- rủi ro không ảnh hưởng 7–30 ngày → loại

## 4. chọn kiến trúc theo loại bài toán
- chưa cần scale lớn → monolith
- cần scale độc lập / team đông → microservice
- dữ liệu quan hệ rõ → sql ; dữ liệu linh hoạt → nosql
- công nghệ không giảm thời gian ra quyết định → loại

## 5. chốt đo lường ngay từ đầu
- chọn 3 metric sống còn (error, latency, throughput)
- không đo được → coi như không tồn tại
- alert chỉ cho lỗi làm hệ thống chết → còn lại → log

## công thức quyết định 5 phút
- problem rõ? → không → dừng
- dữ liệu đi đâu? → không rõ → vẽ
- rủi ro nào giết dự án sớm? → xử trước
- giải pháp đơn giản nhất chạy được? → chọn
- đo được chưa? → chưa → bổ sung

## nguyên tắc loại nhiễu
- không giúp quyết định ngay → loại
- không giúp làm nhanh hơn → loại
- không ảnh hưởng kết quả 30 ngày → loại
- chưa khóa mục tiêu mà bàn công nghệ → dừng