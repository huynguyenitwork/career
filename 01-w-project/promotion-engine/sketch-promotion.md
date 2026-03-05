# sketch promotion – chuẩn hệ thống, tối giản

## mục tiêu

- mô tả **ý định xử lý promotion** từ ecom → rk7
- dùng sketch để **đóng băng logic**, không mô tả chi tiết code
- làm nền cho mermaid / plantuml / code

---

## phạm vi

- áp dụng cho luồng thêm / sửa / xóa promotion
- mô hình command-driven, async + callback
- create api **chỉ trả trạng thái**, không trả entity

---

## nguyên tắc loại

- decision tree chi tiết → loại
- mô tả cách code → loại
- lặp rule ở nhiều nơi → gom
- thông tin không ảnh hưởng quyết định xử lý → loại

---

## kiến trúc tổng quát (ý định)

- ecom phát sự kiện promotion
- skytransfer nhận, lưu, điều phối
- skycrm quyết định nghiệp vụ
- refagent / rk7 thực thi
- callback trả kết quả ngược dòng

---

## rules cốt lõi

- sync là command-driven
- organization khác nhau theo env → dùng **id**
- discount group phải tồn tại trước discount
- discount group + discount dùng **code** để đối chiếu
- promotion có 3 eventype: create / update / delete
- api gọi ra ngoài luôn có retry
- trạng thái gởi lên skycloud mặc định là "draft"

---

## trạng thái nghiệp vụ

- parent = discount group
- child = discount
- trạng thái hợp lệ: active / soft-delete / missing

---

## bảng hành vi theo event (chuẩn hóa)

| eventype | parent status | child status | hành động hệ thống              | kết quả |
| -------- | ------------- | ------------ | ------------------------------- | ------- |
| create   | missing       | missing      | bootstrap create parent → child | done    |
| create   | active        | active       | reject duplicate                | reject  |
| create   | active        | soft-delete  | reject create                   | reject  |
| create   | active        | missing      | create child                    | done    |
| create   | soft-delete   | missing      | reject create child             | reject  |
| update   | missing       | any          | reject update                   | reject  |
| update   | active        | active       | update child                    | done    |
| update   | active        | missing      | reject update                   | reject  |
| update   | active        | soft-delete  | reject update                   | reject  |
| update   | soft-delete   | active       | reject update                   | reject  |
| delete   | active        | missing      | noop hoặc reject (policy)       | reject  |
| delete   | missing       | any          | noop hoặc reject (policy)       | reject  |
| delete   | active        | active       | soft-delete child               | done    |
| delete   | active        | soft-delete  | noop                            | reject  |
| delete   | soft-delete   | active       | noop                            | reject  |

---

## bootstrap rule (ngoại lệ duy nhất)

- chỉ áp dụng khi:
  - parent **chưa từng tồn tại**
  - thuộc luồng setup ban đầu / migration
- cho phép:
  - tạo parent → tạo child
- không áp dụng khi:
  - runtime thông thường
  - parent từng soft-delete

---

## sketch system (ý định – không nhánh)

### flow tổng

```

start
-> receive promotion event
-> validate organization
-> ensure discount group (theo rule)
-> ensure discount (theo eventype)
-> call external api
-> retry if fail
-> callback result
-> end

```

---

## sketch theo pha

### phase 1: intake

- nhận event promotion
- validate payload
- lưu trạng thái received

### phase 2: validate

- validate organization
- xác định eventype

### phase 3: ensure

- ensure discount group
- ensure discount (create/update/delete/skip)

### phase 4: execution

- call api rk7 (direct hoặc qua refagent)
- retry theo policy

### phase 5: finalize

- cập nhật trạng thái promotion ecom
- callback kết quả

---

## sketch dev (chuyển từ system → code)

- system sketch: nói **ý định**
- dev sketch: nói **cách làm**
- system không switch
- dev switch(eventype) để implement

---

## mapping trạng thái promotion ecom

- done → xử lý thành công
- reject → vi phạm rule nghiệp vụ
- processing → đang xử lý
- failed → lỗi kỹ thuật sau retry

---

