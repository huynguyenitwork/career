# lưu ý chung
- tắt cache để test dev
- test theo quy trình các bước thực hiện và các kịch bản test theo bdd (happy path -> risk/edge case)
- yêu cầu đầu vào truyền từ ecom đối với time là dạng utc. để không cần phải convert (để test local cần get/set/reset cli: ```tzutil /g```/```tzutil /s "UTC"```/```tzutil /s "SE Asia Standard Time"```). **trên skycloud không có cài đặt timezone => timezone là ăn theo server nếu lưu trữ cần convert UTC+7 => UTC**

# task pending
- ~~cập nhật thêm các trường mở rộng tại refagent~~ => rk7 (không cần vì anh Đầy bảo, validate từ cloud/midserver không phải từ RK7)
- sửa lại sql skytransfer
- tạo danh sách testcase
- tạo checklist cấu hình từng bước thực hiện hoạt động vận hành (dev/prod)
- thiết kế callback nhận dữ liệu trên skytool (nhận từ refagent)
- thiết kế log để quan sát hành vi/hoạt động delivery dữ liệu (thay vì ecomlog - chỉ coi hoạt động api)
- wbs cần có để có thời gian dự kiến demo đúng
–--

# 15-01-2026
- chỉnh sửa lại script [script-them-cau-hinh-skycrm-vao-bang-parameters.md]
- thiết kế wbs cho task promotion dựa trên sơ đồ component và task được giao [wbs-subtask-va-worklist-dong-bo-promotion-ecom-rk7.md]
- xây dựng bảng tổng hợp các ticket hiểu task promotion cần làm [tong-hop-cac-ticket.md]
- prompt vạn năng tạo wbs rõ kết quả [prompt-van-nang-tao-wbs-ro-ket-qua.md]
- thiết kế sơ đồ tương tác giữa các service req/res ecom => rk7 (dùng component diagram) [diagram-lr.md]
# 14-01-2026
- **lộ trình xử lý job queue** refagent [lo-trinh-xu-ly-job-queue-refagent.md]
- phân tích thiết kế log & trạng thái async callback skytool ↔ refagent [phan-tich-thiet-ke-log-trang-thai-async-callback-skytool-refagent.md]
- thiết kế mẫu payload callback skytool => refagent [mau-thiet-ke-payload-callback-skytool-refagent.md]
- thiết kế hướng xử lý callback từ skytool => refagent (2 cách, truyền callback ngay khi gọi từ skytool|thiết kế cấu hình appsetting cho refagent) [so-sanh-thiet-ke-callback-skytoo-refagent.md]
# 13-01-2026
- vẽ sequence dạng plantuml bằng vscode+extension plantuml diagram as code nhàn hơn nhiều không xa đà sơ đố quá 10s
- skytranfer gọi callback dữ liệu từ refagent thế nào? [skytranfer-goi-callback-du-lieu-tu-refagent.md]
- ~~**lộ trình xử lý job queue** refagent [lo-trinh-xu-ly-job-queue-refagent.md]~~
- test phần chuyển đổi dữ liệu TPayload từ api agent lỗi do converter sai json thiếu convert nếu json nest 2 cấp trở lên dự án [JsonProofTest]
- báo cáo kết quả công việc sau 2 tháng làm việc [bao-cao-ket-qua-cong-viec-sau-2-thang.md]
# 12-01-2026
- ~~**lộ trình xử lý job queue** refagent [lo-trinh-xu-ly-job-queue-refagent.md]~~
- tài liệu đặc tả api refagnet request từ api => tới payload cho job queue handler [refagent-api-specification-ban-dung-chung.md]
- quản lý tài liệu md dcorp các dự án theo timeline với git [quan-ly-tai-lieu-md-theo-timeline-voi-git.md]
- thực hiện luồng viết tay sketch skytransfer => refagent [luong-tu-duy-cua-handler-discount-sketch-logic.md]
# 10-01-2026
- hiểu sơ lược về cách nhân bản handler và các bước xử lý của handler (handler xử lý thay worker như thế nào) [luong-tu-duy-cua-handler-discount-sketch-logic.md]
- bổ sung cập nhật trạng thái cho promotion ecom (-1/1 = reject/done)
- bổ sung các test cases cho luồng thêm/sửa/xóa chiều từ ecom -> skycloud [sketch-so-do.md]. bản demo test cases anh Trưởng [happy-case.xlsx]
# 09-01-2026
- rule command-driven cho api create / update / delete từ ecom → rk7 [rule-command-driven-cho-api-cud-tu-ecom-rk7.md]
- kim chỉ nam thiết kế hệ thống hiện đại [kim-chi-nam-thiet-ke-he-thong-hien-dai.md]
- thảo luận anh tính làm rõ vòng đời của luồng sync từ khi tạo đến kết thúc giữa 2 hệ thống khác nhau/cùng nhau thì dùng driven như nào [logic-thuc-te-toan-bo-he-thong-sync.md]
- định nghĩa lại nhiệm vụ/cơ chế hoạt động cốt lõi của sync [logic-thuc-te-toan-bo-he-thong-sync.md]
# 08-01-2026
- tạo csdl qsrref (postres) trên server 192.168.2.32 và bảng logbook để test log connection
- design-pattern sinh ra để chữa "nỗi đau" thực tế nào và các biến thể khác nhau của từng nhóm [design-pattern-va-cac-van-de-thuc-te-ma-no-giai-quyet.md]
- tổng hợp lại nội dung trao đổi với anh Khương [refagent-noi-dung-trao-doi-voi-anh-khuong.md]
- bổ sung ghi nhận danh sách cửa hàng áp dụng promotion
- trên skycloud không có cài đặt timezone => timezone là ăn theo server nếu lưu trữ cần convert UTC+7 => UTC
=> đọc hiểu luồng hoạt động và xây dựng api nhận request từ skytranfer
# 07-01-2026
- chuyển AutoMapper -> dạng mapper manual (run-first)
- thảo luận với anh Khương về sourcecode và cách xây dựng từ nhánh (feat/ref-agent-ggg) cho tích hợp đầu cuối crm -> rk7 (cầu agent)
- **bổ sung thêm package AutoMapper** mapper 2 đối tượng cùng thuộc tính khác tên class, **khai báo trong startup** và **sử dụng** [automapper-10.1.1-csharp-7.3-net-core-2.1-asp.net-web-api.md]
- class tham số dùng chung cho read model và dto trong service trung gian [class-obj-tham-so-dung-chung-cho-read-model-va-dto-trong-service-trung-gian.md]
- trong thiết kế restful api, create/update và get phục vụ hai mục đích khác nhau. đầu ra của hàm get và đầu vào của hàm create/update nên đặt thế nào phù hợp [phan-biet-dto-create-update-va-model-tra-ve-cua-get-api.md]
- hiểu luồng xử lý api cập nhật (put api) tại sao đầu vào cần nhiều trường thậm chí là gần toàn bộ entity. nếu tham số là rỗng sẽ đặt rỗng đối với thuộc tính của entity. tại sao không phải là nếu không truyền tham số thì sẽ không đặt giá trị **[restful-api-co-che-cot-loi-va-cach-dung-dung.md]**
# 06-01-2026
- thực hiện yêu cầu bổ sung từ anh trưởng 2,3 [demo-cases-create-discount-(happy-path-first).md]
- tạo sketch và lưu tại vscode vì có local history [sketch.md]
# 05-01-2026
- yêu cầu bổ sung từ anh trưởng [demo-cases-create-discount-(happy-path-first).md]
- ~~các trường hợp người dùng gặp phải khi tạo discount và demo [demo-cases-create-discount-(happy-path-first).md]~~
- ~~không cần thiết lập discount group id vì trong discount đã có rồi [script-them-cau-hinh-skycrm-vao-bang-parameters.md]~~
- lỗi async bên trong List.ForEach = chạy ngầm không được chờ → scope bị hủy → dbcontext bị dispose → lỗi runtime (không dùng List.ForEach cho async-await) 
- cập nhật trạng thái processstatus của ecompromotion là hoàn thành
- lỗi addscoped httpclient chỉ gọi api 1 lần trong backgroudservice

