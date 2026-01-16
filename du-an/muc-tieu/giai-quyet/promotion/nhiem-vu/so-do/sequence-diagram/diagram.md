@startuml
skinparam sequenceMessageAlign center

participant ecom
participant skytransfer
participant skycrm
participant refagent
participant rk7

ecom <-> skytransfer : [1] json api (req/res)
activate skytransfer
skytransfer <-> skycrm : [2] json save (req/res)
activate skycrm
skycrm -> refagent : [3] job queue
deactivate skycrm
activate refagent
refagent <-> rk7 : [4] xml api (req/res)
activate rk7
deactivate rk7
refagent --> skytransfer : [5] callback (job done)
deactivate refagent
deactivate skytransfer

@enduml