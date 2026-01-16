@startuml
skinparam componentStyle rectangle
skinparam shadowing false
skinparam linetype ortho

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
