# pipeline pattern

## mục tiêu

- chọn cách tổ chức validation khi rule nhiều và có dependency

---

## các loại validation pattern thường dùng

### guard clause (if trong service/controller)

- dùng khi rule < 5 và không phụ thuộc service khác
- ưu điểm: viết nhanh, không thêm abstraction
- nhược điểm: rule tăng → code dài, khó test, khó tái sử dụng
- tradeoff: tối ưu tốc độ dev ban đầu nhưng scale kém

### validator class (strategy / ivali d ator)

- dùng khi muốn tách validation khỏi service
- ưu điểm: test riêng từng validator dễ, tái sử dụng được
- nhược điểm: rule phụ thuộc data runtime hoặc flow nhiều bước sẽ khó quản lý
- tradeoff: maintain tốt hơn guard nhưng chưa giải quyết orchestration

### specification pattern

- dùng khi rule là business rule domain
- ưu điểm: combine rule and/or, domain model rõ ràng
- nhược điểm: không quản lý thứ tự xử lý và dependency external
- tradeoff: tốt cho domain correctness nhưng không quản lý flow

### fluentvalidation (api layer)

- dùng khi validate dto request api
- ưu điểm: viết nhanh, chuẩn ecosystem .net
- nhược điểm: rule phức tạp + dependency service sẽ rối
- tradeoff: phù hợp input validation, không nên gánh logic hệ thống

### pipeline validation

- dùng khi validation nhiều bước + phụ thuộc data + cần thứ tự
- ưu điểm: flow rõ, thêm rule không sửa code cũ, dừng sớm khi fail
- nhược điểm: setup ban đầu cao hơn
- tradeoff: scale tốt khi hệ thống lớn

---

## kết luận cho hệ thống của bạn

### so sánh

| loại             | phù hợp nhất          | khi hệ thống lớn lên    |
| ---------------- | --------------------- | ----------------------- |
| guard clause     | code nhỏ              | fail                    |
| validator class  | trung bình            | tạm ổn                  |
| specification    | domain rule           | tốt                     |
| pipeline         | service orchestration | rất tốt                 |
| fluentvalidation | api input             | tốt nếu dùng đúng layer |

- chọn: pipeline validation
- lý do: validation nhiều + có integration + phụ thuộc grpc/service
- bổ sung: business rule đặt trong specification bên trong pipeline step

---

## structure đề xuất

### đơn giản

```text
application
├─ pipelines
│   ├─ request_validation_step
│   ├─ enrich_data_step
│   ├─ business_validation_step
│   └─ integration_ready_step
│
├─ specifications
│   ├─ discount_time_valid_spec
│   └─ org_valid_spec
```

### nâng cao

src
├─ application
│ ├─ discounts
│ │ ├─ commands
│ │ │ └─ create_discount_command.cs
│ │ │
│ │ ├─ pipelines
│ │ │ ├─ interfaces
│ │ │ │ └─ ipipeline_step.cs
│ │ │ │
│ │ │ ├─ context
│ │ │ │ └─ discount_validation_context.cs
│ │ │ │
│ │ │ ├─ steps
│ │ │ │ ├─ request_validation_step.cs
│ │ │ │ ├─ enrich_org_step.cs
│ │ │ │ ├─ business_validation_step.cs
│ │ │ │ └─ integration_ready_step.cs
│ │ │ │
│ │ │ └─ validation_pipeline.cs
│ │ │
│ │ ├─ specifications
│ │ │ ├─ discount_time_spec.cs
│ │ │ └─ org_valid_spec.cs
│ │ │
│ │ └─ services
│ │ └─ discount_application_service.cs
│ │
│ └─ abstractions
│ └─ iorg_service.cs
│
├─ domain
│ └─ discounts
│ ├─ entities
│ └─ rules
│
└─ infrastructure
└─ services
└─ org_service.cs

---

## code mẫu pipeline validation

