# checklist export sale data sang sap

## 0. điều kiện kiểm tra trước khi chạy
- đã xóa log xml đã gửi thành công trong `sap_interfaces`
- xác nhận cơ chế "lưu thành công" tồn tại → chưa rõ → dừng dev

## 1. khóa điều kiện chạy
- đúng thời gian → sai → không chạy
- đúng action export sale → sai → không chạy

## 2. khóa phạm vi xử lý
- lập lịch → `saledatataskscheduleservices`
- tạo xml sale + eod → `generatexmlservice`
- ngoài phạm vi này → loại

## 3. flow xuất dữ liệu (không rẽ nhánh)
- lấy ca trong 15 ngày chưa có trong `sap_interfaces`
- validate dữ liệu (đơn, món, giảm giá, thanh toán)
- thiếu dữ liệu → invalid → không gửi
- gom dữ liệu hợp lệ → tạo xml
- gửi xml → success hoặc fail
- ghi log + lưu lịch sử

## 4. quy tắc xử lý lỗi
- lỗi validate → dừng tại chỗ
- lỗi gửi → cho phép gửi lại
- không có log → coi như lỗi nghiêm trọng

## 5. công thức rà soát 5 phút
- ca này đã export chưa? → rồi → loại
- dữ liệu đủ không? → không → invalid
- gửi xong có dấu vết không? → không → bổ sung log
- lỗi này có ảnh hưởng 7–30 ngày không? → không → hoãn

## 6. điểm sống còn cần giữ
- chỉ export dữ liệu hợp lệ
- chỉ chạy đúng thời điểm
- kết quả luôn rơi vào 1 trong 2 trạng thái: success hoặc có log lỗi
