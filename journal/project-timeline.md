# lưu ý chung
- tắt cache khi test dev
- test theo quy trình + kịch bản bdd (happy path → edge/risk)
- time từ ecom dùng utc để tránh convert
- test local: dùng tzutil get/set/reset (```tzutil /g``` / ```tzutil /s "UTC"``` / ```tzutil /s "SE Asia Standard Time"```)
- skycloud không có timezone riêng → dùng timezone server
- khi lưu trữ: convert utc+7 → utc

# task pending
- ~~cập nhật trường mở rộng tại refagent~~ => rk7 (không cần)
- sửa sql skytransfer
- tạo danh sách testcase
- tạo checklist cấu hình vận hành (dev/prod)
- thiết kế callback nhận dữ liệu trên skytool (nhận từ refagent)
- thiết kế log quan sát delivery (không dùng ecomlog)
- tạo wbs để ước lượng thời gian demo

---

# w5

## 27-01-2026
- hướng dẫn quản lý vòng đời windows service bằng .bat [inbox\27-01-2026.md]
- tạo prompt wbs setup môi trường demo [inbox\27-01-2026.md]
- refactor kết nối refagent (dùng từ proj masterdata) và tạo mr

## 26-01-2026
- thêm synctaskid trong bảng ecompromotion skytransfer + khóa ngoại [script-them-cau-hinh-skycrm-vao-bang-parameters.md]
- tắt log tracking, chỉ dùng cho happy case staging

# w4

## 23-01-2026
- base repo sync, mở rộng async
- viết lại get / add / update / delete (skytransfer)

## 22-01-2026
- mô hình branch dev từ dcorp [m1-timeline.md]
- cập nhật migration db skycrm: skycrm-api\Libraries\Data\Migrations\Installation

## 21-01-2026
- ~~bỏ cấu hình masterdata không dùng~~ [script-them-cau-hinh-skycrm-vao-bang-parameters.md]
- bổ sung case sửa/xóa skytransfer => skycrm

## 20-01-2026
- lỗi json serializer system.text.json vs newtonsoft
- cấu hình kết nối đặt tại service sở hữu chiều kết nối, không đặt ở skytransfer

## 19-01-2026
- mô hình api trả ngay + background + callback (no retry) [skycrm-mo-hinh-api-tra-ngay-background-xu-ly-callback-no-retry.md]
- ~~bổ sung cột gensapcode~~ [script-them-cau-hinh-skycrm-vao-bang-parameters.md]
- heidi sql chặn alter table → dùng ssms
- thêm callbackurl trong ecompromotion [script-tao-bang-ecom-promotion.md]

---

# 16-01-2026
- cập nhật wbs promotion theo component diagram [wbs-subtask-va-worklist-dong-bo-promotion-ecom-rk7.md]
- ~~chỉnh script~~ [script-them-cau-hinh-skycrm-vao-bang-parameters.md]

# 15-01-2026
- thiết kế wbs promotion [wbs-subtask-va-worklist-dong-bo-promotion-ecom-rk7.md]
- tổng hợp ticket promotion [tong-hop-cac-ticket.md]
- prompt tạo wbs rõ kết quả [prompt-van-nang-tao-wbs-ro-ket-qua.md]
- sơ đồ tương tác service ecom => rk7 [diagram-lr.md]

# 14-01-2026
- phân tích log & trạng thái callback async [phan-tich-thiet-ke-log-trang-thai-async-callback-skytool-refagent.md]
- thiết kế payload callback [mau-thiet-ke-payload-callback-skytool-refagent.md]
- quyết định hướng callback (truyền trực tiếp, bỏ appsetting) [so-sanh-thiet-ke-callback-skytoo-refagent.md]

# 13-01-2026
- vẽ sequence bằng plantuml
- phân tích callback skytransfer ↔ refagent [skytranfer-goi-callback-du-lieu-tu-refagent.md]
- test convert json nested payload [JsonProofTest]
- báo cáo kết quả 2 tháng [bao-cao-ket-qua-cong-viec-sau-2-thang.md]

