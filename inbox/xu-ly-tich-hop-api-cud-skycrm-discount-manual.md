# mục tiêu tài liệu

- khóa quyết định cách gọi external api sau crud discount
- tối ưu: sửa ít code + giữ crud độc lập + đảm bảo external được gọi đúng thời điểm
- loại sớm giải pháp gây rollback vô nghĩa hoặc tăng cognitive load vận hành

---

# so sánh phương pháp (gate-first)

## decorator pattern

### bản chất
- bọc root service bằng layer trung gian
- decorator.create → root.create → gọi external api

### payoff
- kiểm soát transaction toàn phần
- rollback được nếu external là điều kiện bắt buộc

### tiêu chí loại
- rollback crud discount không tạo thêm giá trị nghiệp vụ
- tăng coupling vào di registration
- tăng effort debug stack call
- tăng rủi ro sửa lan khi thay đổi service

### kết luận
- loại vì payoff thấp hơn chi phí bảo trì

---

## event-driven

### bản chất
- crud xong → raise domain event
- handler subscribe → gọi external api async

### payoff
- tách biệt domain và integration
- scale tốt khi external chậm hoặc tăng tải
- dễ bật/tắt hoặc retry bằng queue

### tiêu chí loại
- không đảm bảo timing gọi external ngay sau crud
- khó debug vì execution phân tán
- response external không nằm trong request context
- tăng chi phí infra (queue, retry, monitoring)

### kết luận
- loại vì không cần eventual consistency

---

## action filter

### bản chất
- hook sau controller action
- intercept request + response → gọi external

### payoff
- sửa tối thiểu code domain
- giữ crud độc lập transaction
- giữ được request context đầy đủ để log/audit
- dễ bật/tắt bằng attribute

### tradeoff chấp nhận
- request bị blocking bởi external
- phụ thuộc performance external api

### kết luận
- phù hợp khi external nhanh và chỉ là post-process

---

# bảng quyết định (đủ dùng để chọn)

| tiêu chí | decorator | event | filter |
|----------|-----------|-------|--------|
| sửa domain code | cao | thấp | rất thấp |
| rollback crud | có | không | không |
| độ phức tạp vận hành | cao | cao | thấp |
| debug trace | khó | rất khó | dễ |
| blocking request | có | không | có |
| phù hợp nghiệp vụ hiện tại | không | không | có |

---

# quyết định cuối

## chọn: action filter

### payoff đạt được
- giảm sửa domain layer
- giữ crud discount độc lập external system
- giữ khả năng audit request/response
- giảm chi phí maintain dài hạn

### rủi ro còn lại
- external api chậm làm tăng latency
- external api fail cần cơ chế log + theo dõi

---

# điều kiện áp dụng (gate runtime)

- external api p95 latency < 1s
- external không phải business critical
- crud discount phải thành công độc lập external
- chấp nhận retry thủ công nếu external fail

---

# trigger chuyển kiến trúc

- external p95 > 1s → chuyển event + queue
- external fail rate > 5% → chuyển event + retry policy
- cần multi external subscriber → chuyển event bus

---

# thực hiện

## bước 1: tạo filter

file: `Filters/DiscountPostProcessFilter.cs`

```csharp
using Dcorp.Web.Framework.Filters;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using System.Threading.Tasks;

namespace Dcorp.Web.Api.Filters
{
    public class DiscountPostProcessFilter : IAsyncActionFilter
    {
        private readonly ILogger<DiscountPostProcessFilter> _logger;
        private readonly IExternalApiClient _externalApi;

        public DiscountPostProcessFilter(
            ILogger<DiscountPostProcessFilter> logger,
            IExternalApiClient externalApi)
        {
            _logger = logger;
            _externalApi = externalApi;
        }

        public async Task OnActionExecutionAsync(
            ActionExecutingContext context,
            ActionExecutionDelegate next)
        {
            var executedContext = await next();

            if (executedContext.Result is OkObjectResult okResult)
            {
                var actionName = context.ActionDescriptor.RouteValues["action"];

                if (actionName == "Create" ||
                    actionName == "Update" ||
                    actionName == "Delete")
                {
                    await ProcessExternalApi(context, okResult);
                }
            }
        }

        private async Task ProcessExternalApi(
            ActionExecutingContext context, 
            OkObjectResult result)
        {
            try
            {
                var request = new
                {
                    action = context.ActionDescriptor.RouteValues["action"],
                    arguments = context.ActionArguments,
                    response = result.Value
                };

                await _externalApi.PostDiscountChangedAsync(request);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "external api call failed");
            }
        }
    }
}
````

---

## bước 2: tạo external client interface

file: `Services/IExternalApiClient.cs`

```csharp
using System.Threading.Tasks;

namespace Dcorp.Web.Api.Services
{
    public interface IExternalApiClient
    {
        Task PostDiscountChangedAsync(object payload);
    }
}
```

---

## bước 3: implement external client

file: `Services/ExternalApiClient.cs`

```csharp
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace Dcorp.Web.Api.Services
{
    public class ExternalApiClient : IExternalApiClient
    {
        private readonly HttpClient _http;
        private readonly IConfiguration _config;

        public ExternalApiClient(
            HttpClient http, 
            IConfiguration config)
        {
            _http = http;
            _config = config;
        }

        public async Task PostDiscountChangedAsync(object payload)
        {
            var url = _config["ExternalApi:DiscountWebhook"];
            var json = JsonSerializer.Serialize(payload);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _http.PostAsync(url, content);
            response.EnsureSuccessStatusCode();
        }
    }
}
```

---

## bước 4: đăng ký di

file: `startup.cs` hoặc `program.cs`

```csharp
services.AddScoped<DiscountPostProcessFilter>();
services.AddHttpClient<IExternalApiClient, ExternalApiClient>();
```

---

## bước 5: apply filter

file: `Controllers/DiscountController.cs`

```csharp
[ServiceFilter(typeof(DiscountPostProcessFilter))]
[HttpPost]
public async Task Create(int orgId, CreateDiscountModel model, string lang)
{
    var result = await _discount.Create(model);
    return Ok(result);
}

[ServiceFilter(typeof(DiscountPostProcessFilter))]
[HttpPut]
public async Task Update(int orgId, DiscountModel model, string lang)
{
    var result = await _discount.Update(model);
    return Ok(result);
}

[ServiceFilter(typeof(DiscountPostProcessFilter))]
[HttpDelete]
public async Task Delete(int[] ids)
{
    var result = await _discount.Delete(ids);
    return Ok(result);
}
```

---

## bước 6: config

file: `appsettings.json`

```json
{
  "ExternalApi": {
    "DiscountWebhook": "https://external-api.com/webhook/discount"
  }
}
```

---

# checklist triển khai

* [ ] tạo filter
* [ ] tạo external client interface
* [ ] implement external client
* [ ] đăng ký di
* [ ] apply attribute vào controller
* [ ] thêm config external endpoint
* [ ] test success path
* [ ] test external fail path
* [ ] thêm monitoring log external fail

---

# rollback nhanh khi production lỗi

* xóa attribute filter khỏi controller
* deploy lại không cần thay domain logic