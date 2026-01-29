# thử nghiệm tái cấu trúc service và repository để test nhanh, rủi ro thấp

## mục tiêu tài liệu
- bỏ code khỏi tài liệu → chỉ giữ tư duy, quyết định, ranh giới
- dùng để đọc nhanh, review nhanh, quyết nhanh
- tái chế cho test / dev / poc (proof of concept), không trôi sang production

---

## khối 1 — service gọi api dùng chung (skycloud)

### quyết định thiết kế
- tách "hợp đồng gọi api" khỏi implementation
- gom toàn bộ http + bearer token vào 1 chỗ
- service nghiệp vụ không chạm http, không chạm auth

### ranh giới rõ
- service này chỉ làm 1 việc: gọi api ngoài
- không chứa logic nghiệp vụ
- không chứa retry, cache, transform

### hệ quả đạt được
- mock dễ khi test
- đổi endpoint / auth không lan code
- tránh over-engineer sớm

### tiêu chí dùng / không dùng
- dùng khi nhiều service cần gọi cùng 1 api ngoài
- không dùng nếu chỉ gọi 1 endpoint đơn lẻ, 1 lần

---

## khối 2 — repository in-memory thay stored procedure (ecom promotion)

### quyết định thiết kế
- giữ service, đổi nguồn dữ liệu
- thay stored procedure bằng list trong ram
- mapping hành vi 1:1 với sql cũ

### ranh giới rõ
- service không biết db hay ram
- repository đại diện cho "nguồn dữ liệu"
- đổi nguồn = đổi di, không đổi logic

### lợi ích trực tiếp
- test không cần database
- rollback bằng cấu hình
- giảm thời gian setup môi trường

### tiêu chí dùng / không dùng
- dùng cho test / dev / poc
- không dùng cho multi-instance production
- không dùng khi cần transaction / persistence

---

## khối 3 — in-memory app storage thay in-memory database (parameter)

### quyết định thiết kế
- bỏ hoàn toàn dbcontext và ef
- dữ liệu sống trong bộ nhớ application
- cache vẫn nằm ở service, không đổi

### ranh giới rõ
- repository chỉ trả dữ liệu
- service chịu trách nhiệm cache
- storage không biết cache, cache không biết storage

### lợi ích trực tiếp
- kiểm soát dữ liệu 100%
- không lệch hành vi như ef in-memory
- debug và trace dễ

### tiêu chí dùng / không dùng
- dùng cho config, parameter, dữ liệu đọc nhiều
- không dùng cho dữ liệu cần ghi lâu dài
- không dùng khi scale ngang nhiều instance

---

## mẫu tư duy chung rút ra

### công thức
- giữ interface
- đổi implementation
- khóa hành vi
- đẩy rủi ro về cấu hình

### khi nào nên áp dụng
- cần đi nhanh nhưng không phá kiến trúc
- cần test logic độc lập môi trường
- cần poc để quyết định bước tiếp theo

### khi nào dừng
- khi bắt đầu cần persistence
- khi cần consistency giữa nhiều instance
- khi dữ liệu trở thành "state hệ thống"

---

## kết luận ngắn
- đây không phải tối ưu vĩnh viễn
- đây là bước đệm hợp lý để quyết định nhanh
- đúng bài cho test / dev / spike kỹ thuật
- đủ đúng để làm ngay, không sa đà hoàn hảo
