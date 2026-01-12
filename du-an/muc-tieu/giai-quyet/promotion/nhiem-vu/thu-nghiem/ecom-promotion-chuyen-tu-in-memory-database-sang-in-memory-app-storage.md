# tài liệu kỹ thuật

## chuyển ecom promotion sang in-memory app repository (c# 7.3)

---

## 1. mục tiêu

* thay thế stored procedure bằng **in-memory app repository**
* giữ interface service
* đổi tên abstraction từ `store` → `repository`
* code chạy được với **c# 7.3**
* dễ test, dễ rollback

---

## 2. kiến trúc sau khi refactor

```
caller / job
   ↓
iecompromotionservices
   ↓
iecompromotionrepository
   ↓
inmemoryecompromotionrepository (list trong ram)
```

---

## 3. interface service (giữ nguyên)

```csharp
public interface IEcomPromotionServices
{
    Task<List<EcomPromotion>> GetPendingOpenDiscountPromotions();
}
```

---

## 4. tạo repository abstraction (thay stored procedure)

```csharp
public interface IEcomPromotionRepository
{
    Task<List<EcomPromotion>> GetPendingOpenDiscountPromotions();
}
```

repository này **đại diện cho nguồn dữ liệu**, không quan tâm db hay ram.

---

## 5. triển khai in-memory app repository (c# 7.3)

```csharp
public class InMemoryEcomPromotionRepository : IEcomPromotionRepository
{
    private static readonly List<EcomPromotion> _data =
        new List<EcomPromotion>
        {
            new EcomPromotion
            {
                Id = 1,
                Code = "OPEN001",
                Name = "open discount test",
                PromotionType = "OPEN_DISCOUNT",
                ProcessStatus = 0,
                StartTime = DateTime.UtcNow.AddDays(-1),
                Created = DateTime.UtcNow
            },
            new EcomPromotion
            {
                Id = 2,
                Code = "CLOSE001",
                Name = "closed discount",
                PromotionType = "CLOSE_DISCOUNT",
                ProcessStatus = 0,
                StartTime = DateTime.UtcNow
            }
        };

    public Task<List<EcomPromotion>> GetPendingOpenDiscountPromotions()
    {
        var result = _data
            .Where(x =>
                x.ProcessStatus == 0 &&
                x.PromotionType == "OPEN_DISCOUNT"
            )
            .OrderBy(x => x.Id)
            .ToList();

        return Task.FromResult(result);
    }
}
```

ghi chú kỹ thuật:

* dùng `new List<T>` thay vì `new()`
* không dùng syntax mới của c# 8+
* dữ liệu sống trong ram của process
* restart app là mất data

---

## 6. refactor service để dùng repository

### trước

* service gọi `_adoservices.execproc(...)`

### sau

* service gọi repository
* không biết sql, không biết db

```csharp
public class EcomPromotionServices : IEcomPromotionServices
{
    private readonly IEcomPromotionRepository _repository;

    public EcomPromotionServices(
        IEcomPromotionRepository repository
    )
    {
        _repository = repository;
    }

    public async Task<List<EcomPromotion>> GetPendingOpenDiscountPromotions()
    {
        try
        {
            return await _repository.GetPendingOpenDiscountPromotions();
        }
        catch
        {
            throw;
        }
    }
}
```

logic nghiệp vụ **không đổi**, chỉ đổi nguồn dữ liệu.

---

## 7. mapping logic stored procedure → repository

stored procedure cũ:

```sql
where processstatus = 0
  and promotiontype = 'open_discount'
order by id asc
```

in-memory repository:

```csharp
.Where(x =>
    x.ProcessStatus == 0 &&
    x.PromotionType == "OPEN_DISCOUNT"
)
.OrderBy(x => x.Id)
```

mapping 1:1, không sai lệch hành vi.

---

## 8. dependency injection

### test / dev (in-memory app)

```csharp
services.AddSingleton<IEcomPromotionRepository, InMemoryEcomPromotionRepository>();
services.AddScoped<IEcomPromotionServices, EcomPromotionServices>();
```

### production (quay lại db khi cần)

```csharp
public class DbEcomPromotionRepository : IEcomPromotionRepository
{
    private readonly IADOServices _adoServices;

    public DbEcomPromotionRepository(IADOServices adoServices)
    {
        _adoServices = adoServices;
    }

    public async Task<List<EcomPromotion>> GetPendingOpenDiscountPromotions()
    {
        var result = await _adoServices.ExecProc(
            "SP_EcomPromotion_OpenDiscount_SkyCRM",
            null
        );

        return result.ToList<EcomPromotion>();
    }
}
```

đổi di là xong, service không sửa.

---

## 9. lợi ích đạt được

* bỏ stored procedure khỏi service
* không phụ thuộc database khi test
* code gọn, đúng single responsibility
* rollback nhanh bằng cấu hình
* tương thích c# 7.3

---

## 10. giới hạn cần biết

* dữ liệu không persistence
* không phù hợp multi-instance production
* không có transaction

---

## 11. kết luận

chuyển sang **in-memory app repository** thực chất là:

> thay sql bằng list trong ram
> giữ interface
> đổi implementation
> service sạch hơn, test dễ hơn

đây là cách **đi nhanh – ít rủi ro – đúng bài** cho dev/test/poc.

nếu muốn đi tiếp bước hợp lý tiếp theo:

* preload promotion từ json
* đóng băng dữ liệu (read-only)
* hoặc ghép memory → redis → db theo tầng ưu tiên
