# lưu ý

## yêu cầu
- **nguyên tắc:** tư duy 20/80 20 nỗ lực tạo 80 kết quả, đơn giản hóa, đủ tốt để chạy (đủ tốt để chạy)
- **vai trò:** (áp dụng với dev, pm, po). với vai trò senior developer cần phải cứng rắn và đi thẳng vấn đề cần thực hiện
- **mục tiêu:** chỉ cần làm cho nó hoạt động
- **bước cần thực hiện phát triển:** tạo bảng liên quan => viết api (crud - từng chức năng một)=> kiểm thử => đánh giá + xác thực (mr) => triển khai
## thông tin chung
- khi chưa rõ, chưa đầy đủ điều kiện cần làm (môi trường, công cụ) chưa xác định, phân bổ được thời gian phát triển
- có được checklist rồi làm và hỏi từng bước 1, tránh hỏi dồn. chia nhỏ những vấn đề giải quyết thành do-check nhỏ
- đi từng chặng nhỏ một và hoàn thành nó để tới đích (vì quỹ thời gian)
## **code cập nhật**
- đơn giản hoá entity: bỏ icollection, bỏ [foreignkey], chỉ giữ trường fk để dễ thao tác db và hotfix.
- commit message viết tiếng anh.
- mô tả mr giữ ý chính và chỉ cần tóm tắt các thay đổi chính để reviewer xem diff cho nhanh.

---

# bước tiếp theo
- báo cáo hằng ngày cho anh Trưởng
- tổng quan
---
	promotion (pending)
	- 15–17: khóa nghiệp vụ (pending)
	- 18–20: chuyển sang kỹ thuật & triển khai (pending)
	17-22 (processing)
	- test chức năng và edge case test (master data và sale data)
	22-25: test risk skytransfer và tiếp tục cho promotion hiểu skycloud quản lý thông tin rk7 chưa làm được
---	

# trao đổi (đi thẳng vấn đề)

# 25-12-2025 – mapping dữ liệu ecom và skycloud + rk7
- đẩy dữ liệu promotion vào rk7 từ ecom để sử dụng lấy danh sách
- checklist:
+ xác định các bảng, thông tin api nào cần outbound rk7
+ vẽ sơ đồ luồng hoạt động code api đồng bộ tạo open discount ecom -> rk7


# 24-12-2025 – đọc hiểu skycloud quản lý thông tin rk7 (api, config, kết nối, fe, be)

# 23-12-2025 – làm rõ yêu cầu hệ thống và nghiệp vụ promotion

# 22-12-2025 – test risk skytransfer

---

# 20-12-2025 – (dự kiến - pending) sẵn sàng triển khai & phân tách ták

mục tiêu:
chuẩn bị đầy đủ điều kiện để bắt đầu coding và phân tách công việc.
checklist:
- rà soát lại toàn bộ nghiệp vụ & thiết kế
- phân tách task triển khai
- xác định tiêu chí hoàn thành (acceptance criteria)
- sẵn sàng bước sang giai đoạn implement

# 19-12-2025 – (dự kiến - pending) thiết kế luồng kỹ thuật & contract api
mục tiêu:
chuyển nghiệp vụ đã khóa thành thiết kế kỹ thuật rõ ràng, có thể implement.
checklist:
- thiết kế luồng kỹ thuật pos ↔ promotion engine
- xác định contract api (request / response)
- xác định cách xử lý lỗi, timeout, retry
- rà soát rủi ro kỹ thuật & hiệu năng

# 18-12-2025 – (dự kiến - pending) khóa nghiệp vụ & chuẩn bị thiết kế kỹ thuật
mục tiêu:
khóa các quyết định nghiệp vụ còn mở để đủ điều kiện thiết kế kỹ thuật.
checklist:
- làm việc với po/đầu mối nghiệp vụ để confirm các rule còn mơ hồ
- chốt các assumption nghiệp vụ còn lại
- xác định phạm vi triển khai kỹ thuật dựa trên nghiệp vụ đã khóa
- chuẩn bị đầu vào cho thiết kế api & kiến trúc

# 17-12-2025 – (promotion engine - pending) làm rõ input / output nghiệp vụ
mục tiêu:
xác định dữ liệu nghiệp vụ tối thiểu cần thiết để promotion engine tính toán và trả kết quả cho pos.
checklist:
- xác định input nghiệp vụ tối thiểu từ pos (bill, item, store, time…)
- xác định output promotion trả về cho pos (giảm tiền, quà, trạng thái)
- làm rõ rule ưu tiên, cộng dồn giữa các promotion
- tổng hợp danh sách câu hỏi cần po/đầu mối nghiệp vụ xác nhận


