# Xử lý hàng đợi đồng bộ

## Mục tiêu

* Đi thẳng vào vấn đề cốt lõi
* Loại bỏ cách lưu trạng thái gây sai lệch
* Áp dụng một cách mới **đúng bản chất API**, dễ dùng ngay, không over-engineering

---

## 1. Vì sao cách cũ không phù hợp (nguyên nhân gốc)

Cách cũ sử dụng `static bool` để đánh dấu trạng thái xử lý (ArticleChanged, PriceChanged, ComboChanged…). Vấn đề không nằm ở cú pháp, mà nằm ở **tư duy mô hình hóa**.

### 1.1. Nhầm lẫn phạm vi xử lý

* API hoạt động theo **request**
* `static bool` tồn tại theo **vòng đời ứng dụng**

Hệ quả:

* Request A thay đổi dữ liệu
* Request B chạy sau vẫn thấy trạng thái `true`
* Không xác định được trạng thái đó thuộc request nào

=> Trạng thái bị dùng sai ngữ cảnh.

---

### 1.2. Trả lời sai câu hỏi

Cách cũ chỉ trả lời được:

> Đã từng có thay đổi hay chưa?

Trong khi bài toán thực tế cần:

> Trong **lần xử lý này**, đã xảy ra **những sự kiện nào**?

Boolean chỉ phản ánh **sự tồn tại**, không phản ánh **hành trình xử lý**.

---

### 1.3. Chỉ xử lý được một lần

* Set `true`
* Xử lý
* Reset

Toàn bộ thông tin bị mất sau khi xử lý xong:

* Không trace được
* Không debug được
* Không audit được
* Không quyết định retry thông minh được

---

## 2. Quyết định đúng theo 20/80

**Quyết định then chốt:**

> Bỏ tư duy “đánh dấu trạng thái toàn cục” → chuyển sang “ghi nhận sự kiện theo từng request”.

Mỗi request là **một ngữ cảnh xử lý độc lập**, cần lưu lại:

* Những sự kiện đã xảy ra
* Theo đúng thứ tự xử lý

---

## 3. Cách mới – áp dụng ngay

### 19-12-2025 (nâng cấp cơ chế retry)

#### 3.1. Ý niệm cho rõ đầu

* **RetryCount**: đã thử mấy lần rồi
* **MaxRetry**: trần sinh học (ở đây = 5)
* Job **Failed nhưng còn retry** → vẫn coi là “pending logic”
* Job **Failed & hết retry** → chết hẳn, không quét nữa

---

#### 3.2. Model mới (chỉnh rất ít, nhưng trúng chỗ hiểm)

```csharp
[Table("ApiProcessingQueue")]
public class ApiProcessingQueue
{
    [Key]
    [Column("id")]
    public long Id { get; set; }

    [Column("requestType")]
    public int RequestType { get; set; }

    [Column("entityId")]
    [StringLength(100)]
    public string EntityId { get; set; }

    // Pending | Processing | Done | Failed
    [Column("status")]
    public int Status { get; set; }

    [Column("requestKey")]
    [StringLength(150)]
    public string RequestKey { get; set; }

    [Column("retryCount")]
    public int RetryCount { get; set; }

    [Column("maxRetry")]
    public int MaxRetry { get; set; } = 5;

    [Column("createdAt")]
    public DateTime CreatedAt { get; set; }

    [Column("updatedAt")]
    public DateTime? UpdatedAt { get; set; }
}
```

**Triết lý nhỏ nhưng quan trọng**
`MaxRetry` nằm trong DB → sau này muốn request loại A retry 3 lần, loại B retry 10 lần, không cần sửa code.

---

#### 3.3. Điều chỉnh enum (không đổi gì, giữ nguyên là đúng)

```csharp
public enum ApiProcessingStatus
{
    Pending = 0,
    Processing = 1,
    Done = 2,
    Failed = 3
}
```

---

#### 3.4. Sửa HasPending: chỉ quét cái còn hy vọng sống

### Trước đây

* Pending là Pending
* Failed là Failed → bỏ luôn (hơi tàn nhẫn)

### Bây giờ

