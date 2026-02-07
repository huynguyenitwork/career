ok, mình viết lại **thành tài liệu phân tích hoàn chỉnh**, có so sánh rõ **cách cũ vs cách mới**, chỉ ra **ưu/nhược**, và **ví dụ áp dụng thực tế với c# 7.3 + asp.net core 2.1**.
mục tiêu: đọc xong là **quyết được hướng + code được ngay**, không tranh luận cảm tính.

---

# tài liệu phân tích thiết kế log & trạng thái async callback

## skytool ↔ refagent

---

## 1. bối cảnh vấn đề

skytool gọi refagent xử lý async (save discount, sync ref data…).
refagent trả `requestId` và callback kết quả về sau.

vấn đề đặt ra:

* chỉ dùng bảng `EcomLog` hiện tại **không đủ** để:

  * theo dõi tiến trình
  * xác nhận trạng thái cuối
  * debug theo từng task async
* file log thì rối, tool log thì không phải nguồn sự thật

=> cần phân tích **cách cũ đang thiếu gì**, và **cách mới giải quyết ra sao**.

---

## 2. cách cũ: dùng bảng `EcomLog` làm trung tâm

### 2.1 schema hiện tại

```sql
CREATE TABLE "EcomLog" (
    "Id" INT,
    "ApiUrl" NVARCHAR(max),
    "Type" NVARCHAR(max),
    "Payload" NVARCHAR(max),
    "Status" NVARCHAR(max),
    "MessageError" NVARCHAR(max),
    "Response" NVARCHAR(max),
    "Created" DATETIME,
    PRIMARY KEY ("Id")
)
```

---

### 2.2 cách vận hành thực tế (cách cũ)

* khi skytool gọi refagent:

  * insert 1 dòng log
* khi nhận response sync:

  * update hoặc insert log khác
* khi callback:

  * insert thêm 1 log nữa (nếu có)

mọi thứ dồn vào **1 bảng chung**.

---

### 2.3 ưu điểm của cách cũ

* triển khai nhanh
* không cần thiết kế thêm bảng
* debug đơn lẻ từng api call thì tạm ổn

---

### 2.4 nhược điểm nghiêm trọng (điểm gãy)

* **không có khái niệm task async**

  * không biết 3–4 dòng log có thuộc cùng 1 luồng không
* **không có trạng thái cuối rõ ràng**

  * success hay failed phải tự đoán
* **status mơ hồ**

  * status là http? business? callback?
* **không dựng được timeline**

  * pm / ops hỏi “task này đang ở đâu?” → chịu
* **không scale**

  * nhiều loại async khác nhau → bảng thành bãi rác log

kết luận:

> `EcomLog` là nhật ký kỹ thuật, không phải công cụ quản lý async.

---

## 3. cách mới: tách rõ 3 lớp trách nhiệm

### 3.1 tổng quan kiến trúc mới

* **core business table**

  * dữ liệu nghiệp vụ cuối
* **sync_task_status**

  * trạng thái hiện tại (1 dòng / task)
* **sync_task_timeline**

  * tiến trình xử lý (n dòng / task)
* **EcomLog**

  * log kỹ thuật (giữ lại, không bỏ)

---

## 4. thiết kế bảng mới (cách mới)

### 4.1 bảng trạng thái: `sync_task_status`

```sql
CREATE TABLE sync_task_status (
    id INT IDENTITY PRIMARY KEY,
    sync_task_id INT NOT NULL,
    act_name NVARCHAR(100),
    request_id NVARCHAR(50),
    status NVARCHAR(30),
    last_error_code NVARCHAR(50),
    last_error_message NVARCHAR(500),
    retry_count INT,
    created_at DATETIME,
    updated_at DATETIME,
    completed_at DATETIME
)
```

#### vai trò

* nguồn sự thật duy nhất của async task
* dùng cho:

  * dashboard
  * retry
  * đối soát dữ liệu

---

### 4.2 bảng timeline: `sync_task_timeline`

