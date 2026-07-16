# nguyễn phú huy

**senior software engineer | business complexity specialist**

tp. hồ chí minh, việt nam
(+84) 353.072.938 · [huy.nguyen.it.work@gmail.com](mailto:huy.nguyen.it.work@gmail.com)
linkedin: linkedin.com/in/nguyen-phu-huy-580180250/

## profile

hơn 6 năm kinh nghiệm phát triển hệ thống doanh nghiệp, chuyên chuyển hóa **quy trình và nghiệp vụ phức tạp** thành hệ thống phần mềm ổn định, chính xác và có khả năng vận hành lâu dài.

có kinh nghiệm làm việc với **f&b, retail, manufacturing, erp, pos, finance**, đóng vai trò cầu nối giữa nghiệp vụ và kỹ thuật. thế mạnh tập trung vào **business modeling, system integration, backend engineering, architecture và reliability**.

kinh nghiệm thực chiến với các hệ thống tích hợp **pos ↔ sap ↔ e-commerce**, erp và các hệ thống nghiệp vụ nội bộ; thiết kế các cơ chế **validation, retry, idempotency, monitoring, auto-healing** để kiểm soát lỗi và đảm bảo dữ liệu đồng bộ.

## core capabilities

| năng lực                    | phạm vi                                                                                 |
| --------------------------- | --------------------------------------------------------------------------------------- |
| **business modeling**       | business rules, business logic, workflow, quy trình nghiệp vụ                           |
| **system integration**      | pos, sap, e-commerce, rest api, webhook, data synchronization                           |
| **architecture**            | clean architecture, api design, schema design, microservices                            |
| **reliability**             | validation, retry, fallback, idempotency, monitoring, tracing, auto-healing             |
| **backend engineering**     | .net/c#, asp.net core, python/odoo                                                      |
| **database design**         | sql server, postgresql, mysql, schema design, query optimization                        |
| **documentation**           | technical specification, brd, uml, api contract                                         |
| **ai-assisted engineering** | ai coding assistant, code review, debugging, testing, technical research, documentation |
| **supporting**              | docker, linux/unix, cli, bash, angular, reactjs, typescript/javascript                  |
| **language**                | tiếng anh — đọc hiểu tài liệu kỹ thuật chuyên sâu                                       |

## professional experience

### dcorp technology corporation

**senior developer · 10/2025 – hiện tại**

**pos integration platform — sap ↔ e-commerce ↔ pos**

**business problem**

chuỗi f&b cần đồng bộ dữ liệu giữa nhiều hệ thống; dữ liệu master, bán hàng và khuyến mãi phải được truyền **đầy đủ, chính xác và đúng thời gian**, trong khi kết nối giữa các hệ thống có thể gián đoạn và nghiệp vụ khuyến mãi có nhiều quy tắc.

**solution**

- phối hợp với ba và pm để phân tích và thiết kế giải pháp tích hợp.
- thiết kế **promotion engine**, chuyển các kịch bản khuyến mãi từ e-commerce xuống pos rk7.
- thiết kế data layer và api contract cho menu, sản phẩm, giá, cửa hàng, bill và store.
- xây dựng **validation rules** cho các loại khuyến mãi như open discount và order discount.
- xây dựng cơ chế **queue, retry và fallback** qua refagent để tiếp tục đồng bộ khi kết nối gián đoạn.
- thiết kế schema skytransfer và skycrm để theo dõi **sync task status** và timeline.
- áp dụng **idempotency** để chống trùng dữ liệu khi retry.
- chuẩn hóa **logging, tracing, monitoring và auto-healing**.

**impact**

- dữ liệu lỗi được phát hiện và chặn ngay tại tầng validation.
- quá trình đồng bộ có khả năng tiếp tục khi kết nối gián đoạn.
- có lịch sử và trạng thái đồng bộ phục vụ audit và debug.
- **giảm 40% thời gian điều tra và xử lý lỗi trên production.**

**technology:** .net core 6–10, postgresql, sql server, mysql, xml, nextjs, gitlab, grafana

### công ty cổ phần nagakawa

**erp developer · 08/2023 – 10/2025**

**erp nội bộ doanh nghiệp sản xuất**

