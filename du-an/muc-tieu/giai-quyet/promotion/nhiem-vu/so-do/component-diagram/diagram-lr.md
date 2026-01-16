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
skinparam shadowing false
skinparam linetype polyline
skinparam ArrowFontSize 10
skinparam ArrowLabelPosition center
skinparam defaultTextAlignment center


component "ecom" as E
component "skytransfer" as ST
component "skycrm" as SC
component "refagent" as RA
component "rk7" as RK

E <--> ST : [1] promotion webhook\njson api
ST <--> SC : [2] save promotion\njson api
SC --> RA : [3a] enqueue job\n(primary)
RA <--> RK : [4] sync promotion\nxml api
SC ..> RK : [3b] direct sync\n(fallback)
RA --> ST : [5] callback result

note right of SC
routing rule:
- try refagent first
- if check health api fall enqueue fail / timeout
- fallback to rk7 direct
- persist sync_path
end note

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

E <--> ST : [1] promotion webhook\njson api
ST <--> SC : [2] save promotion\njson api
SC --> RA : [3a] enqueue job\n(primary)
RA <--> RK : [4] sync promotion\nxml api
SC ..> RK : [3b] direct sync\n(fallback)
RA --> ST : [5] callback result

note left of SC
routing rule:
- try refagent first
- if enqueue fail / timeout
- fallback to rk7 direct
- persist sync_path
end note

@enduml



