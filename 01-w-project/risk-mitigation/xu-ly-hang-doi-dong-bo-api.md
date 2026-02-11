# xử lý hàng đợi đồng bộ api

## mục tiêu
- xử lý queue đúng bản chất request
- loại trạng thái toàn cục gây sai ngữ cảnh
- retry có kiểm soát, không mất request

loại:
- over-engineering
- state trong memory
- tối ưu sớm

---

## vấn đề gốc
- api chạy theo request
- static bool sống theo vòng đời app

hệ quả:
- request sau (b) đọc trạng thái request trước (a)
- không biết trạng thái thuộc lần xử lý nào
- không trace, không retry thông minh

kết luận:
- dùng sai mô hình ngữ cảnh

---

## quyết định then chốt
- bỏ "đánh dấu trạng thái toàn cục"
- chuyển sang "ghi nhận xử lý theo từng request"

nguyên tắc:
- mỗi request = 1 bản ghi
- db giữ ký ức
- service chỉ xử lý

---

## mô hình cốt lõi

### api processing queue
- mỗi dòng = 1 request cần xử lý
- sống qua restart
- worker quét dựa trên data

```csharp
[Table("ApiProcessingQueue")]
public class ApiProcessingQueue
{
    public long Id { get; set; }
    public int RequestType { get; set; }
    public string EntityId { get; set; }
    public int Status { get; set; } // pending | processing | done | failed
    public string RequestKey { get; set; }

    public int RetryCount { get; set; }
    public int MaxRetry { get; set; } = 5;

    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
}
````

dùng để làm gì:

* lưu trạng thái thật của từng request
* quyết định retry dựa trên dữ liệu

loại:

* state chia sẻ giữa request

---

## retry đúng cách

### quy tắc

* failed nhưng retry < max → còn xử lý
* failed và hết retry → dừng vĩnh viễn

```csharp
x.Status == Pending
|| (x.Status == Failed && x.RetryCount < x.MaxRetry)
```

ý nghĩa:

* retry là data-driven
* không if-else rải khắp code

---

## worker logic tối giản

* enqueue → pending
* pick → processing
* success → done
* fail → failed + retry++

```csharp
public void MarkFailed(string entityId)
{
    var entity = GetByEntityId(entityId);
    entity.RetryCount += 1;

    UPDATE status = Failed, retryCount = entity.RetryCount;
}
```

dùng để làm gì:

* không reset thủ công
* worker chỉ quét theo điều kiện

---

## enqueue chuẩn

```csharp
TryEnqueue(new ApiProcessingQueue {
    RequestType = SyncStore,
    EntityId = entityId,
    RequestKey = requestKey,
    Status = Pending,
    RetryCount = 0,
    MaxRetry = 5
});
```

loại:

* enqueue không idempotent

---

## database là trung tâm

```sql
CREATE TABLE ApiProcessingQueue (
    id bigint primary key,
    requestType int,
    entityId nvarchar(100),
    status int,
    requestKey nvarchar(150),
    retryCount int default 0,
    maxRetry int default 5,
    createdAt datetime,
    updatedAt datetime
);
```

index bắt buộc:

* unique(requestKey)
* index(status, requestType)

---

## luồng tổng thể

* api nhận request → enqueue
* worker quét pending / failed còn retry
* xử lý → cập nhật status
* restart service không mất trạng thái

---

## kết luận

* sai lầm cũ: dùng trạng thái toàn cục cho bài toán theo request
* cách đúng: mỗi request là một thực thể có vòng đời
* db giữ ký ức, service là công nhân
* đủ đúng để dùng ngay, đủ mở để mở rộng sau