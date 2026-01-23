# sơ đồ api contract (plantuml)
## [3.1] skycrm ⇄ refagent enqueue job xử lý promotion (async, qua queue)

@startuml
skinparam componentStyle rectangle

component "skycrm" {
    [enqueue promotion job]
}

component "refagent" {
    [POST /api/jobs/enqueue]
}

component "skytransfer" {
    [POST /callback/enqueue-result]
}

"skycrm" --> "refagent" : request\npromotion job payload
"refagent" --> "skycrm" : response\n{ jobId, requestId }

"skycrm" --> "skytransfer" : callback\n{ status, requestId }
@enduml

## api 
``` bash
curl --request POST \
  --url http://localhost:5901/api/set-discount-rk7-data \
  --header 'X-Source-Service: MD' \
  --header 'content-type: application/json' \
  --data '{
    "ActName": "SaveDiscount",
    "Payload": {
		"SyncTaskId": 666,
		"Discount": {
			"Action": 1,
			"DiscountItem": {
				"Item": {
					"Name": "[test] discount 14-01-2026 14:44",
					"genSAPCODE": "[TEST]-sapcode-1401261444",
					"Status": 1,
					"Parent": 1108039
				}
			},
			"DiscountTypeItem": {
				"Item": {
					"Code": 1393,
					"Status": 1
				}
			}
		}
	},
  	"CallbackUrl": "http://localhost:5000/refagent/callback/discount"
}'
```

### req
``` json
{
    "ActName": "SaveDiscount",
    "Payload": {
		"SyncTaskId": 666,
		"Discount": {
			"Action": 1,
			"DiscountItem": {
				"Item": {
					"Name": "[test] discount 14-01-2026 14:44",
					"genSAPCODE": "[TEST]-sapcode-1401261444",
					"Status": 1,
					"Parent": 1108039
				}
			},
			"DiscountTypeItem": {
				"Item": {
					"Code": 1393,
					"Status": 1
				}
			}
		}
	},
  	"CallbackUrl": "http://localhost:5000/refagent/callback/discount"
}
```
### res
``` json
{
  "success": true,
  "message": "SetRefData request with ActName 'SaveDiscount' queued successfully. Processing and callback will happen asynchronously.",
  "data": {
    "requestId": "6a590378-24c9-42b3-819e-06ed75c92382"
  }
}
```

## [3.2] skycrm ⇄ rk7 đồng bộ promotion trực tiếp (sync xml api)


@startuml
skinparam componentStyle rectangle

component "skycrm" {
    [sync promotion to rk7]
}

component "rk7" {
    [POST /xml-api/discount/save]
}

component "skytransfer" {
    [POST /callback/rk7-sync-result]
}

"skycrm" --> "rk7" : request\npromotion xml payload
"rk7" --> "skycrm" : response\nxml result (success | error)

"skycrm" --> "skytransfer" : callback\n{ status, requestId, errorCode }
@enduml
