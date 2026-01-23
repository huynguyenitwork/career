# luồng thêm và sửa promotion

## lưu ý
- tham khảo tài liệu xử lý sync định nghĩa lại nhiệm vụ/cơ chế hoạt động cốt lõi của sync [logic-thuc-te-toan-bo-he-thong-sync.md]
- hàm **create** không trả về bản ghi đã tạo chỉ trả trạng thái (thành công/thất bại)

# sơ đồ plantuml
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

## điều kiện cần (theo thứ tự trên - xuống)
- luồng nghiệp vụ là command-driven
- cập nhật bảng **ecompromotion** [script-tao-bang-ecom-promotion.md]
- thêm **store procedure** để lấy các promotion đang ở trạng thái pending và loại discount mở [script-lay-ecom-promotion-chua-xu-ly-trang-thai-opendiscount-goi-skycrm.md]
- thêm script add các **parameter** liên quan đến **skycloud** [script-them-cau-hinh-skycrm-vao-bang-parameters.md]
- test theo quy trình các bước thực hiện và các kịch bản test theo bdd  **kịch bản happy path**
- tắt cache để test dev
- **xóa dữ liệu cũ** (nếu có) để thử lại

## rules

rules:
- đồng bộ là command-driven
- organization khác nhau theo env (organization lấy **id** nên dựa vào id)
- discount group phải tồn tại trước discount (discount và discount group lấy id nên dựa vào **code**)
- discount có 3 loại sự kiện thêm/sửa/xóa
- api có retry

reasons:
- dùng id thay vì code vì ít phải thêm/sửa hơn nhìn **id** là biết
- mặc định trạng thái gởi lên sky cloud là **draft**

## test-cases
| check | case | event type | status parent (dis-gr)            | status child  | hành vi hệ thống                  | kỳ vọng demo        | kiểm tra | đạt/không đạt | kiểm tra lại |
| ----- | ---- | ---------- | --------------------------------- | ------------- | --------------------------------- | ------------------- | -------- | ------------- | ------------ |
| v     | 1    | create     | không tồn tại (chưa từng tồn tại) | không tồn tại | bootstrap: tạo parent → tạo child | chạy full create    | test     | pass          |              |
| v     | 2    | create     | active                            | active        | reject duplicate                  | reject              | test     | pass          |              |
| v     | 3    | create     | active                            | soft-delete   | reject create                     | reject              | test     | pass          |              |
| v     | 4    | create     | active                            | không tồn tại | create child                      | tạo thành công      | test     | pass          |              |
| v     | 5    | create     | soft-delete                       | không tồn tại | reject create child               | reject              | test     | pass          |              |
| v     | 6    | update     | active                            | không tồn tại | reject update                     | reject              | test     | pass          |              |
| v     | 7    | update     | active                            | active        | update child                      | update success      | test     | pass          |              |
| v     | 8    | update     | active                            | soft-delete   | reject update                     | reject              | test     | pass          |              |
| v     | 9    | update     | soft-delete                       | active        | reject update                     | reject              | test     | pass          |              |
| v     | 6    | update     | không tồn tại                     | bất kỳ        | reject update                     | reject              | test     | pass          |              |
| v     | 11   | delete     | active                            | không tồn tại | noop hoặc reject                  | noop/reject         | test     | pass          |              |
| v     | 12   | delete     | không tồn tại                     | bất kỳ        | noop hoặc reject (policy)         | noop/reject         | test     | pass          |              |
| v     | 13   | delete     | active                            | active        | soft-delete child                 | soft+delete success | test     | pass          |              |
| v     | 14   | delete     | active                            | soft-delete   | noop                              | noop                | test     | pass          |              |
| v     | 15   | delete     | soft-delete                       | active        | noop                              | noop                | test     | pass          |              |

v success
x fail
- todo
+ processing
### các bước
- case thêm mới (success order)
case 1: xóa sạch dữ liệu crm gọi api sync discount hoặc mở lại promotion có sẵn
case 2: mở lại promotion có sẵn
case 3: xóa mềm discount, mở lại promotion có sẵn 
case 4: active lại (1) discount group, xóa hẳn discount và mở lại promotion có sẵn
case 5: xóa mềm discount group, mở lại promotion có sẵn
- case sửa (success order)
case 6: sửa lại eventype promotion updated, mở lại promotion có sẵn
case 7: tạo mới lại case 1, xóa promotion có sẵn và gọi api sync discount (cập nhật ngày kết thúc)
case 8: xóa mềm discount, mở lại promotion có sẵn 
case 9: xóa mềm discount group và mở lại promotion có sẵn
case 6: xóa hẳn discount group và mở lại promotion có sẵn
- case xóa (success order)
case 11: sửa lại eventype promotion deleted và mở lại promotion có sẵn
case 12: xóa hẳn discount group và mở lại promotion có sẵn 
case 13: tạo mới lại case 1, sửa lại eventype promotion deleted và mở lại promotion có sẵn
case 14: mở lại promotion có sẵn
case 15: xóa mềm discount group, chuyển trạng thái discount và mở lại promotion có sẵn


