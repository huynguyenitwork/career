# mục tiêu
- chiều flow từ trái qua phải
- font chữ cho connection cần nhỏ để không chiếm diện tích component
- chữ là ở giữa connection
- (*) loại kết nối là kiểu polyline dễ nhìn nếu muốn căn label giữa (thay vì ortho vuông góc không hỗ trợ căn giữa label dùng nodesep [căn ngang]/ranksep [căn dọc] nhưng không đảm bảo)
- label ở trên/dưới connector (không hỗ trọ)
- xuống dòng dùng (\n)
- không cho chữ cắt qua connector dùng (defaultTextAlignment và ArrowLabelPosition)

# s1 - dùng với polyline
@startuml
left to right direction

skinparam componentStyle rectangle
skinparam shadowing true

skinparam linetype polyline

skinparam defaultTextAlignment center
skinparam ArrowFontSize 10
skinparam ArrowLabelPosition center

component "ecom" as E
component "skytransfer" as ST
component "skycrm" as SC
component "refagent" as RA
component "rk7" as RK

E <--> ST : [1] json api\n(req/res)
ST <--> SC : [2] json save\n(req/res)
SC --> RA : [3] job queue
RA <--> RK : [4] xml api\n(req/res)
RA --> ST : [5]callback (job done)
@enduml



# s2 - dùng với ortho
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
component "skycrm" as SC
component "refagent" as RA
component "rk7" as RK

E <--> ST : [1] json api\n(req/res)
ST <--> SC : [2] json save\n(req/res)
SC --> RA : [3] job queue
RA <--> RK : [4] xml api\n(req/res)
RA --> ST : [5]callback (job done)
@enduml


