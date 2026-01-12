# điều kiện kiểm tra
- xóa nhật ký kết quả đầu ra xml đã được gửi đi cho khách [SAP_INTERFACES] (xác nhận đã gửi thành công) 
- kiểm tra lưu thành công (**TODO**)

# quy trình export dữ liệu sale sang SAP

## điều kiện cần
- đúng thời gian
- đúng hành động (xuất dữ liệu sale)

## phạm vi
- **lập lịch chạy tự động**: `saledatataskscheduleservices`
- **tạo file xml dữ liệu sale và eod**: `generatexmlservice`

## quy trình làm việc
1. **lấy ca chưa export**  
   - kiểm tra 15 ngày trước  
   - chưa có trong `sap_interfaces`
2. **xác thực dữ liệu**  
   - kiểm tra: đơn, món, giảm giá, thanh toán  
   - đánh dấu invalid nếu thiếu thông tin
3. **chuẩn bị gửi file xml**  
   - gom dữ liệu hợp lệ
4. **gửi file + đánh dấu kết quả**  
   - hoàn thành hoặc thất bại (có thể gửi lại nếu lỗi)
5. **lưu trữ lịch sử**  
   - đối soát dữ liệu, lưu log để kiểm tra sau

## lộ trình tổng quát
- **lấy ca chưa export → xác thực dữ liệu → tạo file xml → gửi → lưu lịch sử**

## điểm quan trọng
- dữ liệu đầy đủ và đúng thời gian  
- kết quả: gửi thành công hoặc log lỗi