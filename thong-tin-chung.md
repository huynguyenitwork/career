
# thông tin sky
user/pass: dev/Dcorp@2025
## crm
host-fe-stg: https://stg-skyoffice.dcorp.com.vn
host-fe-dev: https://dev-skyoffice.dcorp.com.vn
host-be-stg: https://api-stg.dcorp.com.vn/crm/swagger/index.html
host-be-dev: https://api-dev.dcorp.com.vn/crm/swagger/index.html
### sql postgres crm
server: 192.168.2.151
port: 5432
database: SkyCRMDB
user: postgres
pass: Dcorp@2025
## masterdata
host-fe-stg: https://stg-skyoffice.dcorp.com.vn
host-fe-dev: https://dev-skyoffice.dcorp.com.vn
host-be-stg: https://api-stg.dcorp.com.vn/masterdata/swagger/index.html
host-be-dev: https://api-dev.dcorp.com.vn/masterdata/swagger/index.html

# thông tin connect qsr - sap
/sap-integration/
├─ inbound/   (qsr → sap)
├─ outbound/  (sap → qsr)

# kiểm tra ip public
lưu ý: 1 mạng chỉ có 1 ip public vì giới hạn tài nguyên địa chỉ trên toàn thế giới (giống như mỗi nhà sẽ có 1 địa chỉ duy nhất) các thiết bị/con người là trong hộ khẩu đó
## với powershell
(Invoke-WebRequest -Uri "https://api.ipify.org").Content
## với cmd
curl https://api.ipify.org

# thông tin về các nhánh
- sap-ecom = mảnh đất của đội SAP trong thế giới thương mại.
- qsr-ecom = mảnh đất của đội QSR trong thế giới thương mại.
=> không có chuyện nhánh là "đi từ đất này qua đất kia". mỗi thằng là một khu biệt thự riêng
# thông tin kết nối server

## r-keeper
- user/pass: RK7 22663/Phat!@#2003

## skytransfer

### RK7Server1
- server/post: 118.69.108.41/2323
- user/pass: HTTPAPI/1

### RK7Server2 (như RK7Server1)
- server/post: 118.69.108.41/2323
- user/pass: HTTPAPI/1

- apixml: https://118.69.108.41:2323/rk7api/v0/xmlinterface.xml
- xmlrq:
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetRefData" RefName="Restaurants" IgnoreEnums="1" WithChildItems="2" WithMacroProp="1" PropMask="items.(Name,Code,Status,Region,Concept,genECOMCODE,GUIDString,LocationLat,LocationLong)" />
</RK7Query>

## rk7

### pc server
server: 192.168.2.32
user/pass: Administrator/Dcorp@2025

### r-keeper
user/pass: admin/1

# giai đoạn dự án

## 1. kick-off
- mục tiêu: đồng bộ team, xác định scope, vai trò, timeline.
- 20/80 trọng tâm: ai làm gì + thời hạn quan trọng + mục tiêu dự án.
## 2. workshop
- mục tiêu: hiểu nhu cầu khách hàng & vạch giải pháp sơ bộ.
- trọng tâm: những yêu cầu chính, vấn đề cốt lõi cần giải quyết, rủi ro lớn.
## 3. phân tích & thiết kế hệ thống
- mục tiêu: chuyển yêu cầu thành blueprint kỹ thuật.
- trọng tâm: kiến trúc tổng thể, luồng dữ liệu chính, các module cốt lõi.
## 4. development (dev)
- mục tiêu: code & build hệ thống.
- trọng tâm: chức năng chính phải chạy trước, coding chuẩn, không bug nặng.
## 5. sit (system integration test)
- mục tiêu: kiểm thử tích hợp các module.
- trọng tâm: các chức năng chính hoạt động trơn tru, dữ liệu luân chuyển đúng, lỗi nghiêm trọng được fix.
## 6. uat (user acceptance test)
- mục tiêu: khách hàng xác nhận hệ thống đáp ứng yêu cầu.
- trọng tâm: các use-case chính hoạt động, ux chấp nhận được, lỗi nhỏ có thể fix sau.
## 7. go-live
- mục tiêu: đưa hệ thống vào vận hành thực tế.
- trọng tâm: hệ thống chạy ổn định, backup + support sẵn sàng, các issue nghiêm trọng được kiểm soát.

---

# thông tin cô lao công
tên: nguyệt
## khung giờ dọn dẹp
- chiều: 1h30p|2h00p
## khác
- giấy vệ sinh: thứ 2 đầu tuần

# thông tin cá nhân chia sẻ với nhân sự
- nơi ở: quận 7
- mức lương: 28, 29 (lương net, chưa bao gồm thuế và bhxh)

# công ty
- vị trí tuyển: https://www.topcv.vn/viec-lam/senior-net-dev-project-3-thang-di-lam-ngay/1947593.html?ta_source=jobsearchlist_linkdetail&u_sr_id=x6dlvypwfbcyid4eqlqhuf00xahholwgsjtx69em_1762919853
- yêu cầu
	- lập trình tích hợp dữ liệu giữa hệ thống pos của dcorp và hệ thống sap, ecom
	- thực hiện mapping & đồng bộ các master data: menu, sản phẩm, giá, cửa hàng…
	- gửi dữ liệu bán hàng chi tiết theo bill, theo store, theo ngày cho hệ thống erp
	- thiết kế các cơ chế monitoring để đảm bảo dữ liệu luôn đầy đủ – chính xác – đúng hạn
	- xây dựng các cơ chế xử lý lỗi & tự hồi phục (auto-healing) nếu xảy ra sự cố trong quá trình truyền dữ liệu giữa 2 hệ thống

