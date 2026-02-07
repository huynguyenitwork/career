# skycloud rest json service — chuẩn hoá ý định thiết kế

## mục tiêu
- dùng 1 service chung cho toàn bộ crud → giảm trùng lặp
- chuẩn hoá cách gọi rest json → giảm lỗi tích luỹ
- tách rời auth / request / cache / deserialize → dễ thay đổi từng phần
- tối ưu quyết định dev 7–30 ngày → thêm api mới không cần nghĩ lại kiến trúc

## phạm vi áp dụng
- rest api + json
- bearer token (jwt)
- backend .net core
- không chứa business logic

## nguyên tắc cốt lõi
- 20/80: 1 xương sống dùng cho mọi api, phần còn lại chỉ đổi endpoint + dto
- service chỉ làm "gọi" → không xử lý nghiệp vụ
- mọi logic lặp lại phải bị kéo về 1 chỗ

## kiến trúc ý định
- auth: chỉ chịu trách nhiệm cấp token
- request: gửi http request đúng chuẩn rest
- deserialize: chuyển json → object
- cache: chỉ can thiệp khi cần, không dính domain
- domain/service nghiệp vụ: đứng ngoài, chỉ orchestration

## service rest dùng chung
- cung cấp đủ 4 hành động: get / post / put / delete
- không biết domain là gì
- không biết cache dùng cho ai
- không biết token lấy từ đâu

## executor dùng chung (xương sống)
- tồn tại để:
  - gom logic cache về 1 chỗ
  - tránh copy-paste get/search
  - đảm bảo flow gọi api thống nhất
- chỉ làm 3 việc theo thứ tự:
  - kiểm tra cache
  - gọi api
  - ghi lại cache nếu hợp lệ
- chỉ áp dụng cho response dạng object → tránh lỗi kiểu dữ liệu

## quy tắc cache
- chỉ cache get / search
- không cache post / put / delete
- cache ngắn hạn → giảm call dư thừa, không thay thế source of truth
- cache key phải phản ánh đúng query

## quy tắc mở rộng api
- api mới = endpoint mới + dto mới
- không sửa executor nếu không có bug kiến trúc
- không thêm logic rẽ nhánh theo domain

## checklist bắt buộc
- không xml
- không hard-code token
- không nhét business logic vào service gọi api
- không cache hành động thay đổi dữ liệu
- không bypass executor cho get/search

## kết luận vận hành
- tách đúng → code phẳng, dễ đọc
- thêm api nhanh → không tăng gánh nhận thức
- sai chỗ nào biết ngay sai tầng nào
- đủ đúng để làm ngay, không tối ưu sớm
