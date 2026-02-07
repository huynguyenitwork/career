# mục tiêu
- mô tả trình tự xử lý promotion theo thời gian
- làm rõ nhánh rẽ khi có / không có refagent
- dùng để đọc nhanh luồng callback và điểm quyết định routing
- loại bỏ chi tiết triển khai không ảnh hưởng luồng

```plantuml
@startuml
skinparam sequenceMessageAlign center

participant ecom
participant skytransfer
participant skycrm
participant refagent
participant rk7

ecom <-> skytransfer : [1] send promotion
activate skytransfer

skytransfer -> skycrm : [2] save promotion + requestid
activate skycrm

alt refagent (available)
    skycrm -> refagent : [3a] enqueue promotion job
    activate refagent

    refagent -> rk7 : [4a] sync promotion
    activate rk7
    rk7 --> refagent : sync result

    refagent --> skycrm : job result
    refagent --> skytransfer : [5a] callback api
    deactivate refagent
else refagent (unavailable)
    skycrm -> rk7 : [3b] sync promotion (direct)
    activate rk7
    rk7 --> skycrm : sync result
    deactivate rk7

    skycrm --> skytransfer : callback api (direct)
end

deactivate skycrm
deactivate skytransfer
@enduml
```