* Pending → quét
* Failed **nhưng RetryCount < MaxRetry** → vẫn quét

```csharp
public bool HasPending(ApiRequestType[] requestTypes)
{
    var typeInts = requestTypes.Select(x => (int)x).ToArray();

    return _queue.Get(x =>
        typeInts.Contains(x.RequestType) &&
        (
            x.Status == (int)ApiProcessingStatus.Pending ||
            (
                x.Status == (int)ApiProcessingStatus.Failed &&
                x.RetryCount < x.MaxRetry
            )
        )
    ).Any();
}
```

Worker lúc này giống bác sĩ cấp cứu:

* còn nhịp tim → còn cứu
* hết retry → để đó làm hồ sơ tử vong ☠️

---

#### 3.5. Sửa TryMarkProcessing: cho Failed được hồi sinh

```csharp
public bool TryMarkProcessing(string entityId)
{
    var entity = GetByEntityId(entityId);
    if (entity == null) return false;

    if (
        entity.Status == (int)ApiProcessingStatus.Processing ||
        entity.Status == (int)ApiProcessingStatus.Done
    )
        return false;

    if (
        entity.Status == (int)ApiProcessingStatus.Failed &&
        entity.RetryCount >= entity.MaxRetry
    )
        return false;

    _dbContext.Database.ExecuteSqlCommand(
        @"UPDATE ApiProcessingQueue SET 
            status = @status,
            updatedAt = @updatedAt
          WHERE entityId = @entityId",
        new SqlParameter("@status", (int)ApiProcessingStatus.Processing),
        new SqlParameter("@updatedAt", DateTime.UtcNow),
        new SqlParameter("@entityId", entityId)
    );

    return true;
}
```

---

#### 3.6. Sửa MarkFailed: thất bại có kiểm soát

### Quy tắc mới

* Fail → tăng retry
* Nếu **retry >= max** → giữ Failed vĩnh viễn
* Nếu chưa max → vẫn Failed, nhưng **còn cửa quay lại**

```csharp
public void MarkFailed(string entityId)
{
	var entity = GetByEntityId(entityId);
	if (entity == null) return;
	var retryCount = entity.RetryCount += 1;
	_dbContext.Database.ExecuteSqlCommand(
		@"UPDATE ApiProcessingQueue SET 
			status = @status,
			updatedAt = @updatedAt,
			retryCount = @retryCount
		WHERE entityId = @entityId",
		new SqlParameter("@status", (int)ApiProcessingStatus.Failed),
		new SqlParameter("@updatedAt", DateTime.UtcNow),
		new SqlParameter("@retryCount", retryCount),
		new SqlParameter("@entityId", entityId)
	);
}
```

Cái hay ở đây

* **Không reset Pending thủ công**
* Worker chỉ cần quét theo logic HasPending
* Retry là **data-driven**, không phải if-else rải khắp nơi

---

#### 3.7. Khi enqueue: nhớ set retry từ đầu cho tử tế

```csharp
_apiProcessingQueue.TryEnqueue(new ApiProcessingQueue
{
    RequestType = (int)ApiRequestType.SyncStore,
    EntityId = entityId,
    RequestKey = requestKey,
    Status = (int)ApiProcessingStatus.Pending,
    RetryCount = 0,
    MaxRetry = 5
});
```

---

#### 3.8. Migration bổ sung (rất nhẹ)

```sql
ALTER TABLE ApiProcessingQueue
ADD retryCount INT NOT NULL DEFAULT 0,
    maxRetry INT NOT NULL DEFAULT 5;
```

Index cũ giữ nguyên, không cần thêm.

---

#### 3.9. Tổng kết

* Bạn đã có:

  * queue **không mất request**
  * retry **có giới hạn**
  * worker **không loop ngu**
* Mô hình này:

  * chịu được crash
  * audit được
  * scale worker song song được nếu sau này cần

Nếu muốn, bước kế tiếp rất đẹp là:

* thêm `lastError`
* thêm `nextRetryAt` → retry có backoff
  Nhưng đó là chương sau, khi hệ thống bắt đầu… có cá tính

### 18-12-2025 (khởi tạo)

