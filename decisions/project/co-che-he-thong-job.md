# cơ chế hệ thống job


## cốt lõi
- "job" = 1 đơn vị công việc độc lập, có thể xử lý sau, có thể retry
- khác nhau ở "nội dung", giống nhau ở "cơ chế"

## vòng đời chuẩn (không đổi)
- create → queue → worker pick → handler process → success | fail → retry | dead

## vai trò (điểm dễ nhầm)
- worker = điều phối, lấy job, quản lý vòng đời
- handler = thực thi logic nghiệp vụ
- nhét logic vào worker → sai thiết kế

## thành phần tối thiểu cần có
- producer: tạo job
- queue: giữ job chờ xử lý
- worker: lấy job
- handler: xử lý việc
- storage: trạng thái + log
- monitoring: phát hiện nghẽn / fail

## công nghệ không quan trọng
- redis / rabbitmq / kafka / sql / memory
- đổi công cụ ≠ đổi tư duy

## khi nào dùng job (tiêu chí loại nhanh)
- xử lý lâu
- không cần trả kết quả ngay
- có khả năng fail, cần retry
- tải lớn, không chặn request
→ không thỏa các điểm trên → không cần job

## các "biến thể" thực chất giống nhau
- background / scheduled / event-driven / long-running / distributed / outbox
- khác trigger, không khác lõi

## áp dụng nhanh cho bài toán mới
- xác định job unit
- chọn queue đơn giản nhất đủ dùng
- viết handler rõ trách nhiệm
- worker chỉ gọi handler
- quản lý state + retry

## kết luận dùng để nhớ
- job = đơn vị việc + vòng đời
- worker điều phối, handler hành động
- hiểu vòng đời → hiểu toàn hệ job