## checklist triển khai (tối giản)

- webhook nhận promotion từ ecom
- validate + lưu raw + callbackurl
- background xử lý promotion
- api callback inbound
- log theo requestid
- test happy path + reject path

---

## kết luận

- sketch dùng để **giữ logic thẳng**
- rule đứng riêng, flow không rẽ nhánh
- chỉ bung nhánh khi sang code
- đủ rõ để vẽ mermaid, đủ gọn để sửa nhanh

## nhánh core

| order | service     | direction | actname (status) | status     | eventcode           | dùng để làm gì                  | loại nếu             |
| ----- | ----------- | --------- | ---------------- | ---------- | ------------------- | ------------------------------- | -------------------- |
| 1     | ecom        | up        | ecom_webhook     | pending    | EC_WEBHOOK_RECEIVED | phát sinh luồng                 | không có synctaskid  |
| 1.1   | skytransfer | up        | st_store_payload | processing | ST_PAYLOAD_STORED   | lưu payload gốc từ ecom         | payload rỗng         |
| 2     | skytransfer | up        | st_ingest        | processing | ST_RECEIVED_ECOM    | nhận yêu cầu                    | duplicate            |
| 3     | skytransfer | down      | st_forward_crm   | processing | ST_FORWARD_CRM      | đẩy sang skycrm                 | retry nội bộ         |
| 4     | skycrm      | down      | crm_persist      | processing | CRM_SAVED           | lưu promotion                   | fail rollback        |
| 5     | skycrm      | down      | crm_dispatch_ra  | processing | CRM_ENQUEUE_RA      | chọn refagent                   | không async          |
| 6     | refagent    | down      | ra_process       | processing | RA_JOB_RECEIVED     | nhận job                        | thiếu requestid      |
| 7     | refagent    | down      | ra_sync          | processing | RA_SYNC_RK7         | sync rk7                        | partial              |
| 8     | refagent    | up        | ra_done          | processing | RA_DONE_ST          | trả kết quả upstream            | done >1              |
| 8.1   | skytransfer | up        | st_store_result  | processing | ST_RESPONSE_STORED  | lưu response cuối từ downstream | chưa có result/final |
| 9     | skytransfer | up        | st_finalize      | success    | ST_FINALIZED        | chốt task                       | thiếu completedat    |
| 10    | ecom        | up        | ecom_done        | success    | EC_COMPLETED        | kết thúc luồng                  | ecom không cần       |
| 11    | skytransfer | up        | st_finalize      | failed     | ST_FAILED           | đóng task lỗi                   | thiếu lasterror      |
| 12    | skytransfer | up        | st_finalize      | timeout    | ST_TIMEOUT          | đóng task quá hạn               | chưa hết sla         |
| 13    | skytransfer | up        | st_finalize      | canceled   | ST_CANCELED         | dừng chủ động                   | không có action hủy  |

---

## nhánh fallback (ghi cùng bảng, khác eventcode)

| order | service     | direction | actname          | status     | eventcode          | dùng để làm gì         | loại nếu            |
| ----- | ----------- | --------- | ---------------- | ---------- | ------------------ | ---------------------- | ------------------- |
| 5f    | skycrm      | down      | crm_dispatch_rk7 | processing | CRM_DIRECT_RK7     | bypass refagent        | không phải fallback |
| 6f    | skycrm      | up        | crm_done         | processing | CRM_DONE_ST        | done trực tiếp về st   | thiếu finalstatus   |
| 7f    | skytransfer | up        | st_finalize      | failed     | ST_FAILED_FALLBACK | đóng task lỗi fallback | thiếu lasterror     |

## mapping code

