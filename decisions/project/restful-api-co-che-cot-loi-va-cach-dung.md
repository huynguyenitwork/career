# restful api – cơ chế cốt lõi và cách dùng

## contract & triết lý (nền bắt buộc)
- restful api = hợp đồng trạng thái
- trách nhiệm client vs server
- dùng sai method = phá hợp đồng
→ dùng để khóa tư duy trước khi thiết kế

## ngữ nghĩa http method (bảng luật)
- get: đọc
- post: tạo / hành động
- put: replace toàn bộ
- patch: update từng phần
- delete: loại bỏ
→ dùng để chọn method, không bàn cãi

## put & patch (vùng rủi ro cao)
- put: replace 100%, field thiếu = mất
- patch: merge từng phần
- null vs không truyền
→ dùng để tránh mất dữ liệu

## tiêu chí quyết định (actionable)
- có full state → put
- chỉ sửa 1 phần → patch
- không chắc dữ liệu đủ → patch
→ dùng ngay khi code api

## hệ quả & edge case (cảnh báo)
- gửi thiếu field
- client version mismatch
- backend merge ngầm
→ dùng để review thiết kế, code review

## usage ổn định, ít tranh cãi
- get: list, detail, check
- post: create, trigger
- delete: hard/soft delete
→ đặt sau, không ảnh hưởng quyết định put/patch