–--

# 31-12-2025
- thử nghiệm cập nhật trạng thái discount group từ xóa => nháp (dto chỉ gồm id, status)
- di chuyển request trong hoppscotch là không thấy chỉ cần thêm mới thư mục và nhân bản từ collection khác qua
- bổ sung thêm parameters lấy các thông tin id của orgs và discountgroups dựa trên key là code thay vì dùng name [script-them-cau-hinh-skycrm-vao-bang-parameters.md]
# 30-12-2025
- vẽ lại sơ đồ logic code drawio theo 3 dạng khác nhau theo cách tiếp cận **diagram as code** [ve-lai-logic-cua-so-do-tiep-can-diagram-as-code.md]
- po hỏi tiến độ nhưng kỳ vọng đầu ra không rõ ràng, cần xác nhận lại (xác định vấn đề và dựa trên tài liệu clipup để đưa ra kết quả kỳ vọng đúng) [van-de-po-hoi-tien-do-nhung-ky-vong-dau-ra-khong-ro.md]
- vấn đề về định dạng nội dung format nội dung url để lấy dữ liệu (**form urlencoded** hay **uri encoding**) [van-de-encode-query-string-trong-.net-core-2.1.md]
- vấn đề về việc đăng ký service dạng scope/transident/singleton [van-de-cac-loi-di-lifetime-khi-chuyen-sang-in-memory-app-&-backgroundservice.md]
- tạo service lấy thông tin ecompromotion dữ liệu từ ecom -> skytransfer bằng cách sử dụng **in-memory app** thay vì dùng **in-memory database** [ecom-promotion-chuyen-tu-in-memory-database-sang-in-memory-app-storage.md]
- tạo service lấy thông tin parameter và cache bằng cách sử dụng **in-memory app** thay vì dùng **in-memory database** [parameter-cache-chuyen-tu-in-memory-database-sang-in-memory-app-storage.md]
- tạo playground test api skytransfer -> skycloud.

