# mục tiêu
- in charge (phụ trách) vào module sync promotion (khuyến mãi đồng bộ hóa mô-đun) của dự án. sẽ làm việc closely (ở sau cùng)
- bbd document. focus vào các scheme của promotion (cơ chế khuyến mãi)
- đồng bộ khuyến mãi từ ecom sang rk7 để pos áp dụng đúng chính sách
- phạm vi: 4.4.6 - promotion sync
- giảm thiểu rủi ro nhất có thể, ban đầu không nhìn tổng quan về sau sẽ khắc phục sự cố


# thông tin tài liệu
hi @all
mọi người tham khảo document tích hợp với qsr và taptap nhé.

một số thông tin:
- đây là dự án khá lớn. ==tích hợp 2 chiều==
- gồm 2 phần:
+ erp: đồng bộ master-data và sales-data (phần này hiệp cover giúp anh)
+ order online: đồng bộ và xử lý đơn đơn hàng từ ecom web về skyorder/pos (phần này vinh và anh khương sẽ cover)
- qc: tâm châu

đây là bbd bên taptap làm. mình sẽ tham khảo tạm thời ở đây nhé:
https://docs.google.com/document/d/1zw0zm9dfhjjrk-4zchvbjkuxslf5ydzf/edit#heading=h.c2p732u297ql

# danh sách công việc cần làm
- hiểu dự án đang làm gì? phát triển mới module sync promotion (khuyến mãi đồng bộ hóa mô-đun) mới chỉ cưỡi ngựa xem hoa chưa rõ được hoạt động thực người dùng (chỉ hiểu sơ bộ về sơ đồ hoạt động)
- biết rõ vai trò và phạm vi công việc? đồng bộ khuyến mãi từ ecom sang rk7 để pos áp dụng đúng chính sách
- được cấp tài khoản nội bộ
- clone code + chạy được môi trường
- biết quy trình làm việc & người hỗ trợ
- nhận 1 task nhỏ để thực hành
- ghi chú lại tất cả thông tin quan trọng

# nội dung chính cần thực hiện
- xoay quanh các cơ chế khuyến mãi
- thiết lập môi trường, cấu hình cài cắm, các bên bộ phận tham gia
- các vấn đề thường gặp xảy ra và gây khó chịu khách hàng, nhân viên và cơ sở hạ tầng dữ liệu
	+ những gì cần giải quyết cấp thiết
	+ những gì đã sửa chữa rồi


# câu hỏi xoay quanh scheme promotion

## trước 
- các vấn đề đặt ra/giải quyết
- mapping master data giữa ecom → poss thế nào inbound/outbound
- danh sách test case bdd cho từng lỗi promotion

# ==vai trò nhiệm vụ==

## vấn đề chung 
- giám sát hoạt động promotion
- lệch 1 trường → sai giá → khách chửi, cửa hàng hoàn bill, finance sai số, audit gõ đầu, và PM thức trắng
## trách nhiệm
- ecom → promotion engine → pos
- luôn hiểu nhau, không hiểu sai, không hiểu lầm, không hiểu méo.
## bước thực hiện
- hiểu toàn bộ scheme, từ logic đến structure
- hiểu dòng chảy dữ liệu giữa các hệ thống
- hiểu cách viết và đọc bdd để test trước khi chạy thật
## yêu cầu ban đầu

### nắm 12 scheme promotion nhưng 4 vector cốt lõi 
- selector – chọn đối tượng 
- trigger – điều kiện kích hoạt
- benefit – giảm cái gì
- constraint – giới hạn, độ ưu tiên, số lần áp dụngs


## các câu hỏi
1.1 Cơ chế đồng bộ (Sync Flow)

•	đồng bộ theo thời điểm nào? 
•	khi đồng bộ thất bại thì retry như thế nào?


việc chính cần làm
	việc viết webhook crud là việc chắc chắn rồi em nhé. mình sẽ expose những endpoint này ra cho bên đối tác. phần này đọc tài liệu và viết model theo doc thôi

	còn việc nặng đó là
	- lưu data vào db trung gian
	- lấy data từ db trung gian đó map qua db của rk7 cho đúng

