#### 3.1. Tư duy thiết kế

* Không dùng `static`
* Không chia sẻ trạng thái giữa các request
* Mỗi API call có một **ApiProcessingQueue** riêng
* Context ghi nhận **danh sách sự kiện** đã xảy ra

Hệ thống cần:
- Nhận HTTP API inbound
- Ghi nhận request vào hàng đợi
- Background worker quét & xử lý
- Không xử lý trùng
- Service restart không mất trạng thái
- Chỉ cần biết: có pending hay không → quyết định chạy

Giải pháp:
- DB-backed processing queue
- Không giữ state trong memory / DI scope
- DB là “bộ nhớ dài hạn”, service chỉ là công nhân thời vụ

---

#### 3.2. Định nghĩa model

```csharp
using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace AppServer.Models.Entities
{
    [Table("ApiProcessingQueue")]
    public class ApiProcessingQueue
    {
        [Key]
        [Column("id")]
        public long Id { get; set; }

        // Loại request / nghiệp vụ (sync store, sync product, ...)
        [Column("requestType")]
        public int RequestType { get; set; }

        // Đối tượng chính của request
        [Column("entityId")]
        [StringLength(100)]
        public string EntityId { get; set; }

        // Pending | Processing | Done | Failed
        [Column("status")]
        public int Status { get; set; }

        // Dùng để chống xử lý trùng (idempotent)
        [Column("requestKey")]
        [StringLength(150)]
        public string RequestKey { get; set; }

        // HTTP đẩy vào lúc nào
        [Column("createdAt")]
        public DateTime CreatedAt { get; set; }

        // Lúc worker chạm vào gần nhất
        [Column("updatedAt")]
        public DateTime? UpdatedAt { get; set; }
    }
}
```
#### 3.3. Định nghĩa repository

#### enum
```csharp
public enum ApiProcessingStatus
{
    Pending = 0,
    Processing = 1,
    Done = 2,
    Failed = 3
}

public enum ApiRequestType
{
    SyncStore = 1,
    SyncProduct = 2,
    SyncPrice = 3,
    SyncCombo = 4
}
```
#### interface 

```csharp
public interface IApiProcessingQueueRepository : IBaseDataRepository<ApiProcessingQueue>
{
	bool TryEnqueue(ApiProcessingQueue entity);
	IEnumerable<ApiProcessingQueue> GetPending(int take = 100);
	bool TryMarkProcessing(long id);
	void MarkDone(long id);
	void MarkFailed(long id);
}

```
#### implement

```csharp
public class ApiProcessingQueueDataManager : IApiProcessingQueueRepository
{
	private readonly DatabaseContext _dbContext;
	private readonly BaseDataManager<ApiProcessingQueue> _queue;

	public ApiProcessingQueueDataManager(DatabaseContext dbContext)
	{
		_dbContext = dbContext;
		_queue = new BaseDataManager<ApiProcessingQueue>(_dbContext);
	}

	public bool TryEnqueue(ApiProcessingQueue entity)
	{
		var exists = _queue.Get(x => x.RequestKey == entity.RequestKey).Any();
		if (exists) return false;

		entity.Status = (int)ApiProcessingStatus.Pending;
		entity.CreatedAt = DateTime.UtcNow;

		_queue.Add(entity);
		_dbContext.SaveChanges();
		return true;
	}


	public bool HasPending(ApiRequestType[] requestTypes)
	{
		var typeInts = requestTypes.Select(x => (int)x).ToArray();
		var pending = (int)ApiProcessingStatus.Pending;
		return _queue.Get(x =>
				x.Status == pending &&
				typeInts.Contains(x.RequestType)
			).Any();
	}


	public bool TryMarkProcessing(string entityId)
	{
		var entity = GetByEntityId(entityId);
		if (entity == null) return false;
		if (entity.Status != (int)ApiProcessingStatus.Pending) return false;

		_dbContext.Database.ExecuteSqlCommand(
			@"UPDATE ApiProcessingQueue SET 
				status = @status,
				updatedAt = @updatedAt
			WHERE entityId = @entityId",
			new SqlParameter("@status", (int)ApiProcessingStatus.Processing),
			new SqlParameter("@updatedAt", DateTime.UtcNow),
			new SqlParameter("@entityId", entityId)
		);
		return true;
	}

	public void MarkDone(string entityId)
	{
		UpdateStatusJob(entityId, ApiProcessingStatus.Done);
	}

	public void MarkFailed(string entityId)
	{
		UpdateStatusJob(entityId, ApiProcessingStatus.Failed);
	}

	private void UpdateStatusJob(string entityId, ApiProcessingStatus status)
	{
		var entity = GetByEntityId(entityId);
		if (entity == null) return;
		_dbContext.Database.ExecuteSqlCommand(
			@"UPDATE ApiProcessingQueue SET 
				status = @status,
				updatedAt = @updatedAt
			WHERE entityId = @entityId",
			new SqlParameter("@status", (int)status),
			new SqlParameter("@updatedAt", DateTime.UtcNow),
			new SqlParameter("@entityId", entityId)
		);

	}

    private ApiProcessingQueue GetByEntityId(string entityId)
    {
		return _queue.Get(g=>g.EntityId == entityId).First();

	}
}
```
#### 3.4. Service xử lý