# 16-12-2025 – (promotion engine) làm rõ thời điểm kích hoạt & luồng pos
mục tiêu: làm rõ thời điểm pos gọi promotion engine và luồng nghiệp vụ khi áp dụng promotion lên bill.
checklist:
- làm rõ pos gọi promotion ở thời điểm nào (tạm tính / chốt bill)
- xác định luồng xử lý khi pos áp dụng promotion
- làm rõ hành vi khi không đủ điều kiện áp dụng promotion
- ghi nhận các điểm nghiệp vụ chưa được xác nhận

# 15-12-2025 – (Promotion Engine) làm rõ phạm vi & mục tiêu nghiệp vụ
mục tiêu: Xác định vai trò của promotion engine trong toàn bộ luồng ecom → skytransfer → POS và mục tiêu business cần đạt.
checklist:
- xác định promotion engine đứng ở đâu trong kiến trúc tổng thể
- làm rõ mục tiêu business của promotion (chốt bill, đồng bộ giá, ưu đãi POS)
- xác định phạm vi nghiệp vụ promotion engine chịu trách nhiệm
- liệt kê các giả định nghiệp vụ đang tồn tại

# 10-12-2025 - kiểm thử luồng hoạt động MasterData (Stores/Product/Prices/Combo) và SaleData (SaleTransaction và SaleEOD) để thông luồng hoạt động

# 09-12-2025 - (2)phối hợp với anh Hiệp sync chặt với nhau phần luồng giá – combo để chạy mượt
mục tiêu: phối hợp xử lý sync luồng giá - combo của master data
checklist:
- xác định phạm vi code
- xem luồng hiện tại kết hợp xem trên rk7 để xem combo hoạt động và tạo như thế nào (nguyên liệu cho sale data)
- vẽ sơ đồ luồng hoạt động (hiểu cấu trúc cách thực hiện business không có tài liệu - đọc và tự tìm hiểu)



# 08-12-2025 - phối hợp với anh Hiệp sync chặt với nhau phần luồng giá – combo để chạy mượt
mục tiêu: phối hợp xử lý sync luồng giá - combo của master data
checklist:
- xác định phạm vi code
- xem luồng hiện tại kết hợp xem trên rk7 để xem combo hoạt động và tạo như thế nào (nguyên liệu cho sale data)
- vẽ sơ đồ luồng hoạt động (hiểu cấu trúc cách thực hiện business không có tài liệu - đọc và tự tìm hiểu)
- hệ thống hóa các api tạo


# 05-12-2025 - (5)kiểm tra và so sánh khác biệt giữa cấu trúc phần mềm export xml và tài liệu mô tả sale data
mục tiêu: kiểm thử hoàn chỉnh lại luồng sale data => đi nhanh.
checklist:
non-function
- **thuật ngữ chuyên ngày f&b và pos**
- **thử nghiệm luồng tuần tự, đồng thời và song song**, cách nhận biết hệ thống
- xác thực thông tin các endpoint là môi trường gì (test hay prod)
networking
- cần nắm được thông tin chung việc anh hiệp làm, chủ động phối hợp để xác định việc đã, đang và sẽ làm
- có cần hỏi hay không? => (chưa cần - chưa nắm được)
- họp với qsr => mục combo và pricelist (4.4.4, 4.4.5 tài liệu docx) 	
subtask
- **test lại luồng sale data, vẽ sơ đồ luồng xử lý (process flow + activity diagram)**

# 04-12-2025 - (4)kiểm tra và so sánh khác biệt giữa cấu trúc phần mềm export xml và tài liệu mô tả sale data
mục tiêu: xác định đầu ra xml mà khách hàng cần (tài liệu mô tả).
checklist:
- đọc hiểu luồng code xác định phạm vi và đầu vào tạo xml nguồn dựa trên các store procedure
- kiểm thử với dữ liệu có sẵn trong db. phối hợp với anh Đầy cung cấp db backup


# 03-12-2025 - (3)kiểm tra và so sánh khác biệt giữa cấu trúc phần mềm export xml và tài liệu mô tả sale data
mục tiêu: làm rõ sự khác biệt giữa cấu trúc phần mềm khi export ra file xml và tài liệu mô tả sale data, từ đó xác định các điểm cần bổ sung hoặc điều chỉnh.
checklist:
- Đọc hiểu và xác định luồng tạo file xml nguồn + xlst => xml đích gửi erp (non function)
- trình bày lại giải pháp đó (cách thực hiện - cách hiểu)
- sơ đồ xử lý code (không cần đi vào chi tiết)