**business problem**

doanh nghiệp cần số hóa nhiều quy trình nội bộ và thay thế phần mềm cũ; nghiệp vụ khác nhau giữa các lĩnh vực sản xuất, nhân sự, kế toán, kho và quy trình phê duyệt.

**solution**

- phát triển các module **đề xuất, quy trình, dự án, nhân sự, thông báo và tổng quan vận hành**.
- tùy chỉnh hệ thống theo nghiệp vụ của nhiều doanh nghiệp: cây xanh đô thị, may mặc, thiết bị điện lạnh/gia dụng, cơ điện và xây dựng.
- phát triển backend bằng **python/odoo** và tùy biến frontend bằng xml/javascript.
- triển khai migration từ hệ thống base sang odoo.
- xây dựng technical specification cho các module.
- thực hiện unit test, uat, sửa lỗi và tối ưu hiệu năng.
- sử dụng docker để chuẩn hóa môi trường phát triển.

**impact**

- hệ thống mới **thay thế hoàn toàn phần mềm cũ**.
- hỗ trợ số hóa các nghiệp vụ nội bộ trên một hệ thống thống nhất.
- **tiết kiệm 100% chi phí license** thông qua migration từ base sang odoo.

**technology:** python, odoo, postgresql, xml, javascript, docker, git

### công ty cổ phần thương mại giải pháp hachinet việt nam

**it engineer staffing · 07/2020 – 07/2023**

#### rj travels web portal

**business problem:** hệ thống cần quản lý nhiều loại dịch vụ du lịch và chăm sóc khách hàng.

**solution:** phát triển frontend angular, backend asp.net boilerplate, thiết kế database/query, docker hóa backend services, unit test và bảo trì hệ thống.

**technology:** angular 16, asp.net boilerplate, sql server, docker, git

#### lightning bim — arENT inc. japan

**business problem:** hỗ trợ tạo và tối ưu bố trí thép trong công trình xây dựng trên nền tảng revit.

**solution:** phát triển module xử lý cốt thép, cảnh báo va chạm, mặt cắt; nghiên cứu và tích hợp revit api; lưu trữ dữ liệu bằng extensible storage; xây dựng test bằng nunit/revit.testrunner.

**technology:** c#, wpf, .net framework 4.7.2, revit api, git

#### egov — bkav corporation

**business problem:** quản lý văn bản điện tử và quy trình xử lý cho chính phủ điện tử.

**solution:** phân tích yêu cầu và phát triển các module văn bản, xử lý, phân quyền và workflow; tích hợp api asp.net mvc5.

**technology:** c#, asp.net mvc5/webapi, entity framework 6, backbonejs, mysql

### công ty cổ phần công nghệ dft việt nam

**full stack developer · 06/2018 – 06/2020**

#### finportal — thịnh phát portal

**business problem:** quản lý chứng từ, kiểm soát phê duyệt và theo dõi dòng tiền cho hệ thống tài chính nội bộ.

**solution:** thiết kế và phát triển api quản lý chứng từ, kiểm soát approval workflow và tích hợp báo cáo trực quan.

**technology:** c#, asp.net boilerplate, angular, sql server, chartjs

#### mobifone customer portal

**business problem:** cung cấp cổng quản lý dịch vụ viễn thông, giao dịch và đăng ký dịch vụ.

**solution:** phát triển quản lý tài khoản, lịch sử giao dịch, thông báo khuyến mãi; tham gia triển khai và bảo trì.

**technology:** c#, asp.net boilerplate, angular, sql server, bootstrap

### ezcloud global

**full stack developer · 11/2016 – 06/2018**

#### ezfolio

**business problem:** quản lý toàn bộ quy trình khách sạn gồm đặt phòng, lưu trú, giá phòng, buồng phòng, báo cáo và phân phối qua ota.

**solution:** phát triển đặt phòng, lịch phòng, giá linh hoạt, phân quyền nhân viên và tích hợp các kênh ota như agoda, booking.com.

**technology:** c#, asp.net mvc5, sql server, vue.js, bootstrap

## education

**trường đại học xây dựng hà nội (huce)**
chuyên ngành công nghệ phần mềm · 2013 – 2017