dưới đây là **bộ code tối thiểu chạy được** (console app .net) để bạn thấy pipeline validation hoạt động và có **đoạn add step vào ValidationPipeline** rõ ràng.

---

# program.cs

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Application.Discounts.Commands;
using Application.Discounts.Services;
using Application.Discounts.Pipelines;
using Application.Discounts.Pipelines.Context;
using Application.Discounts.Pipelines.Interfaces;
using Application.Discounts.Pipelines.Steps;
using Application.Abstractions;
using Infrastructure.Services;

var builder = Host.CreateApplicationBuilder(args);

// register service
builder.Services.AddScoped<IOrgService, OrgService>();

// register step (dùng để resolve)
builder.Services.AddScoped<RequestValidationStep>();
builder.Services.AddScoped<EnrichOrgStep>();
builder.Services.AddScoped<BusinessValidationStep>();
builder.Services.AddScoped<IntegrationReadyStep>();

// register pipeline + thứ tự step
builder.Services.AddScoped<ValidationPipeline>(sp =>
{
    return new ValidationPipeline(new IPipelineStep<DiscountValidationContext>[]
    {
        sp.GetRequiredService<RequestValidationStep>(),
        sp.GetRequiredService<EnrichOrgStep>(),
        sp.GetRequiredService<BusinessValidationStep>(),
        sp.GetRequiredService<IntegrationReadyStep>()
    });
});
// đăng ký pipeline
// builder.Services.AddScoped<ValidationPipeline>();

// register application service
builder.Services.AddScoped<DiscountApplicationService>();

var app = builder.Build();

using var scope = app.Services.CreateScope();
var service = scope.ServiceProvider.GetRequiredService<DiscountApplicationService>();

var command = new CreateDiscountCommand
{
    OrgId = 1,
    DiscountName = "test discount",
    StartTime = DateTime.UtcNow.AddMinutes(1),
    EndTime = DateTime.UtcNow.AddHours(2)
};

await service.Handle(command);
```

---

# command

```csharp
namespace Application.Discounts.Commands;

public class CreateDiscountCommand
{
    public int OrgId { get; set; }
    public string DiscountName { get; set; }
    public DateTime StartTime { get; set; }
    public DateTime EndTime { get; set; }
}
```

---

# context

```csharp
using Application.Discounts.Commands;
using Domain.Discounts.Entities;

namespace Application.Discounts.Pipelines.Context;

public class DiscountValidationContext
{
    public CreateDiscountCommand Command { get; set; }
    public OrgEntity Org { get; set; }
    public bool IsValid { get; set; } = true;
    public string Error { get; set; }
}
```

---

# pipeline interface

```csharp
namespace Application.Discounts.Pipelines.Interfaces;

public interface IPipelineStep<T>
{
    Task Execute(T ctx);
}
```

---

# pipeline runner

```csharp
using Application.Discounts.Pipelines.Context;
using Application.Discounts.Pipelines.Interfaces;

namespace Application.Discounts.Pipelines;

public class ValidationPipeline
{
    private readonly IEnumerable<IPipelineStep<DiscountValidationContext>> _steps;

    public ValidationPipeline(IEnumerable<IPipelineStep<DiscountValidationContext>> steps)
    {
        _steps = steps;
    }

    public async Task Run(DiscountValidationContext ctx)
    {
        foreach (var step in _steps)
        {
            await step.Execute(ctx);
            if (!ctx.IsValid) break;
        }
    }
}
```

---

# steps

## request_validation_step

```csharp
using Application.Discounts.Pipelines.Context;
using Application.Discounts.Pipelines.Interfaces;

namespace Application.Discounts.Pipelines.Steps;