## flow system

### sketch system phase 2

#### sketch
start
-> skytransfer call http api refagent
	refagent queue request api & payload
-> refagent emit callback api
end
#### context
- queueworker: mở kho, lấy đơn
- queuemessagehandler: đọc nhãn đơn
- setrefdataprocessor: phân luồng công việc
- baseactnamehandler: áp quy trình chung
- savemenuitemhandler: thợ làm việc thật

### sketch system context (flow 1)
start
-> receive promotion event (created / updated / deleted)

-> validate organization
    no  -> error, stop
    yes -> continue

-> determine discount action (based on eventype)
    - create
    - update
    - soft delete
    - skip
-> for eventype create
	- nếu **parent không tồn tại**:
		- **ngoại lệ bootstrap (khởi tạo ban đầu)**:
			- nếu **parent chưa từng tồn tại trong hệ thống** và request thuộc luồng setup ban đầu:
			- → **cho phép tạo parent trước, sau đó tạo child**
			- lý do:
				* cần khởi tạo aggregate root lần đầu để hệ thống vận hành
				* không tồn tại parent thì không thể có child về mặt nghiệp vụ
				* phạm vi áp dụng:
				* bootstrap system
				* setup merchant / dcgroup lần đầu
				* migration dữ liệu gốc
			- giới hạn:
				* chỉ áp dụng khi parent chưa từng tồn tại
				* không áp dụng cho runtime thông thường
				* không áp dụng nếu parent đã từng bị soft-delete
		**=> cập nhật trạng thái promotion ecom (1-done)**
	- nếu **parent tồn tại nhưng soft-delete / inactive**:
	  - → **reject**
	  - lý do: parent đã bị loại khỏi lifecycle nghiệp vụ, child không được gắn vào
	  - phạm vi áp dụng: soft-delete mang ý nghĩa nghiệp vụ
		**=> cập nhật trạng thái promotion ecom (-1-reject)**

	- nếu **parent tồn tại và active**:
	  - tiếp tục áp dụng rule create của child:
		- child chưa tồn tại → create => **=> cập nhật trạng thái promotion ecom (1-done)**
		- child active → reject (duplicate) **=> cập nhật trạng thái promotion ecom (-1-reject)**
		- child soft-delete → reject **=> cập nhật trạng thái promotion ecom (-1-reject)**
		
-> for eventype update
	- nếu **parent không tồn tại**:
		- → **reject** => cập nhật trạng thái promotion ecom (-1-reject)
		- lý do: aggregate không hợp lệ

	- nếu **parent soft-delete / inactive**:
		- → **reject** => cập nhật trạng thái promotion ecom (-1-reject)
		- lý do: không cho phép thay đổi child của aggregate đã bị đóng

	- nếu **parent active**:
		- tiếp tục rule update child:
			- child active → update => cập nhật trạng thái promotion ecom (1-done)
			- child missing → **reject** => cập nhật trạng thái promotion ecom (-1-reject)
			- child soft-delete → **reject** => cập nhật trạng thái promotion ecom (-1-reject)
			
-> for eventype delete
	- nếu **parent không tồn tại**:
		- → **noop hoặc reject** (theo policy) => cập nhật trạng thái promotion ecom (-1-reject)
		- lý do: không có aggregate hợp lệ để thao tác

	- nếu **parent soft-delete / inactive**:
		- → **noop** => cập nhật trạng thái promotion ecom (-1-reject)
		- lý do: child đã mặc định không còn hiệu lực theo parent

	- nếu **parent active**:
		- áp dụng rule delete child:
			- child active → soft-delete => cập nhật trạng thái promotion ecom (1-done)
			- child soft-delete → noop => cập nhật trạng thái promotion ecom (-1-reject)
			- child missing → noop hoặc reject => cập nhật trạng thái promotion ecom (-1-reject)


### sketch system (flow 2)
start
sky crm/sky office
-> ecom call create/update/delete/
-> save sky crm/sky office [manual|auto] (**luồng gởi xuống-anh.khương api http**)
	-> ref agent (api crud)
	-> call api xml (rk7) 
	


## flow dev

### sketch implement (for dev)
start
-> sync promotion (eventype)

-> [a] get organization
-> org exist & org status is active?
    no  -> throw error, stop

