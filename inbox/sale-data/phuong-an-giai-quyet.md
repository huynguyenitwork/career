# xlst => xml
- xslt là công thức: không tự sinh dữ liệu, chỉ biến xml nguồn thành xml đầu ra theo quy tắc.
- cách hoạt động: xslt quét xml nguồn, khớp template, lặp qua các phần tử, đổi tên hoặc thêm giá trị cố định.
- cách dùng: có xml nguồn + xslt → chạy bộ xử lý (python, saxon, xsltproc…) → ra xml đầu ra.

# mục tiêu so sánh xml export với tài liệu sale data

### 1. mục tiêu

xác định các trường, segment, dữ liệu thiếu hoặc sai trong xml export hiện tại so với yêu cầu sale data chuẩn, để chỉnh sửa và tạo xml hợp lệ gửi hệ thống nhận.

### 2. đầu vào

- **xml export hiện tại**: file xml do hệ thống pos/erp hoặc xslt tạo ra.
- **tài liệu sale data chuẩn**: định nghĩa các segment, trường bắt buộc, optional, kiểu dữ liệu, thứ tự.

### 3. đầu ra

- **danh sách chênh lệch / gap**: các trường hoặc segment thiếu, sai tên, sai kiểu dữ liệu, sai thứ tự.
- **xml chuẩn**: xml đã được điều chỉnh, hợp lệ theo tài liệu sale data.

### 4. điều kiện cần

- có xml export hiện tại.
- có tài liệu sale data chuẩn.
- công cụ hoặc phương pháp so sánh (script, excel, validator).
- hiểu rõ các segment quan trọng (transaction, lineitem, payment…).

### 5. điều kiện đủ

- so sánh đầy đủ giữa xml export và chuẩn.
- xác định các trường thiếu hoặc sai.
- có phương án điều chỉnh (sửa nguồn dữ liệu, xslt, mapping).
- xml đầu ra thử nghiệm hợp lệ theo chuẩn.

### 6. luồng thực hiện

1. lấy xml export hiện tại.
2. lấy tài liệu sale data chuẩn.
3. so sánh cấu trúc và dữ liệu (segment, trường, thứ tự, kiểu).
4. ghi nhận các điểm thiếu hoặc sai.
5. điều chỉnh xml nguồn/xslt/mapping.
6. xuất xml mới → kiểm tra hợp lệ.
7. xml chuẩn → gửi lên hệ thống nhận.



# mục tiêu so khớp xml đích và xslt (lỗi thời)

## mục tiêu

kiểm tra nhanh file XML có khớp với template XSLT hay không, không cần dò từng dòng.

## cách làm 20/80

1. dùng công cụ chạy thử XSLT với XML.
2. nếu chạy thành công và có output → mapping đúng.
3. nếu báo lỗi hoặc output trống → sai tên tag, sai XPath, thiếu trường, sai cấp cha.
4. không cần so thủ công, chỉ dựa trên báo lỗi để biết chỗ thiếu/sai.

## công cụ đề xuất

- XSLT Tester (linangdata.com/xslt-tester): chạy XSLT trực tiếp, báo lỗi rõ.
- EasyCodeForAll TestXSLT (easycodeforall.com/TestXSLT.jsp): hỗ trợ XSLT 1.0, xem output nhanh.

## checklist

1. xslt chạy được không?
2. các nhóm dữ liệu chính có output không? (DiscTotal, PaymentTotal, Sale, SaleTotal, TaxTotal)
3. lỗi hoặc field thiếu là gì?

## kết luận

chỉ cần chạy xslt trên xml bằng một trong hai tool trên. nếu có lỗi → bạn biết ngay field nào sai/thiếu mà không phải kiểm tra mắt.
