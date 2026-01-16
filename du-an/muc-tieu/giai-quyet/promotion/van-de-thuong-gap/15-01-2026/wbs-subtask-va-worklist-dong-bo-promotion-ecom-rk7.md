# mục tiêu
dựa trên tài liệu sơ đồ, task cho dev [tong-hop-cac-ticket.md] và prompt vạn năng tạo wbs rõ kết quả [prompt-van-nang-tao-wbs-ro-ket-qua.md] cần
- **1 → 5 là subtask của 1 task lớn**
- **mỗi mục có 1 tiêu đề tổng quát**
- **bên dưới là worklist rất cụ thể, đầu ra nhìn thấy được**
- **viết để pm copy dán thẳng vào clickup**
- **ngắn, sắc, không triết lý**
## các trạng thái công việc
[done]: đã hoàn thành
[inprogress]: đang xử lý hoặc xử lý 1 phần
[pending]: tạm dừng
[todo]: việc cần làm
[reject]: từ chối
---

## [1] ecom ⇄ skytransfer - webhook nhận promotion

- api endpoint nhận promotion giá mở từ ecom
- swagger / postman collection cho webhook
- validate payload + generate requestid
- lưu raw promotion + callbackurl vào db
- log trạng thái "received"
- dev test: call webhook bằng postman, verify db record + log theo requestid
---

## [2] skytransfer ⇄ skycloud - lưu promotion vào skycrm

- mapping promotion giá mở sang model crm
- api save promotion vào skycloud
- db record promotion trên skycrm
- response trả về promotionid
- log trạng thái "saved_to_crm"
- dev test: trigger flow từ [1], verify promotion xuất hiện trên crm + log
---

## [3] skytransfer ⇄ refagent - enqueue job xử lý promotion

- build payload job từ promotion crm
- api enqueue job sang refagent
- lưu jobid + requestid mapping
- log trạng thái "queued"
- response xác nhận enqueue thành công
- dev test: kiểm tra queue có job mới + mapping jobid đúng requestid
---

## [4] refagent ⇄ rk7 - đồng bộ promotion xuống rk7

- consume job từ queue
- mapping promotion giá mở sang rk7 schema
- call rk7 xml api insert/update promotion
- parse response trả về params cho refagent
- [pending]log trạng thái ("synced_to_rk7" hoặc "failed",...)
- dev test: verify promotion tồn tại trên rk7 hoặc log lỗi đúng case
---

## [5] refagent ⇄ skytransfer - callback kết quả xử lý

- build callback payload (success / fail)
- gọi callbackurl từ skytransfer
- retry callback theo policy nếu lỗi (refagent)
- cập nhật trạng thái cuối cùng trong db (skytransfer)
- log trạng thái "completed"
- dev test: giả lập success và fail, verify callback được nhận + trạng thái cuối
---

## ghi chú dùng cho pm

- mỗi mục là **1 subtask độc lập**, có thể giao cho 1 dev
- mỗi subtask demo được bằng api + log + db record
- chạy được v0 toàn luồng trước, chưa cần tối ưu
- requestid là chìa khóa trace xuyên hệ thống

bản này đúng kiểu:

- pm nhìn là biết giao việc
- dev nhìn là biết làm gì trong 1–3 tiếng
- qa nhìn là biết test ở đâu