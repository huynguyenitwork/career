# tài liệu kỹ thuật

## các lỗi di lifetime khi chuyển sang in-memory app & backgroundservice

---

## 1. bối cảnh chung

bạn đang:

* chuyển từ:

  * db / stored procedure
  * sang **in-memory app** (list, dictionary, cache trong ram)
* sử dụng:

  * `backgroundservice`
  * `httpclient`
  * cache provider
* giữ nguyên interface + service, **chỉ đổi cách lưu trữ**

hệ quả:
liên tục gặp lỗi runtime liên quan đến **dependency injection lifetime**.

---

## 2. các lỗi đã gặp (triệu chứng)

### lỗi 1

```
cannot resolve scoped service 'iecompromotionservices' from root provider
```

### lỗi 2

```
cannot resolve scoped service 'icacheprovider' from root provider
```

### lỗi 3

```
unable to resolve service for type 'httpclient'
```

### lỗi 4

backgroundservice không chạy / chạy nhưng crash ngầm

---

## 3. nguyên nhân gốc (root cause)

### nguyên nhân duy nhất, lặp đi lặp lại

> **singleton đang cố dùng scoped service**

giải thích ngắn gọn:

* `backgroundservice` → luôn là **singleton**
* root provider chỉ tạo được:

  * singleton
  * transient
* **không được phép** tạo scoped từ root
* nhưng bạn:

  * inject scoped vào singleton
  * hoặc singleton gián tiếp phụ thuộc scoped

di không báo compile-time
→ nó trả thù lúc runtime.

---

## 4. những chỗ gây lỗi cụ thể trong code của bạn

### 4.1 cache provider đăng ký sai lifetime

```csharp
services.AddScoped<ICacheProvider, CacheProvider>(); // sai
```

trong khi:

* cache là in-memory
* dùng chung toàn app
* bị inject vào:

  * parameterservices (singleton)
  * backgroundservice
  * skycloudservices

=> **scoped cache = thiết kế sai**

---

### 4.2 singleton service inject scoped

```csharp
services.AddSingleton<IParameterServices, ParameterServices>();
```

nhưng `ParameterServices` có:

```csharp
private readonly ICacheProvider _cache;
```

→ singleton + scoped = lỗi chắc chắn.

---

### 4.3 backgroundservice inject service sai cách

* backgroundservice = singleton
* không được inject:

  * repository scoped
  * cache scoped
  * service scoped

nếu cần dùng → **phải createscope()**

---

## 5. cách khắc phục đúng (chuẩn kiến trúc)

### 5.1 nguyên tắc vàng về lifetime

* singleton:

  * stateless
  * cache
  * helper
  * backgroundservice
* scoped:

  * dbcontext
  * repository có db
  * unit of work
* transient:

  * validator
  * mapper
  * object dùng xong bỏ

> **singleton không bao giờ inject scoped**

---

### 5.2 cache provider – cách đúng duy nhất trong case này

```csharp
services.AddSingleton<ICacheProvider, CacheProvider>();
```

lý do:

* cache không gắn request
* cache dùng chung
* cache sống theo app

---

### 5.3 in-memory repository / service

```csharp
services.AddSingleton<IParameterRepository, InMemoryParameterRepository>();
services.AddSingleton<IParameterServices, ParameterServices>();

services.AddSingleton<IEcomPromotionRepository, InMemoryEcomPromotionRepository>();
services.AddSingleton<IEcomPromotionServices, EcomPromotionServices>();
```

điều kiện:

* không dbcontext
* không giữ state mutable nguy hiểm
* chỉ đọc / cập nhật có kiểm soát

---

### 5.4 backgroundservice dùng scoped service đúng cách

```csharp
public class MasterDataTaskScheduleServices : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;

    public MasterDataTaskScheduleServices(IServiceScopeFactory scopeFactory)
    {
        _scopeFactory = scopeFactory;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            using (var scope = _scopeFactory.CreateScope())
            {
                var svc = scope.ServiceProvider
                               .GetRequiredService<IEcomPromotionServices>();

                await svc.GetPendingOpenDiscountPromotions();
            }

            await Task.Delay(10000, stoppingToken);
        }
    }
}
```

keyword phải nhớ:
**createscope()**

---

### 5.5 httpclient đúng cách

```csharp
services.AddHttpClient<ISkyCloudServices, SkyCloudServices>();
```

và trong `SkyCloudServices`:

```csharp
public SkyCloudServices(HttpClient httpClient)
{
    _httpClient = httpClient;
}
```

không tự new httpclient.

---

## 6. cấu hình di cuối cùng (đã sửa đúng)

```csharp
// ecom → skytransfer
services.AddSingleton<IEcomPromotionRepository, InMemoryEcomPromotionRepository>();
services.AddSingleton<IEcomPromotionServices, EcomPromotionServices>();

// cache
services.AddSingleton<ICacheProvider, CacheProvider>();
services.AddHostedService<CacheServices>();

// skycloud
services.AddHttpClient<ISkyCloudServices, SkyCloudServices>();
services.AddHostedService<MasterDataTaskScheduleServices>();

// parameters
services.AddSingleton<IParameterRepository, InMemoryParameterRepository>();
services.AddSingleton<IParameterServices, ParameterServices>();
```

---

## 7. checklist tránh tái phạm (20/80)

* backgroundservice luôn là singleton
* cache in-memory luôn là singleton
* singleton không inject scoped
* scoped chỉ được resolve:

  * trong controller
  * hoặc trong createscope()
* lỗi lifetime → **đừng debug logic**

---

## 8. kết luận

vấn đề bạn gặp **không phải do code nghiệp vụ**
mà là do:

> **lifetime không nhất quán khi chuyển sang in-memory + backgroundservice**

hiểu đúng lifetime →

* app chạy ổn
* background chạy đều
* cache dùng an toàn
* không còn lỗi “cannot resolve scoped service”

đây là loại kiến thức **đắt giá**, dính 1 lần là nhớ cả đời.
