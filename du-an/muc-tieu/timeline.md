# vấn đề
## mục tiêu và timeline 1 

- đầu tiên giải đáp cho tôi việc mapping giữa data trung gian và data rk7 cần những gì?
ví dụ trên rk7 có việc tạo promotion dựa trên giao diện r-keeper và xử lý nó rồi. bây giờ làm thế nào để có thể từ mapping data trung gian vào data rk7 với cơ chế tương tự?
- có lẽ tôi nên đi từ từng schema 1 để thực hiện quy trình và sau đó mở rộng?
- bây giờ với 1 schema tôi cần biết: 
	- checklist cần thực hiện 
	- wbs 
	- các câu hỏi cần hỗ trợ thông tin và phối hợp (như api, database trung gian, database rk7,...) đặt vấn đề trước?
## mục tiêu và timeline 2

- chạy ứng dụng .net core thế nào trong vscode? migrate dữ liệu ra sao? gọi web api? (chỉ dùng với .netcore2.x cả ef và core)

## hỏi đáp

em đang muốn mapping 1-1 từ db trung gian sang db rk7 theo cách tạo promotion trên r-keeper như sáng anh có tạo. 
em đang thực hiện 1 end-to-end trường hợp đầu tiên là **Scheme-01** Giảm giá sản phẩm theo % ở tài liệu. 
ví dụ Giảm giá 50% cho Nhóm sản phẩm Pizza Chay, Truyền thống, …  tối đa 100.000VND
thì em cần :
- api test r-keeper cho chức năng này gồm payload và response thế nào
- database hoặc thông tin database rk7 để biết dữ liệu lưu trữ, các bảng thế nào
- tài liệu tham khảo
- db trung gian để có các trường, bảng tương ứng (hoặc tạo)

## tham khảo thêm

- đồng bộ dữ liệu từ db trung gian lên rk7. xem RK7 đáp ứng được những scheme nào, rồi lên list xử lý từng cái.
- chuẩn hóa danh sách