# 29-12-2025
- quy trình dành cho nhà phát triển phần mềm [quy-trinh-danh-cho-nha-phat-trien-phan-mem.md]
- chuẩn hóa service skycloud chức năng đọc từ cache/crud dùng cho toàn bộ rest json (req/res) [chuan-hoa-service-skycloud-dung-cho-toan-bo-rest-json.md]
- vấn đề lookup organization theo tên gây chậm khi sync promotion và giải pháp tăng latency bằng cache (chặn đầu) [van-de-lookup-organization-theo-ten-gay-cham-khi-sync-promotion.md]
- vấn đề trùng promotion do người dùng thao tác lặp và giải pháp idempotency bằng cache (chặn đầu) [van-de-trung-promotion-do-nguoi-dung-thao-tac-lap.md]
- script thêm cấu hình skycrm vào bảng parameters [script-them-cau-hinh-skycrm-vao-bang-parameters.md]
- tạo service skycloud tương đồng như rk7 [tao-service-skycloudservice-co-interface-co-get-post-put-delete-.net-core-2.1-c#-7.3.md]
- kiểm tra xem skycrm api dùng xác thực và bảo mật nào (useauthentication/useauthorization)? [ban-chat-bao-mat-trong-api-sky-crm.md] =>  **tạm thời không dùng bảo mật thực hiện dev trước** (với access token)
- thử thêm các param thông qua api put/get skytransfer (chỉ lấy/cập nhật). trao đổi anh tính/hiệp giải đáp thắc mắc 2 option thêm parameters
- cập nhật thêm trường cho ecompromotion (created/updated/processstatus) [script-tao-bang-ecom-promotion.md]
- sửa lại procedure kiểm tra promotion đang chờ xử lý từ ecom cho loại promotion là open_discount [script-lay-ecom-promotion-chua-xu-ly-trang-thai-opendiscount-goi-skycrm.md]
- tiếp tục xây dựng discounts theo hướng skytransfer => skyoffice
# 26-12-2025
- anh trưởng trao đổi lại về cơ chế vận hành open discount từ ecom
# 25-12-2025
- bắt đầu xử lý task đồng bộ discount mở (họp và trao đổi với anh trường + đầy)
- vẽ sơ đồ luồng hoạt động
- test các api cần thiết tạo và kiểm tra discount rk7
- viết api xử lý đồng bộ skytransfer -> rk7 cho trường hợp tạo mới (đang xử lý)[chỉ cần các trường name/sapcode/status và tab chi tiết]
- ~~tạo procedure kiểm tra promotion đang chờ xử lý từ ecom cho loại promotion là open_discount [script-lay-ecom-promotion-chua-xu-ly-trang-thai-opendiscount-goi-rk7]~~

# 23-12-2025
làm rõ vấn đề (anh tính - trưởng - huy)
- giả sử promotion engine không phải là decision service khi service này là trung gian giữa ecom-> service trung gian->rk7(pos) trong trường hợp này pos gọi service trung gian để tính toán và áp mã giảm giá từ bill
- thì promotion engine này có thể thực hiện gì nếu promotion này chịu trách nhiệm truyền thông tin mã  giảm giá, điều kiện từ bên ecom=> rk7 và pos sẽ cần dùng discount/promotion từ phía rk7
=> **ecom sẽ gọi api gửi dữ liệu qua rk7** (lấy danh sách discount cho pos), **qua skycrm** để thực hiện **pricing engine** logic decision tính toán/confirm discount 

# 17-12-2025
- cần anh tính cung cấp thông tin làm rõ yêu cầu về nghiệp vụ
em update nhanh tình trạng hiện tại để mọi người nắm:

hiện tại em đã làm rõ và kết nối được điểm (1): ecom → service trung gian (skytransfer) để nhận và lưu trữ dữ liệu.
điểm (2): luồng pos gọi sang promotion engine để bill áp dụng/ kích hoạt promotio → hiện chưa rõ nghiệp vụ:
– pos gọi ở thời điểm nào (realtime khi bán hay khi chốt bill?)
– promotion trả kết quả gì cho pos
– rule ưu tiên / cộng dồn / fallback khi không có promotion
em đang chờ làm rõ điểm (2) để tiếp tục


# 15-12-2025

## vấn đề
- promotion engine là gì mà phải tách ra?
promotion engine là service tính khuyến mãi theo ngữ cảnh bill. việc này cần real-time và thay đổi nhiều, nên không xử lý bằng sync data
- **dev cần hiểu promotion engine tới mức nào?**
dev chỉ cần biết input pos gửi sang và output engine trả về. logic bên trong do team engine và po chịu trách nhiệm.
- **kẹt gì?**
hiện tại chưa có api contract pos ↔ promotion engine nên em đang chờ để integrate đúng luồng.
- **khi nào code?**
khi có spec input/output + thời điểm pos gọi promotion engine thì em sẽ implement ngay.

# 01-12-2025
data trung gian sẽ gọi tới promotion engine thay vì đồng bộ như thông thường ecom - db trung gian - rk7 (thảo luận anh tính)
# 27-11-2025
- tạo api nhận thông tin các chương trình giảm giá từ ecom
- tạo script tạo các bảng thông tin về promtion sử dụng từ ecom [script nằm trong vấn đề thường gặp]