–--warning---
refactor sau 3 case
–--warning---
-> switch(eventype)

    case created:
        -> kiểm tra parent - discount group
			không tồn tại
			  => tạo mới discount group
			  => kiểm tra child - discount
					không tồn tại ~> tạo mới
					soft-delete ~> từ chối
					tồn tại ~> từ chối
			soft-delete => từ chối
			tồn tại => tiếp tục
				=> kiểm tra child - discount
					không tồn tại ~> tạo mới
					soft-delete ~> từ chối
					tồn tại ~> từ chối

    case updated:
        -> kiểm tra parent - discount group
			không tồn tại|soft-delete => từ chối
			tồn tại => tiếp tục
				=> kiểm tra child - discount
					không tồn tại|soft-delete ~> từ chối
					tồn tại ~> cập nhật

    case deleted:
		-> kiểm tra parent - discount group
			không tồn tại => từ chối
			soft-delete => từ chối
			tồn tại => tiếp tục
				=> kiểm tra child - discount
					không tồn tại ~> từ chối
					soft-delete ~> từ chối
					tồn tại ~> **xóa**

=> [c] ensure discount group (subprocess)
    without id
        -> check exists not deleted by name => get id if exists
        -> check exists deleted by name => get id if exists
        -> not exists => create new + get new id
    with id
        -> check exists not deleted by name => get id if exists
        -> check exists deleted by name => get id if exists
        -> not exists => throw exception

=> [d] call api
-> retry?
-> done




## bảng so sánh system sketch và dev sketch 
| system sketch    | dev sketch         |
| ---------------- | ------------------ |
| nói **ý định**   | nói **cách làm**   |
| không switch     | switch rõ ràng     |
| dùng từ business | dùng từ kỹ thuật   |
| bền khi thay đổi | chính xác khi code |


## bảng check event
eventype   | discount exist?  | hành động
-----------|------------------|-------------------------
created    | no               | create
created    | yes              | skip / idempotent
updated    | yes              | update
updated    | no               | create (upsert)
deleted    | yes              | soft delete
deleted    | no               | skip

# tasklist

## [1] ecom ⇄ skytransfer - webhook nhận promotion

- expose webhook api cho ecom gửi promotion (swagger + postman để tích hợp)
- validate payload, generate callbackurl (skytransfer hoặc skyagent), lưu raw promotion + callbackurl vào db
- backgroundservice gọi api skycloud xử lý promotion (thêm/sửa/xóa)
- expose api callback inbound để skycloud hoặc refagent gọi trả kết quả theo callbackurl
- log trạng thái ("received" → "processing" → "sent")
- dev test: call webhook bằng postman, verify db record + job chạy + log theo requestid
---

## [2] skytransfer ⇄ skycloud - lưu promotion vào skycrm
- expose api nhận promotion inbound từ skytransfer
- validate org, discount group, discount để quyết định create / update / delete hoặc trả lỗi
- enqueue job xử lý cud promotion vào skycrm + gọi api rk7 qua refagent (fallback gọi trực tiếp rk7)
- callback api theo callbackurl cho skytransfer (fallback gọi trực tiếp rk7)
- log trạng thái xử lý promotion gởi skytransfer (theo từng giai đoạn)
- dev test: trigger flow từ [1], verify promotion trên crm + trạng thái log
---

## [3.1] skycrm ⇄ refagent - enqueue job xử lý promotion

- build job payload từ promotion crm (promotionid, params, requestid, action:cud)
- call api enqueue do refagent expose action cud
- nhận requestid trả về từ refagent để thông báo enqueue success/fail
- lưu mapping promotionid ↔ jobid ↔ requestid tại skycrm
- ghi log trạng thái "queued" tại skycrm
- dev test: verify refagent nhận request + queue có job + mapping đúng requestid

---

## [3.2] skycrm ⇄ rk7 - đồng bộ promotion xuống rk7 (direct)

- map promotion crm sang rk7 schema
- call rk7 xml api insert/update/delete promotion
- parse response rk7 (success / error code)
- gọi callback api về skytransfer với kết quả sync
- log trạng thái ("synced_to_rk7" hoặc "failed",...)
- dev test: verify promotion trên rk7 hoặc log lỗi đúng case

---

## [4.1] refagent ⇄ rk7 - đồng bộ promotion xuống rk7 (async)

- map payload job sang rk7 schema
- call rk7 xml api insert/update/delete promotion
- parse response rk7 và normalize result
- gọi callback api về skytransfer với kết quả sync [5.1]
- log trạng thái ("synced_to_rk7" hoặc "failed",...)
- dev test: verify rk7 data hoặc error log theo jobid

---

## [5.1] refagent ⇄ skytransfer - callback kết quả xử lý

- gọi callbackurl về skytransfer (từ [1])
- retry callback theo policy khi lỗi mạng / timeout (nếu có)
- update trạng thái xử lý cuối cùng của promotion trong skytransfer
- log trạng thái ("completed",...)
- dev test: mock success & fail, verify callback + final status
