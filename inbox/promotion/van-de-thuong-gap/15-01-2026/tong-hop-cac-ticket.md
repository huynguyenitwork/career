# sơ đồ kết nối

## dạng sketch
ecom=>skytransfer (call restfulapi json)
skytransfer=>skycloud (call restfulapi json save skycrm)
skytransfer=>refagent (call restfulapi queuejob, load balancing, auto healing)
refagent=>rk7 (call restfulapi xml)
refagent=>skytransfer (callback api, khi queuejob hoàn thành)

## dạng plant uml (component uml)
@startuml
left to right direction
skinparam componentStyle rectangle

skinparam shadowing false
skinparam linetype ortho
skinparam ArrowFontSize 10
skinparam ArrowLabelPosition center
skinparam defaultTextAlignment center

skinparam nodesep 40
skinparam ranksep 120

component "ecom" as E
component "skytransfer" as ST
component "skycloud" as SC
component "refagent" as RA
component "rk7" as RK

E <--> ST : [1] json api\n(req/res)
ST <--> SC : [2] json\nsave skycrm\n(req/res)
ST --> RA : [3] job queue
RA <--> RK : [4] xml api\n(req/res)
RA --> ST : [5]callback\n(job done)
@enduml

# chung
https://app.clickup.com/t/9018236177/DC-14322
Acceptance criteria
Transfer sever: Nhận toàn bộ dữ liệu gốc (raw) từ ECOM đẩy về
SkyCRM: Map promotion về object trên CRM để user có thể thao tác được trên SkyResto
Map đầy đủ thông tin cho đối tượng Promotion như: Tên, Mô tả, Loại, Mã, Hạn áp dụng (start/end), ....
RefAgent: Map promotion từ CRM để đưa vào RK7
Chỉ map các thông tin chính như: Tên, Mã, Loại

# qsr
https://app.clickup.com/t/9018236177/DC-14291
Description
Đồng bộ discount từ ECom về RK7 thông qua Promotion engine trên SkyCRM
Mục đích: Promotion quản lý tại 1 nơi là ECOM (Source of truth), master data sẽ được đồng bộ tới các nơi sử dụng (Online order, POS - dine in, ...) 
Do RK7 chỉ đáp ứng các promotion / discount đơn giản - không quản lý các Promotion phức tạp. Do đó cần xây dựng 1 promotion engine trên SkyCRM để xử lý Validate promotion thay cho RK7
Acceptance criteria
[Transfer Server] Xử lý nhận Promotion từ ECOM về Transfer server (raw data)
[SkyCRM] Lưu Promotion về CRM. Promotion được đồng bộ sẽ hiển thị trên danh sách Promotion trên SkyResto
[RefAgent] Viết API trên RefAgent để nhận promotion vừa tạo/update và xử lý trước khi lưu promotion vào RefServer
[RefAgent] Lưu Promotion vào RK7 theo thông tin: ECOMCODE, Tên promotion, Loại promotion, Ngày bắt đầu, ngày kết thúc  và trả về REFCODE và REFID sau khi insert/update thành công
Trả lỗi nếu lưu xuống RK7 không thành công
Trả success nếu lưu xuống RK7 thành công
Cần có cơ chế retry trong trường hợp sync xuống RK7 không thành công


Promotion Sheme
Cần đảm bảo các sheme sau được đồng bộ từ ECOM xuống RK7
Open discount (Giảm giá mở)
Giảm giá tổng đơn (% and Amount)
Giảm giá item (% and Amount)
Mua X tặng Y
...
...

# dev
https://app.clickup.com/t/9018236177/DC-14285
Description
ECOM đẩy CTKM giá mở về RK7
Note:
Promotion/Discount mở: Là discount rỗng, cho phép truyền số tiền giảm giá vào mà không cần phải thiết lập / validate các điều kiện của nó

Acceptance criteria
Viết Webhook để nhận Promotion giá mở từ ECOM đẩy sang
Lưu Promotion xuống RK7
Các thông tin cần thiết:
Mã 
Tên
Loại promotion/discount: Giá mở

