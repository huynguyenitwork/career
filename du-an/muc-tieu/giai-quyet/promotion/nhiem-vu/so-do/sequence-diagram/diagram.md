@startuml
skinparam sequenceMessageAlign center

@startuml
participant ecom
participant skytransfer
participant skycrm
participant refagent
participant rk7

ecom <-> skytransfer : [1] send promotion
activate skytransfer
skytransfer -> skycrm : [2] save promotion + requestid
activate skycrm
alt refagent (có sẵn)
    skycrm -> refagent : [3a] enqueue promotion job
    activate refagent
    refagent -> rk7 : [4a] sync promotion
    activate rk7
    rk7 --> refagent : sync result
    refagent --> skycrm : job result
    refagent --> skytransfer : [5a] callback api   
    deactivate refagent
else refagent (không có sẵn)
    skycrm -> rk7 : [3b] sync promotion (direct)
    rk7 --> skycrm : sync result
    deactivate rk7
    skycrm --> skytransfer : callback api (direct) 
    deactivate skycrm
    deactivate skytransfer
end

@enduml
