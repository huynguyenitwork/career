## vấn đề thường gặp

### rk7man bị ngắt kết nối
- do ref bị tắt. vào server 32 => run "C:\DAY_QC\QSR\bin\win\refsrv.exe - Shortcut.lnk"

## 1. truy cập hệ thống sky (dùng cho dev/test)

- user/pass chung: dev / Dcorp@2025

### domain skytransfer=>rk7

#### org_id
- dev: 8582
- stg: 8547
refagent: http://localhost:5901
skycrm: http://localhost:5001
#### run
skycrm: dev/stg
skytransfer: localhost
refagent: cloudflared

### crm
- fe-dev: https://dev-skyoffice.dcorp.com.vn
- fe-stg: https://stg-skyoffice.dcorp.com.vn
- be-dev (swagger): https://api-dev.dcorp.com.vn/crm/swagger/index.html
- be-stg (swagger): https://api-stg.dcorp.com.vn/crm/swagger/index.html

### masterdata
- fe-dev: https://dev-skyoffice.dcorp.com.vn
- fe-stg: https://stg-skyoffice.dcorp.com.vn
- be-dev (swagger): https://api-dev.dcorp.com.vn/masterdata/swagger/index.html
- be-stg (swagger): https://api-stg.dcorp.com.vn/masterdata/swagger/index.html

### database crm (postgres)
- server: 192.168.2.151:5432
- db: skycrmdb
- user/pass: postgres / Dcorp@2025

---

## 2. tích hợp qsr ↔ sap (scope kỹ thuật)

- path tích hợp: /sap-integration/
- inbound: qsr → sap
- outbound: sap → qsr
- mục tiêu: đồng bộ master data + dữ liệu bán hàng

---

## 3. kết nối r-keeper / rk7 (phục vụ tích hợp)

### skytransfer
- rk7 server: 118.69.108.41:2323
- user/pass: httpapi / 1
- api xml: https://118.69.108.41:2323/rk7api/v0/xmlinterface.xml

### rk7 pc server
- server ip: 192.168.2.32
- server name: SKYXQASERVER
- user/pass: administrator / Dcorp@2025

### r-keeper app
- user/pass: admin / 1

---

## 4. quy ước nhánh source

- sap-ecom: codebase của team sap
- qsr-ecom: codebase của team qsr
- nguyên tắc: mỗi nhánh là hệ riêng, không “đi xuyên đất”

---

## 5. vòng đời dự án (để định vị trạng thái hiện tại)

- kick-off: khóa scope, vai trò, timeline
- workshop: chốt nhu cầu + rủi ro chính
- phân tích & thiết kế: kiến trúc + luồng dữ liệu
- dev: build chức năng cốt lõi
- sit: test tích hợp end-to-end
- uat: khách hàng xác nhận
- go-live: vận hành thật + support

---

## 6. mô tả công việc dev (dùng để tự đánh giá fit)

- tích hợp pos ↔ sap ↔ ecom
- mapping & đồng bộ master data (menu, sản phẩm, giá, store)
- gửi sales data theo bill / store / ngày
- thiết kế monitoring dữ liệu
- xử lý lỗi + auto-healing

---

## 7. câu hỏi cần khóa trước khi nhận việc

- dự án pos × sap đang ở giai đoạn nào?
- dev tham gia build mới hay chủ yếu fix?
- quy trình ci/cd, code review, deploy?
- onsite hay hybrid?
- tech stack cụ thể (redis, kafka, ef core…)?

---

## 8. offer & điều kiện làm việc (để quyết định nhận/không)

- loại hợp đồng: dịch vụ 3 tháng → có thể lên chính thức
- lương gross: 28.500.000
- thực lĩnh ~25.9 triệu
- bhxh đóng trên 8.6 triệu
- trả lương: ngày 5 & 15
- thử việc: 7 ngày, 85% lương
- giờ làm: t2–t6, 8h–18h
- start: 9h00, thứ hai 24/11/2025
- lưu ý: không chia sẻ lương nội bộ

---

## 9. thông tin cần loại khỏi tài liệu làm việc

- thông tin lao công, giờ dọn dẹp
- lộ trình di chuyển cá nhân
- thông tin đời sống không liên quan dự án
- giải thích kiến thức phổ thông không phục vụ quyết định
