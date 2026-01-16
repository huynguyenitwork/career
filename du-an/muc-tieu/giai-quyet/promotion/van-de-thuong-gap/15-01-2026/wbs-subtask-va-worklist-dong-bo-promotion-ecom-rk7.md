# mục tiêu
dựa trên tài liệu sơ đồ, task cho dev [tong-hop-cac-ticket.md] và prompt vạn năng tạo wbs rõ kết quả [prompt-van-nang-tao-wbs-ro-ket-qua.md] cần
- **1 → 5 là subtask của 1 task lớn**
- **mỗi mục có 1 tiêu đề tổng quát**
- **bên dưới là worklist rất cụ thể, đầu ra nhìn thấy được**
- **viết để pm copy dán thẳng vào clickup**
- **ngắn, sắc, không triết lý**

## timeline
- 16-01-2026: điều chỉnh lại flow giai đoạn từ skytransfer có 2 hướng => skycloud/refagent thành skytransfer=>skycloud=>refagent
- 15-01-2026: flow giai đoạn từ skytransfer có 2 hướng => skycloud/refagent

## các trạng thái công việc
[done]: đã hoàn thành
[inprogress]: đang xử lý hoặc xử lý 1 phần
[pending]: tạm dừng
[todo]: việc cần làm
[reject]: từ chối
---

## [1] ecom ⇄ skytransfer - webhook nhận promotion

* expose api webhook nhận promotion từ ecom (method, auth rõ ràng)
* define schema payload + validate mandatory fields
* generate requestid xuyên suốt cho toàn flow
* persist raw payload + callbackurl vào db (trace-first)
* ghi log trạng thái "received" kèm requestid
* dev test: postman gọi webhook, check db + log theo requestid

---

## [2] skytransfer ⇄ skycrm - lưu promotion vào skycrm

* map promotion giá mở sang crm model chuẩn
* implement api create/update promotion trên skycrm
* persist promotion record trên db crm
* trả response chứa promotionid + requestid
* ghi log trạng thái "saved_to_crm"
* dev test: trigger từ [1], verify crm record + log đúng promotionid

---

## [3.1] skycrm ⇄ refagent - enqueue job xử lý promotion

* build job payload từ promotion crm (id, params, requestid,...)
* call api enqueue job sang refagent
* lưu mapping promotionid ↔ jobid ↔ requestid
* ghi log trạng thái "queued"
* gọi callback api về skytransfer để thông báo enqueue success / fail
* dev test: check queue có job mới + mapping đúng requestid

---

## [3.2] skycrm ⇄ rk7 - đồng bộ promotion xuống rk7 (direct)

* map promotion crm sang rk7 schema
* call rk7 xml api insert/update promotion
* parse response rk7 (success / error code)
* gọi callback api về skytransfer với kết quả sync
* [pending] ghi log trạng thái "synced_to_rk7" hoặc "failed"
* dev test: verify promotion trên rk7 hoặc log lỗi đúng case

---

## [4.1] refagent ⇄ rk7 - đồng bộ promotion xuống rk7 (async)

* consume job promotion từ queue
* map payload job sang rk7 schema
* call rk7 xml api insert/update promotion
* parse response rk7 và normalize result
* [pending] ghi log trạng thái "synced_to_rk7" hoặc "failed"
* dev test: check rk7 data hoặc error log theo jobid

---

## [5.1] refagent ⇄ skytransfer - callback kết quả xử lý

* build callback payload theo chuẩn (success / fail)
* gọi callbackurl về skytransfer
* retry callback theo policy khi lỗi mạng / timeout
* update trạng thái cuối promotion trong db skytransfer
* ghi log trạng thái "completed"
* dev test: mock success & fail, verify callback + final status

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