| order | service                      | direction | actname                            | status                     | eventcode                            | message                                   |
| ----- | ---------------------------- | --------- | ---------------------------------- | -------------------------- | ------------------------------------ | ----------------------------------------- |
| 1     | Delivery.Service.Ecom        | up        | Delivery.ActionName.EcomWebhook    | Delivery.Status.Pending    | Delivery.EventCode.EcWebhookReceived | Delivery.EventMessage.EcWebhookReceived   |
| 1.1   | Delivery.Service.Skytransfer | up        | Delivery.ActionName.StStorePayload | Delivery.Status.Processing | Delivery.EventCode.StPayloadStored   | Delivery.EventMessage.StPayloadStored     |
| 2     | Delivery.Service.Skytransfer | up        | Delivery.ActionName.StIngest       | Delivery.Status.Processing | Delivery.EventCode.StReceivedEcom    | Delivery.EventMessage.StReceivedEcom      |
| 3     | Delivery.Service.Skytransfer | down      | Delivery.ActionName.StForwardCrm   | Delivery.Status.Processing | Delivery.EventCode.StForwardCrm      | Delivery.EventMessage.StForwardCrm        |
| 4     | Delivery.Service.SkyCRM      | down      | Delivery.ActionName.CrmPersist     | Delivery.Status.Processing | Delivery.EventCode.CrmSaved          | Delivery.EventMessage.CrmSaved            |
| 5     | Delivery.Service.SkyCRM      | down      | Delivery.ActionName.CrmDispatchRa  | Delivery.Status.Processing | Delivery.EventCode.CrmEnqueueRa      | Delivery.EventMessage.CrmEnqueueRa        |
| 6     | Delivery.Service.RefAgent    | down      | Delivery.ActionName.RaProcess      | Delivery.Status.Processing | Delivery.EventCode.RaJobReceived     | Delivery.EventMessage.RaJobReceived       |
| 7     | Delivery.Service.RefAgent    | down      | Delivery.ActionName.RaSync         | Delivery.Status.Processing | Delivery.EventCode.RaSyncRk7         | Delivery.EventMessage.RaSyncRk7           |
| 8     | Delivery.Service.RefAgent    | up        | Delivery.ActionName.RaDone         | Delivery.Status.Processing | Delivery.EventCode.RaDoneSt          | Delivery.EventMessage.RaDoneSt            |
| 8.1   | Delivery.Service.Skytransfer | up        | Delivery.ActionName.StStoreResult  | Delivery.Status.Processing | Delivery.EventCode.StResponseStored  | Delivery.EventMessage.StResponseStored    |
| 10    | Delivery.Service.Ecom        | up        | Delivery.ActionName.EcomDone       | Delivery.Status.Success    | Delivery.EventCode.EcCompleted       | Delivery.EventMessage.EcCompleted         |
| 11    | Delivery.Service.Skytransfer | up        | Delivery.ActionName.StFinalize     | Delivery.Status.Failed     | Delivery.EventCode.StFailed          | Delivery.EventMessage.StFinalizedFailed   |
| 12    | Delivery.Service.Skytransfer | up        | Delivery.ActionName.StFinalize     | Delivery.Status.Timeout    | Delivery.EventCode.StTimeout         | Delivery.EventMessage.StFinalizedTimeout  |
| 13    | Delivery.Service.Skytransfer | up        | Delivery.ActionName.StFinalize     | Delivery.Status.Canceled   | Delivery.EventCode.StCanceled        | Delivery.EventMessage.StFinalizedCanceled |
| 5f    | Delivery.Service.SkyCRM      | down      | Delivery.ActionName.CrmDispatchRk7 | Delivery.Status.Processing | Delivery.EventCode.CrmDirectRk7      | Delivery.EventMessage.CrmDirectRk7        |
| 6f    | Delivery.Service.SkyCRM      | up        | Delivery.ActionName.CrmDone        | Delivery.Status.Processing | Delivery.EventCode.CrmDoneSt         | Delivery.EventMessage.CrmDoneSt           |
| 7f    | Delivery.Service.Skytransfer | up        | Delivery.ActionName.StFinalize     | Delivery.Status.Failed     | Delivery.EventCode.StFailedFallback  | Delivery.EventMessage.StFailedFallback    |

