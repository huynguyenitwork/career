# 15-01-2026
- thiết kế wbs cho task promotion dựa trên sơ đồ component và task được giao [wbs-subtask-va-worklist-dong-bo-promotion-ecom-rk7.md]
- xây dựng bảng tổng hợp các ticket hiểu task promotion cần làm [tong-hop-cac-ticket.md]
- prompt vạn năng tạo wbs rõ kết quả [prompt-van-nang-tao-wbs-ro-ket-qua.md]
- thiết kế sơ đồ tương tác giữa các service req/res ecom => rk7 (dùng component diagram) [diagram-lr.md]
# 14-01-2026
- phân tích thiết kế log & trạng thái async callback skytool ↔ refagent [phan-tich-thiet-ke-log-trang-thai-async-callback-skytool-refagent.md]
- thiết kế mẫu payload callback skytool => refagent [mau-thiet-ke-payload-callback-skytool-refagent.md]
- thiết kế hướng xử lý callback từ skytool => refagent đưa quyết định phù hợp (2 cách, truyền callback ngay khi gọi từ skytool | ~~thiết kế cấu hình appsetting cho refagent~~) [so-sanh-thiet-ke-callback-skytoo-refagent.md]
# 13-01-2026
- vẽ sequence dạng plantuml bằng vscode+extension plantuml diagram as code nhàn hơn nhiều không xa đà sơ đố quá 10s
- skytranfer gọi callback dữ liệu từ refagent thế nào? [skytranfer-goi-callback-du-lieu-tu-refagent.md]
- test phần chuyển đổi dữ liệu TPayload từ api agent lỗi do converter sai json thiếu convert nếu json nest 2 cấp trở lên dự án [JsonProofTest]
- báo cáo kết quả công việc sau 2 tháng làm việc [bao-cao-ket-qua-cong-viec-sau-2-thang.md]
# 12-01-2026
- **lộ trình xử lý job queue** refagent [lo-trinh-xu-ly-job-queue-refagent.md]
- tài liệu đặc tả api refagnet request từ api => tới payload cho job queue handler [refagent-api-specification-ban-dung-chung.md]
- quản lý tài liệu md dcorp các dự án theo timeline với git [quan-ly-tai-lieu-md-theo-timeline-voi-git.md]
- thực hiện luồng viết tay sketch skytransfer => refagent [luong-tu-duy-cua-handler-discount-sketch-logic.md]
# 10-01-2026
- hiểu sơ lược về cách nhân bản handler và các bước xử lý của handler (handler xử lý thay worker như thế nào) [luong-tu-duy-cua-handler-discount-sketch-logic.md]
- bổ sung cập nhật trạng thái cho promotion ecom (-1/1 = reject/done)
# 09-01-2026
- rule command-driven cho api create / update / delete từ ecom → rk7 [rule-command-driven-cho-api-cud-tu-ecom-rk7.md]
- thảo luận anh tính làm rõ vòng đời của luồng sync từ khi tạo đến kết thúc giữa 2 hệ thống khác nhau/cùng nhau thì dùng driven như nào [logic-thuc-te-toan-bo-he-thong-sync.md]
- định nghĩa lại nhiệm vụ/cơ chế hoạt động cốt lõi của sync [logic-thuc-te-toan-bo-he-thong-sync.md]
# 08-01-2026
- design-pattern sinh ra để chữa "nỗi đau" thực tế nào và các biến thể khác nhau của từng nhóm [design-pattern-va-cac-van-de-thuc-te-ma-no-giai-quyet.md]
- vấn đề dù thế giới có hàng ngàn loại "job", tất cả chỉ là biến thể của cùng một cơ chế cốt lõi [co-che-job-trong-he-thong-phan-mem-hien-dai.md]
- tổng hợp lại nội dung trao đổi với anh Khương [refagent-noi-dung-trao-doi-voi-anh-khuong.md]
- trên skycloud không có cài đặt timezone => timezone là ăn theo server nếu lưu trữ cần convert UTC+7 => UTC
# 07-01-2026
- class tham số dùng chung cho read model và dto trong service trung gian [class-obj-tham-so-dung-chung-cho-read-model-va-dto-trong-service-trung-gian.md]
- trong thiết kế restful api, create/update và get phục vụ hai mục đích khác nhau. đầu ra của hàm get và đầu vào của hàm create/update nên đặt thế nào phù hợp [phan-biet-dto-create-update-va-model-tra-ve-cua-get-api.md]
- hiểu luồng xử lý api cập nhật (put api) tạsi sao đầu vào cần nhiều trường thậm chí là gần toàn bộ entity. nếu tham số là rỗng sẽ đặt rỗng đối với thuộc tính của entity. tại sao không phải là nếu không truyền tham số thì sẽ không đặt giá trị **[restful-api-co-che-cot-loi-va-cach-dung-dung.md]**
# 06-01-2026
- tạo sketch và lưu tại vscode vì có local history [sketch.md]
# 05-01-2026
- yêu cầu bổ sung từ anh trưởng [demo-cases-create-discount-(happy-path-first).md]
- ~~các trường hợp người dùng gặp phải khi tạo discount và demo [demo-cases-create-discount-(happy-path-first).md]~~
- không cần thiết lập discount group id vì trong discount đã có rồi [script-them-cau-hinh-skycrm-vao-bang-parameters.md]
- lỗi async bên trong List.ForEach = chạy ngầm không được chờ → scope bị hủy → dbcontext bị dispose → lỗi runtime (không dùng List.ForEach cho async-await)
- lỗi AddScoped HttpClient chỉ gọi api 1 lần trong backgroudservice