# 02-12-2025 - (2)kiểm tra và so sánh khác biệt giữa cấu trúc phần mềm export xml và tài liệu mô tả sale data
mục tiêu: làm rõ sự khác biệt giữa cấu trúc phần mềm khi export ra file xml và tài liệu mô tả sale data, từ đó xác định các điểm cần bổ sung hoặc điều chỉnh.
checklist:
- rà soát lflow và phạm vi source code đang xử lý sale data export, thu thập các file xml export.
- so sánh xml export mẫu với xml export: trường nào đã có, trường nào cần bổ sung

# 01-12-2025 - (1)kiểm tra và so sánh khác biệt giữa cấu trúc phần mềm export xml và tài liệu mô tả sale data
mục tiêu: làm rõ sự khác biệt giữa cấu trúc phần mềm khi export ra file xml và tài liệu mô tả sale data, từ đó xác định các điểm cần bổ sung hoặc điều chỉnh.
checklist:
- rà soát flow và mapping sale data hiện hành.
- thu thập và phân tích file xml export mẫu (hiện trạng).
- xác định phạm vi source code đang xử lý sale data.

# 28-11-2025 - làm rõ cơ chế đồng bộ từ data trung gian sang rk7
mục tiêu: làm rõ cơ chế đồng bộ để chuẩn bị viết api tạo mới promotion từ data trung gian sang rk7.
checklist:
- xác nhận cơ chế sync (là api sẽ gọi realtime sau khi lưu db hay chạy bằng background job)
- thu thập format tạo promotion của rk7 (payload, response xác định chính xác các field bắt buộc để gửi request tạo mới)
- xây dựng bảng mapping tối thiểu (chốt 3–5 trường quan trọng từ schema trung gian map sang rk7 (tên, % giảm, thời gian hiệu lực, mã sản phẩm…)
- xác định quy tắc xử lý lỗi (chốt cách ghi log, hành vi khi tạo fail, có cần retry hay chỉ ghi nhận lỗi)

# 27-11-2025 - tạo api nhận khuyến mãi từ ecom
mục tiêu: hoàn thiện api để nhận dữ liệu khuyến mại từ ecom và lưu vào database trung gian.
checklist:
- thiết kế api theo chuẩn webhook ecom (payload, response).
- triển khai api và kết nối với database trung gian.
- kiểm thử api với dữ liệu scheme-01 từ ecom.
- đẩy code và tạo merge request xác thực.
- (**chưa cần**) document api nếu cần cho các developer khác.

# 26-11-2025 - thêm các bảng từ payload ecom vào database trung gian
mục tiêu: cập nhật db trung gian để lưu trữ đầy đủ dữ liệu từ ecom.
checklist:
- tạo bảng/trường trong db trung gian dựa trên payload và yêu cầu đầu vào từ ecom.
- migrate tạo model trong code.
- (**bổ sung**) chuẩn bị cấu trúc dữ liệu để phục vụ api nhận dữ liệu khuyến mại từ ecom.

# 25-11-2025 - thực hiện tạo scheme-01 giảm giá sản phẩm (%) - round 1 từ ecom về database trung gian
mục tiêu: test luồng tích hợp của scheme-01 cho round 1, từ ecom về database trung gian.
checklist:
	- xem và kiểm tra payload/response của webhook ecom → api database trung gian cho round 1.
	- xác định các bảng/trường trong database trung gian cần dùng cho round 1.
	- tham khảo tài liệu liên quan đến scheme-01 và round 1.
	- chuẩn bị hoặc tạo các bảng/trường cần thiết trong database trung gian cho round 1.
	- (**chưa cần**) thực hiện kéo/hứng dữ liệu từ ecom về database trung gian cho round 1.
	- (**chưa cần**) thảo luận với người phụ trách trước khi commit code/checkout branch.
# 24-11-2025 - hiểu module đồng bộ khuyến mãi
mục tiêu: nắm tổng quan luồng hoạt động và tài liệu của module sync promotion.
checklist:
	- xem và tạo sơ đồ topology của module sync promotion.
	- hiểu luồng dữ liệu giữa ecom → db trung gian → rk7.
	- đọc hiểu tài liệu scheme nhóm và các biến thể.
	- xác định các tác nhân (người, service, hệ thống) tham gia vào luồng.
	- liệt kê quản lý task, checklist liên quan.