```sql
CREATE TABLE sync_task_timeline (
    id INT IDENTITY PRIMARY KEY,
    sync_task_id INT NOT NULL,
    request_id NVARCHAR(50),
    event_type NVARCHAR(50),
    event_message NVARCHAR(500),
    created_at DATETIME
)
```

#### vai trò

* trả lời câu hỏi: “chuyện gì đã xảy ra?”
* pm / ops đọc được
* audit được

---

## 5. so sánh trực diện: cũ vs mới

### 5.1 theo tiêu chí vận hành

* theo dõi trạng thái:

  * cũ: không rõ
  * mới: rõ ràng, 1 dòng / task
* dựng timeline:

  * cũ: gần như không thể
  * mới: query ra ngay
* retry / reconciliation:

  * cũ: viết script thủ công
  * mới: dựa trên status
* scale hệ thống:

  * cũ: log phình, khó kiểm soát
  * mới: mở rộng an toàn

---

### 5.2 theo nguyên lý 20/80

* 20% effort thêm bảng
* đổi lại 80%:

  * dễ vận hành
  * dễ debug
  * dễ mở rộng

---

## 6. ví dụ áp dụng cụ thể với c# 7.3 + asp.net core 2.1

### 6.1 khi gửi request a → b

```csharp
public void SendToRefAgent(SyncTask task)
{
    _db.SyncTaskStatus.Add(new SyncTaskStatus
    {
        SyncTaskId = task.Id,
        ActName = task.ActName,
        Status = "pending",
        CreatedAt = DateTime.UtcNow
    });

    _db.SyncTaskTimeline.Add(new SyncTaskTimeline
    {
        SyncTaskId = task.Id,
        EventType = "request_sent",
        EventMessage = "send request to refagent",
        CreatedAt = DateTime.UtcNow
    });

    _db.SaveChanges();
}
```

---

### 6.2 khi nhận response sync (queued)

```csharp
public void OnQueued(int syncTaskId, string requestId)
{
    var status = _db.SyncTaskStatus.Single(x => x.SyncTaskId == syncTaskId);
    status.RequestId = requestId;
    status.Status = "processing";
    status.UpdatedAt = DateTime.UtcNow;

    _db.SyncTaskTimeline.Add(new SyncTaskTimeline
    {
        SyncTaskId = syncTaskId,
        RequestId = requestId,
        EventType = "queued",
        EventMessage = "refagent queued request",
        CreatedAt = DateTime.UtcNow
    });

    _db.SaveChanges();
}
```

---

### 6.3 khi nhận callback b → a

```csharp
public void HandleCallback(CallbackDto dto)
{
    var status = _db.SyncTaskStatus.Single(x => x.RequestId == dto.RequestId);

    status.Status = dto.Status;
    status.CompletedAt = DateTime.UtcNow;
    status.LastErrorCode = dto.Error?.Code;
    status.LastErrorMessage = dto.Error?.Message;

    _db.SyncTaskTimeline.Add(new SyncTaskTimeline
    {
        SyncTaskId = status.SyncTaskId,
        RequestId = dto.RequestId,
        EventType = "callback_received",
        EventMessage = dto.Status,
        CreatedAt = DateTime.UtcNow
    });

    _db.SaveChanges();
}
```

---

## 7. vai trò của `EcomLog` trong cách mới

* vẫn dùng để:

  * log raw payload
  * log response đầy đủ
  * debug kỹ thuật
* **không dùng để**:

  * xác định trạng thái
  * dựng timeline nghiệp vụ

nói gọn:

> ecomlog ghi chi tiết, status + timeline ghi sự thật.

---

## 8. kết luận cuối cùng

* cách cũ:

  * nhanh, nhưng không kiểm soát được async
* cách mới:

  * thêm 2 bảng
  * đổi lại:

    * hệ thống có trí nhớ
    * vận hành không phụ thuộc con người
    * scale không đau

câu chốt cho tài liệu nội bộ:

> async không có trạng thái là mù.
> async không có timeline là câm.
> log kỹ thuật không thể thay thế dữ liệu nghiệp vụ.