–--

# 31-12-2025
- di chuyển request trong hoppscotch là không thấy chỉ cần thêm mới thư mục và nhân bản từ collection khác qua
# 30-12-2025
- po hỏi tiến độ nhưng kỳ vọng đầu ra không rõ ràng, cần xác nhận lại (xác định vấn đề và dựa trên tài liệu clipup để đưa ra kết quả kỳ vọng đúng) [van-de-po-hoi-tien-do-nhung-ky-vong-dau-ra-khong-ro.md]
- vấn đề về định dạng nội dung format nội dung url để lấy dữ liệu (**form urlencoded** hay **uri encoding**) [van-de-encode-query-string-trong-.net-core-2.1.md]
- vấn đề về việc đăng ký service dạng scope/transident/singleton [van-de-cac-loi-di-lifetime-khi-chuyen-sang-in-memory-app-&-backgroundservice.md]

# 29-12-2025
- chuẩn hóa service skycloud chức năng đọc từ cache/crud dùng cho toàn bộ rest json (req/res) [chuan-hoa-service-skycloud-dung-cho-toan-bo-rest-json.md]
- vấn đề lookup organization theo tên gây chậm khi sync promotion và giải pháp tăng latency bằng cache (chặn đầu) [van-de-lookup-organization-theo-ten-gay-cham-khi-sync-promotion.md]
- vấn đề trùng promotion do người dùng thao tác lặp và giải pháp idempotency bằng cache (chặn đầu) [van-de-trung-promotion-do-nguoi-dung-thao-tac-lap.md]
- script thêm cấu hình skycrm vào bảng parameters [script-them-cau-hinh-skycrm-vao-bang-parameters.md]
- tạo service skycloud tương đồng như rk7 [tao-service-skycloudservice-co-interface-co-get-post-put-delete-.net-core-2.1-c#-7.3.md]
- kiểm tra xem skycrm api dùng xác thực và bảo mật nào (useauthentication/useauthorization)? [ban-chat-bao-mat-trong-api-sky-crm.md] => **tạm thời không dùng bảo mật thực hiện dev trước** (với access token)
- thử thêm các param thông qua api put/get skytransfer (chỉ lấy/cập nhật). trao đổi anh tính/hiệp giải đáp thắc mắc 2 option thêm parameters
- cập nhật thêm trường cho ecompromotion (created/updated/processstatus) [script-tao-bang-ecom-promotion.md]
- sửa lại procedure kiểm tra promotion đang chờ xử lý từ ecom cho loại promotion là open_discount [script-lay-ecom-promotion-chua-xu-ly-trang-thai-opendiscount-goi-skycrm.md]

# 26-12-2025
- chạy 2 api masterdata-api và skycrm-api mà không dùng nhiều màn hình vs thì chạy với cli ```dotnet run --project <path project>```
- **không gọi được grpc** trong crm (cần chạy project masterdata-api)
- wbs thời gian xử lý với anh trưởng theo luồng mới (dự kiến 3 ngày), cần trao đổi thêm anh khương để có được api dạng queue cho promotion gởi tới rk7 cần **đăng ký kết nối ref agent** [luồng đồng bộ](luong-dong-bo-ket-noi-tam-thoi.md)
- backup database bị lỗi (pg_restore: error: could not execute query: error: role "dcorp_dev" does not exist)
- hỏi anh tính cơ chế hoạt động promotion engine theo như yêu cầu điều chỉnh từ anh trưởng [pending]
# 25-12-2025
- script sql dành cho promotion thiết lập từ ecom -> skytransfer

# 23-12-2025
- bây giờ tôi cần đồng bộ dữ liệu promotion từ ecom sang máy pos để có thể sử dụng. để mà người dùng có thể lấy thông tin master data/rule/validate áp dụng promotion cho pos thì cần lấy thông tin và dữ liệu tính toán từ skyoffice. vì vậy tôi cần setup môi trường skyoffice trên máy local để tìm hiểu và thử nghiệm tích hợp, do đó cần anh nào đó cung cấp thông tin source code/db và cách cấu hình ban đầu để có thể sử dụng promotion trên skyoffice
- promotion engine trong mô hình ecom → service trung gian → rk7 (pos) vai trò nhiệm vụ gì? => là decision service cho pos call api