```csharp
_apiProcessingQueue.TryEnqueue(new ApiProcessingQueue
{
	RequestType = (int)ApiRequestType.SyncStore,
	EntityId = entityId,
	RequestKey = Guid.NewGuid().ToString(),
    Status = (int)ApiProcessingStatus.Processing,
});

```
---



#### 3.5. Migration DB (SQL – dùng được liền)

#### SQL Server / MySQL tương đương

```sql
CREATE TABLE ApiProcessingQueue (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    requestType INT NOT NULL,
    entityId NVARCHAR(100) NOT NULL,
    status INT NOT NULL,
    requestKey NVARCHAR(150) NOT NULL,
    createdAt DATETIME NOT NULL,
    updatedAt DATETIME NULL
);
```

#### Index quan trọng (đừng bỏ)

```sql
-- Chống trùng request
CREATE UNIQUE INDEX UX_ApiProcessingQueue_RequestKey
ON ApiProcessingQueue (requestKey);

-- Quét pending nhanh
CREATE INDEX IX_ApiProcessingQueue_Status_Type
ON ApiProcessingQueue (status, requestType);
```

---

#### 3.6. Luồng chạy tổng thể (1 phút là hiểu)

1. HTTP API inbound

   * build `requestKey`
   * `TryEnqueue`
2. Background worker

   * `HasPending(...)`
   * nếu false → ngủ
3. Worker pick job

   * `TryMarkProcessing`
4. Xử lý nghiệp vụ
5. `MarkDone` hoặc `MarkFailed`

Service **restart bao nhiêu lần cũng được**
DB còn → hệ thống còn ký ức.

---

#### 3.7. Một câu chốt cho team / PO / future-you

> “Service là công nhân, database là trí nhớ.”



## 4. vì sao cách mới hiệu quả hơn

### 4.1. đúng bản chất api

* api xử lý theo request
* context sống đúng vòng đời request

không còn tình trạng:

* request này đọc trạng thái của request khác

---

### 4.2. ghi nhận được hành trình xử lý

hệ thống biết rõ:

* đã xử lý những bước nào
* thiếu bước nào
* thứ tự đã đi qua

điều này đặc biệt quan trọng với các luồng:

* store → product → price → combo → promotion

---

### 4.3. mở đường cho mở rộng sau này

từ mô hình này, có thể mở rộng thêm mà không phá kiến trúc:

* thêm trạng thái success / failed
* retry theo từng event
* audit log
* chuyển sang event-driven khi hệ thống đủ lớn

---

## 5. kết luận

* cách cũ sai vì dùng **trạng thái toàn cục** cho **bài toán theo request**
* cách mới đúng vì ghi nhận **sự kiện theo ngữ cảnh xử lý cụ thể**
* theo nguyên lý 20/80: giải quyết đúng vấn đề, chi phí thấp, hiệu quả cao

khi hệ thống có thể kể lại chính xác những gì nó vừa xử lý, việc ra quyết định trở nên rõ ràng và có căn cứ.
