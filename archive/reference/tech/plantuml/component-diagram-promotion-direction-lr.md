# mục tiêu
- mô tả flow api promotion từ trái → phải
- sơ đồ chỉ phục vụ đọc nhanh & quyết định integration
- label nằm giữa connector, không che component
- xuống dòng bằng "\n"
- không mô tả logic xử lý ngoài routing chính

---

## s1 — polyline (ưu tiên, dễ căn label)

```plantuml
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
SC --> RA : [3a] enqueue job\nprimary
RA <--> RK : [4] sync promotion\nxml api
SC ..> RK : [3b] direct sync\nfallback
RA --> ST : [5] callback result

@enduml
```

---

## s2 — ortho (ít dùng, khó căn label)

```plantuml
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
SC --> RA : [3a] enqueue job\nprimary
RA <--> RK : [4] sync promotion\nxml api
SC ..> RK : [3b] direct sync\nfallback
RA --> ST : [5] callback result

@enduml
```
