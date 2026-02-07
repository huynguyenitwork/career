# sử dụng database sql server như camera an ninh dữ liệu

## mục tiêu dùng tài liệu
- nhìn db là biết chuyện gì vừa xảy ra
- audit toàn hệ thống mà không chạm app
- truy vết sai sót sau khi sự cố đã xảy ra

## tư duy cốt lõi
- db là nguồn sự thật cuối
- nếu db tự ghi lịch sử → app không cần biết
- giám sát tốt hơn can thiệp

## nguyên lý vận hành
- mỗi thay đổi dữ liệu = một dấu vết thời gian
- update / delete không mất dữ liệu cũ
- lịch sử được sql server tự lưu, tách khỏi bảng chính

## giá trị 20/80
- bật temporal → có lịch sử toàn bộ
- không trigger → không rủi ro logic ẩn
- không sửa code → không phá hệ thống đang chạy
- tra cứu sau sự cố → biết ai, khi nào, đổi cái gì

## luồng giám sát dữ liệu
- thao tác xảy ra
- db tự ghi phiên bản cũ
- bảng history tích lũy theo thời gian
- truy vấn lại bất kỳ mốc nào trong quá khứ

## phạm vi giám sát đạt được
- bảng nào vừa thay đổi
- dòng nào bị tác động
- cột nào bị sửa
- thời điểm chính xác

## quyết định thiết kế (loại sớm)
- cần audit toàn hệ thống → temporal
- cần can thiệp logic khi ghi → trigger (khác mục tiêu)
- chỉ cần log app → không đủ

## khi nào nên bật toàn db
- hệ thống nhiều người thao tác
- dữ liệu nhạy cảm, khó rollback
- cần truy trách nhiệm sau sự cố

## chi phí cần chấp nhận
- tốn thêm storage
- query history chậm hơn query live
- cần kỷ luật dọn history khi quá lớn

## kết luận hành động
- temporal table = camera an ninh thụ động
- bật trước khi có sự cố, không phải sau
- dùng để điều tra, không dùng để thay thế business logic