# câu hỏi
– dự án pos x sap đang ở giai đoạn nào?
– vai trò của dev cụ thể? fix bug hay build mới?
– môi trường ci/cd, code review, quy trình deploy?
– làm onsite hay hybrid?
– tech stack chi tiết (redis? kafka? ef core?).

# lộ trình di chuyển
## chú quý - dcorp
- di chuyển
	[chú quý] -> lê văn lương -> (nguyễn văn linh) nguyễn hữu thọ -> khánh hội -> bến vân đồn -> cầu khánh hội -> tôn đức thắng -> đinh tiên hoàng -> cầu bông -> lê văn duyệt -> phan đăng lưu -> hoàng hoa thám -> [dcorp]
- thời gian (6g45p - 7g50p)
	7g00p (11.6km): 30p - 1g10p => 8g10p (tối đa)
	7g20p (11.6km): 35p - 1g15p => 8g35p (tối đa)
## dcorp - chú quý
	[dcorp] hoàng hoa thám -> phan đăng lưu -> lê văn duyệt -> cầu bông -> đinh tiên hoàng -> võ thị sáu -> phạm ngọc thạch -> alexandre de rhodes -> nam kỳ khởi nghĩa -> lê lợi -> trần hưng đạo -> phạm ngũ lão -> nguyễn thái học -> cầu ông lãnh -> hoàng diệu -> khánh hội -> nguyễn hữu thọ -> lê văn lương -> nguyễn văn linh -> lê văn lương -> [chú quý]
- thời gian (18g05p - 19g25p)
	18g00p  (12.1km): 40p - 1g20p => 19g20p (tối đa)
	18g20p (12.1km): 35p - 1g15p => 19g35p (tối đa)
	
## nhà riêng - dcorp (**đinh tiên hoàng** - 1 chiều)
- di chuyển
- thời gian (6g30p - 7g45p)
	7g00p (18.1km): 40p - 1g25p => 8g25p (tối đa)
	7g20p (18.1km): 40p - 1g25p => 8g45p (tối đa)
## dcorp - nhà riêng (**võ thị sáu** - 2 chiều)
- di chuyển
- thời gian (18g05p - 19g30p)
	18g00p (17.8km): 45p - 1g25p => 19g25p (tối đa)
	18g20p (17.8km): 45p - 1g25p => 19g40p (tối đa)
# thông tin offer

## thông tin trao đổi

### thông tin hợp đồng với sky x

- loại hợp đồng: dịch vụ (có thể chuyển sang chính thức sau 3 tháng)
  - nếu chia tay: kết thúc hợp đồng sau 3 tháng
  - nếu chuyển chính thức: bỏ qua thử việc 2 tháng

### lương

  - lương cơ bản: 28,5 triệu
  - lương đóng bhxh: 8,6 triệu
  - thực lĩnh: 25,9 triệu
  - nhận lương: vào tài khoản cá nhân, ngày 5 và 15 hàng tháng

### thử việc (đánh giá năng lực thực)

- 7 ngày đầu: hưởng 85% lương, không đóng bhxh
- giờ làm việc: thứ 2 – thứ 6, 8h – 18h, nghỉ trưa 11h45 – 13h
- ngày bắt đầu đi làm:

  - nên đến khoảng 9h (tránh quá sớm vì mọi người họp)
  - nhờ hỗ trợ mở cửa từ chị quản lý


## thông tin mail

### thời gian và địa điểm
- thời gian bắt đầu công việc: 9h00 sáng thứ hai, ngày 24/11/2025.
- địa điểm: công ty dcorp, 12/04 hoàng hoa thám, p7, quận bình thạnh, tp.hcm.
### thông tin về lương và hợp đồng
- lương chính thức: 28.500.000 đồng (gross/tháng), tương đương 25.800.000 đồng (net/tháng).
- lương thử việc 1 tuần: 85% lương chính thức, tính theo số ngày làm việc thực tế.
- hình thức hợp đồng: hợp đồng lao động 3 tháng (sau thử việc đạt yêu cầu).
- tham gia bhxh sau khi ký hợp đồng 3 tháng, đóng trên mức lương cơ bản 8.549.000 đồng.
### mô tả công việc chính
- lập trình tích hợp dữ liệu giữa hệ thống pos của dcorp và hệ thống sap, ecom.
- thực hiện mapping và đồng bộ các master data: menu, sản phẩm, giá, cửa hàng…
- gửi dữ liệu bán hàng chi tiết theo bill, theo store, theo ngày cho hệ thống erp.
- thiết kế các cơ chế monitoring để đảm bảo dữ liệu luôn đầy đủ, chính xác, đúng hạn.
- xây dựng các cơ chế xử lý lỗi và tự hồi phục (auto-healing) nếu có sự cố.
- thực hiện các công việc liên quan khác theo yêu cầu của quản lý.
### phương tiện và thời gian làm việc
- tự chuẩn bị laptop cá nhân và phương tiện đi lại.
- gửi xe máy tại sân tòa nhà dcorp/văn phòng khách hàng.
- thời gian làm việc: thứ hai đến thứ sáu. sáng: 08h00 – 11h45, chiều: 13h00 – 18h00.
### yêu cầu phản hồi
- điền thông tin theo đường link được cung cấp trước 22h00 thứ sáu ngày 21/11/2025.
- xác nhận qua email với nội dung: "em đồng ý với nội dung email & thư mời nhận việc".
### lưu ý
- không tiết lộ mức lương với đồng nghiệp (trừ nhân sự và quản lý trực tiếp).