# 12-01-2026
- lộ trình job queue refagent [lo-trinh-xu-ly-job-queue-refagent.md]
- api spec refagent [refagent-api-specification-ban-dung-chung.md]
- quản lý tài liệu md theo timeline [quan-ly-tai-lieu-md-theo-timeline-voi-git.md]
- sketch luồng skytransfer => refagent [luong-tu-duy-cua-handler-discount-sketch-logic.md]

# 10-01-2026
- cơ chế handler & nhân bản handler [luong-tu-duy-cua-handler-discount-sketch-logic.md]
- cập nhật trạng thái promotion ecom (-1/1)

# 09-01-2026
- rule command-driven api cud [rule-command-driven-cho-api-cud-tu-ecom-rk7.md]
- làm rõ vòng đời sync [logic-thuc-te-toan-bo-he-thong-sync.md]
- định nghĩa lại cơ chế sync [logic-thuc-te-toan-bo-he-thong-sync.md]

# 08-01-2026
- design pattern và bài toán thực tế [design-pattern-va-cac-van-de-thuc-te-ma-no-giai-quyet.md]
- cơ chế job hệ thống [co-che-job-trong-he-thong-phan-mem-hien-dai.md]
- tổng hợp trao đổi anh khương [refagent-noi-dung-trao-doi-voi-anh-khuong.md]
- lưu ý timezone skycloud (utc+7 → utc)

# 07-01-2026
- class tham số dùng chung read model + dto [class-obj-tham-so-dung-chung-cho-read-model-va-dto-trong-service-trung-gian.md]
- phân biệt dto create/update và get [phan-biet-dto-create-update-va-model-tra-ve-cua-get-api.md]
- cơ chế put api [restful-api-co-che-cot-loi-va-cach-dung-dung.md]

# 06-01-2026
- tạo sketch local [sketch.md]

# 05-01-2026
- demo case create discount [demo-cases-create-discount-(happy-path-first).md]
- lỗi async list.foreach
- lỗi addscoped httpclient trong backgroundservice

---

# 31-12-2025
- quản lý request hoppscotch

# 30-12-2025
- làm rõ kỳ vọng đầu ra po [van-de-po-hoi-tien-do-nhung-ky-vong-dau-ra-khong-ro.md]
- encode query string [van-de-encode-query-string-trong-.net-core-2.1.md]
- lỗi lifetime service [van-de-cac-loi-di-lifetime-khi-chuyen-sang-in-memory-app-&-backgroundservice.md]

# 29-12-2025
- chuẩn hóa service skycloud [chuan-hoa-service-skycloud-dung-cho-toan-bo-rest-json.md]
- tối ưu lookup organization [van-de-lookup-organization-theo-ten-gay-cham-khi-sync-promotion.md]
- idempotency chống trùng promotion [van-de-trung-promotion-do-nguoi-dung-thao-tac-lap.md]
- script cấu hình skycrm [script-them-cau-hinh-skycrm-vao-bang-parameters.md]
- service skycloud tương đồng rk7
- bảo mật api skycrm (dev không dùng) [ban-chat-bao-mat-trong-api-sky-crm.md]
- cập nhật trường ecompromotion [script-tao-bang-ecom-promotion.md]
- sửa procedure open_discount [script-lay-ecom-promotion-chua-xu-ly-trang-thai-opendiscount-goi-skycrm.md]

# 26-12-2025
- chạy api bằng cli dotnet run
- lỗi grpc do thiếu masterdata-api
- wbs luồng đồng bộ mới (3 ngày) [luong-dong-bo-ket-noi-tam-thoi.md]
- lỗi backup db (pg_restore role)
- pending làm rõ promotion engine

# 25-12-2025
- script sql promotion ecom -> skytransfer

# 23-12-2025
- yêu cầu đồng bộ promotion ecom → pos
- cần setup skyoffice local để thử nghiệm
- promotion engine = decision service cho pos