## code
### delivery skytransfer
```csharp
public static class Delivery
{
	public static class Status
	{
		public const string Pending = "pending";
		public const string Processing = "processing";
		public const string Success = "success";
		public const string Failed = "failed";
		public const string Timeout = "timeout";
		public const string Canceled = "canceled";
	}

	public static class EventCode
	{
		public const string EcWebhookReceived = "EC_WEBHOOK_RECEIVED";
		public const string StPayloadStored = "ST_PAYLOAD_STORED";
		public const string StReceivedEcom = "ST_RECEIVED_ECOM";
		public const string StForwardCrm = "ST_FORWARD_CRM";
		public const string CrmReceivedSt = "CRM_RECEIVED_ST";
		public const string CrmSaved = "CRM_SAVED";
		public const string CrmEnqueueRa = "CRM_ENQUEUE_RA";
		public const string RaJobReceived = "RA_JOB_RECEIVED";
		public const string RaSyncRk7 = "RA_SYNC_RK7";

		public const string RaDoneSt = "RA_DONE_ST";

		public const string StPayloadStored = "ST_PAYLOAD_STORED";
		public const string StFinalized = "ST_FINALIZED";
		public const string EcCompleted = "EC_COMPLETED";
		public const string StFailed = "ST_FAILED";
		public const string StTimeout = "ST_TIMEOUT";
		public const string StCanceled = "ST_CANCELED";

		public const string CrmDirectRk7 = "CRM_DIRECT_RK7";
		public const string CrmDoneSt = "CRM_DONE_ST";

		public const string StFailedFallback = "ST_FAILED_FALLBACK";
	}

	public static class ActionName
	{
		public const string EcomWebhook = "ecom_webhook";
		public const string StIngest = "st_ingest";
		public const string StForwardCrm = "st_forward_crm";
		public const string CrmReceivedSt = "crm_process";
		public const string CrmPersist = "crm_persist";
		public const string CrmDispatchRa = "crm_dispatch_ra";

		public const string RaProcess = "ra_process";
		public const string RaSync = "ra_sync";
		public const string RaDone = "ra_done";

		public const string StFinalize = "st_finalize";
		public const string EcomDone = "ecom_done";

		public const string CrmDispatchRk7 = "crm_dispatch_rk7";
		public const string CrmDone = "crm_done";
	}

	public static class EventMessage
	{
		public const string EcWebhookReceived = "ecom phát sinh webhook, khởi tạo luồng xử lý mới cho promotion.";
		public const string StReceivedEcom = "skytransfer đã nhận yêu cầu từ ecom và bắt đầu xử lý.";
		public const string StForwardCrm = "skytransfer chuyển promotion sang hệ skycrm để tiếp tục xử lý.";
		public const string CrmReceivedSt = "skycrm đã nhận yêu cầu từ skytransfer và bắt đầu xử lý.";
		public const string CrmSaved = "skycrm đã lưu promotion vào hệ thống thành công.";
		public const string CrmEnqueueRa = "skycrm đã chọn refagent phù hợp và đẩy job sang refagent.";
		public const string RaJobReceived = "refagent đã nhận job xử lý từ skycrm.";
		public const string RaSyncRk7 = "refagent đang đồng bộ promotion sang hệ RK7.";

		public const string RaDoneSt = "refagent hoàn tất xử lý và trả kết quả về cho skytransfer.";

		public const string StFinalizedSuccess = "skytransfer chốt task thành công.";
		public const string EcCompleted = "ecom xác nhận luồng xử lý promotion đã hoàn tất.";
		public const string StFinalizedFailed = "skytransfer chốt task ở trạng thái lỗi.";
		public const string StFinalizedTimeout = "skytransfer chốt task do quá thời gian xử lý.";
		public const string StFinalizedCanceled = "skytransfer chủ động dừng và hủy task.";

		// fallback
		public const string CrmDirectRk7 = "skycrm bỏ qua refagent và đồng bộ trực tiếp sang RK7.";
		public const string CrmDoneSt = "skycrm hoàn tất xử lý và trả kết quả trực tiếp về cho skytransfer.";
		public const string StFailedFallback = "skytransfer chốt task lỗi theo nhánh fallback.";
	}
	public static class Service
	{
		public const string Ecom = "ecom";
		public const string Skytransfer = "skytransfer";
		public const string SkyCRM = "skycrm";
		public const string RefAgent = "refagent";
	}
}
```