public class RequestValidationStep : IPipelineStep<DiscountValidationContext>
{
    public Task Execute(DiscountValidationContext ctx)
    {
        if (string.IsNullOrWhiteSpace(ctx.Command.DiscountName))
        {
            ctx.IsValid = false;
            ctx.Error = "discount name required";
        }

        if (ctx.Command.StartTime >= ctx.Command.EndTime)
        {
            ctx.IsValid = false;
            ctx.Error = "invalid time";
        }

        return Task.CompletedTask;
    }
}
```

---

## enrich_org_step

```csharp
using Application.Abstractions;
using Application.Discounts.Pipelines.Context;
using Application.Discounts.Pipelines.Interfaces;

namespace Application.Discounts.Pipelines.Steps;

public class EnrichOrgStep : IPipelineStep<DiscountValidationContext>
{
    private readonly IOrgService _orgService;

    public EnrichOrgStep(IOrgService orgService)
    {
        _orgService = orgService;
    }

    public async Task Execute(DiscountValidationContext ctx)
    {
        if (!ctx.IsValid) return;

        ctx.Org = await _orgService.GetById(ctx.Command.OrgId);

        if (ctx.Org == null)
        {
            ctx.IsValid = false;
            ctx.Error = "org not found";
        }
    }
}
```

---

## business_validation_step

```csharp
using Application.Discounts.Pipelines.Context;
using Application.Discounts.Pipelines.Interfaces;

namespace Application.Discounts.Pipelines.Steps;

public class BusinessValidationStep : IPipelineStep<DiscountValidationContext>
{
    public Task Execute(DiscountValidationContext ctx)
    {
        if (!ctx.IsValid) return Task.CompletedTask;

        if (!ctx.Org.IsActive)
        {
            ctx.IsValid = false;
            ctx.Error = "org inactive";
        }

        return Task.CompletedTask;
    }
}
```

---

## integration_ready_step

```csharp
using Application.Discounts.Pipelines.Context;
using Application.Discounts.Pipelines.Interfaces;

namespace Application.Discounts.Pipelines.Steps;

public class IntegrationReadyStep : IPipelineStep<DiscountValidationContext>
{
    public Task Execute(DiscountValidationContext ctx)
    {
        if (!ctx.IsValid) return Task.CompletedTask;

        if (ctx.Command.StartTime < DateTime.UtcNow.AddMinutes(-5))
        {
            ctx.IsValid = false;
            ctx.Error = "start too old";
        }

        return Task.CompletedTask;
    }
}
```

---

# application service (nơi gọi pipeline)

```csharp
using Application.Discounts.Commands;
using Application.Discounts.Pipelines;
using Application.Discounts.Pipelines.Context;

namespace Application.Discounts.Services;

public class DiscountApplicationService
{
    private readonly ValidationPipeline _pipeline;

    public DiscountApplicationService(ValidationPipeline pipeline)
    {
        _pipeline = pipeline;
    }

    public async Task Handle(CreateDiscountCommand command)
    {
        var ctx = new DiscountValidationContext
        {
            Command = command
        };

        await _pipeline.Run(ctx);

        if (!ctx.IsValid)
            throw new Exception(ctx.Error);

        Console.WriteLine("validation passed -> create discount");
    }
}
```

---

# abstraction

```csharp
using Domain.Discounts.Entities;

namespace Application.Abstractions;

public interface IOrgService
{
    Task<OrgEntity> GetById(int id);
}
```

---

# domain

```csharp
namespace Domain.Discounts.Entities;

public class OrgEntity
{
    public int Id { get; set; }
    public bool IsActive { get; set; }
}
```

---

# infrastructure

```csharp
using Application.Abstractions;
using Domain.Discounts.Entities;

namespace Infrastructure.Services;

public class OrgService : IOrgService
{
    public Task<OrgEntity> GetById(int id)
    {
        return Task.FromResult(new OrgEntity
        {
            Id = id,
            IsActive = true
        });
    }
}
```

---

## flow

```
command -> validation pipeline -> từng step chạy -> pass -> create discount
```

---

## dấu hiệu nên áp dụng ngay

- validation > 6 rule
- validation phụ thuộc grpc hoặc integration
- service bắt đầu > 300 dòng
- logic validation + orchestration trộn lẫn nhau
