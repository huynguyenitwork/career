# kiến trúc validation cho skytransfer 
_version 1.0.1_

## mục tiêu kiến trúc

- payload request dài → cần validation nhiều bước
- discount type sẽ **tăng dần theo thời gian (3–8 type)**
- rule validation có thể **10–50 rule**
- controller phải **mỏng**
- validation **không phình thành file 500–1000 dòng**
- thêm discount mới **không sửa code cũ**
- rule có thể **dùng lại cho nhiều discount type**

kiến trúc dùng kết hợp:

- pipeline pattern
- strategy pattern
- factory pattern
- chain of responsibility
- **generic rule binding (compile-time)**

generic rule binding giúp:

- rule bind trực tiếp vào validator
- di container resolve đúng rule
- **không cần filter runtime**

---

# 1. kiến trúc validation tổng thể

luồng request

```
http request
↓
controller
↓
request validator (schema validation)
↓
service validation pipeline
    ↓
    campaign validation step
    ↓
    discount type validation step
        ↓
        discount validator (strategy)
            ↓
            rule chain (generic rules)
↓
business logic
```

---

# 2. phân tầng validation

## request validator (schema)

mục tiêu

- bảo vệ api contract
- kiểm tra **shape dữ liệu**

ví dụ rule

- request null
- discountType null
- value < 0
- string length

---

## service validation

mục tiêu

- kiểm tra **domain rule**

ví dụ

| rule               |
| ------------------ |
| campaign tồn tại   |
| campaign active    |
| discount expire    |
| discount quota     |
| discount type rule |

---

# 3. validation pipeline

validation dài → chia step

pipeline

```
validation pipeline
   ├─ campaign validation step
   └─ discount type validation step
```

mỗi step

```
1 domain rule group
```

step cuối sẽ gọi validator theo discount type.

---

# 4. discount validator (strategy)

mỗi discount type có validator riêng

ví dụ

```
percentage discount validator
fixed amount validator
tiered discount validator
buy-x-get-y validator
shipping discount validator
```

validator chỉ chứa

```
rule chain của type đó
```

---

# 5. rule chain (generic rule)

rule bind trực tiếp vào validator bằng generic

```
IDiscountRule<TValidator>
```

ví dụ

```
percentage validator
    ↓
    percentage range rule
    ↓
    expire date rule (shared)
```

điểm quan trọng

```
rule được inject đúng validator từ DI
```

không cần

```
AppliesTo()
switch(discountType)
runtime filtering
```

---

# 6. ví dụ code (1 file)

code minh họa toàn bộ flow **pipeline + strategy + generic rule + DI**

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.DependencyInjection;

namespace DiscountValidationExample
{
    // -----------------------------
    // request model
    // -----------------------------

    public class CreateDiscountRequest
    {
        public string DiscountType { get; set; }
        public decimal Value { get; set; }
        public DateTime ExpireDate { get; set; }
    }

    public class DiscountContext
    {
        public CreateDiscountRequest Request { get; }

        public DiscountContext(CreateDiscountRequest request)
        {
            Request = request;
        }
    }

    // -----------------------------
    // request validator
    // -----------------------------

    public class CreateDiscountRequestValidator
    {
        public void Validate(CreateDiscountRequest request)
        {
            if (request == null)
                throw new Exception("request null");

            if (string.IsNullOrEmpty(request.DiscountType))
                throw new Exception("discountType required");

            if (request.Value < 0)
                throw new Exception("value must be positive");
        }
    }

    // -----------------------------
    // pipeline step
    // -----------------------------

    public interface IValidationStep
    {
        Task ExecuteAsync(DiscountContext context);
    }

    public class ValidationPipeline
    {
        private readonly IEnumerable<IValidationStep> _steps;

        public ValidationPipeline(IEnumerable<IValidationStep> steps)
        {
            _steps = steps;
        }

        public async Task ExecuteAsync(DiscountContext context)
        {
            foreach (var step in _steps)
                await step.ExecuteAsync(context);
        }
    }

    // -----------------------------
    // campaign validation
    // -----------------------------

    public class CampaignValidationStep : IValidationStep
    {
        public Task ExecuteAsync(DiscountContext context)
        {
            bool campaignActive = true;

            if (!campaignActive)
                throw new Exception("campaign inactive");

            return Task.CompletedTask;
        }
    }

    // -----------------------------
    // validator interface
    // -----------------------------

    public interface IDiscountValidator
    {
        string DiscountType { get; }

        Task ValidateAsync(DiscountContext context);
    }

    // -----------------------------
    // generic rule interface
    // -----------------------------

    public interface IDiscountRule<TValidator>
        where TValidator : IDiscountValidator
    {
        Task ValidateAsync(DiscountContext context);
    }

    // -----------------------------
    // percentage validator
    // -----------------------------

    public class PercentageDiscountValidator : IDiscountValidator
    {
        public string DiscountType => "percentage";

        private readonly IEnumerable<IDiscountRule<PercentageDiscountValidator>> _rules;

        public PercentageDiscountValidator(
            IEnumerable<IDiscountRule<PercentageDiscountValidator>> rules)
        {
            _rules = rules;
        }

        public async Task ValidateAsync(DiscountContext context)
        {
            foreach (var rule in _rules)
                await rule.ValidateAsync(context);
        }
    }

    // -----------------------------
    // fixed validator
    // -----------------------------

    public class FixedDiscountValidator : IDiscountValidator
    {
        public string DiscountType => "fixed";

        private readonly IEnumerable<IDiscountRule<FixedDiscountValidator>> _rules;

        public FixedDiscountValidator(
            IEnumerable<IDiscountRule<FixedDiscountValidator>> rules)
        {
            _rules = rules;
        }

        public async Task ValidateAsync(DiscountContext context)
        {
            foreach (var rule in _rules)
                await rule.ValidateAsync(context);
        }
    }

    // -----------------------------
    // rules
    // -----------------------------

    public class PercentageRangeRule
        : IDiscountRule<PercentageDiscountValidator>
    {
        public Task ValidateAsync(DiscountContext context)
        {
            var value = context.Request.Value;

            if (value <= 0 || value > 100)
                throw new Exception("percentage must be 1-100");

            return Task.CompletedTask;
        }
    }

    public class FixedAmountRule
        : IDiscountRule<FixedDiscountValidator>
    {
        public Task ValidateAsync(DiscountContext context)
        {
            if (context.Request.Value <= 0)
                throw new Exception("fixed amount must be positive");

            return Task.CompletedTask;
        }
    }

    // shared rule
    public class ExpireDateRule :
        IDiscountRule<PercentageDiscountValidator>,
        IDiscountRule<FixedDiscountValidator>
    {
        public Task ValidateAsync(DiscountContext context)
        {
            if (context.Request.ExpireDate <= DateTime.UtcNow)
                throw new Exception("discount expired");

            return Task.CompletedTask;
        }
    }

    // -----------------------------
    // validator factory
    // -----------------------------

    public class DiscountValidatorFactory
    {
        private readonly IEnumerable<IDiscountValidator> _validators;

        public DiscountValidatorFactory(IEnumerable<IDiscountValidator> validators)
        {
            _validators = validators;
        }

        public IDiscountValidator Get(string type)
        {
            var validator = _validators.FirstOrDefault(v =>
                v.DiscountType.Equals(type, StringComparison.OrdinalIgnoreCase));

            if (validator == null)
                throw new Exception($"unsupported discount type {type}");

            return validator;
        }
    }

    // -----------------------------
    // validation step
    // -----------------------------

    public class DiscountTypeValidationStep : IValidationStep
    {
        private readonly DiscountValidatorFactory _factory;

        public DiscountTypeValidationStep(DiscountValidatorFactory factory)
        {
            _factory = factory;
        }

        public async Task ExecuteAsync(DiscountContext context)
        {
            var validator = _factory.Get(context.Request.DiscountType);

            await validator.ValidateAsync(context);
        }
    }

    // -----------------------------
    // validation service
    // -----------------------------

    public class DiscountValidationService
    {
        private readonly ValidationPipeline _pipeline;

        public DiscountValidationService(ValidationPipeline pipeline)
        {
            _pipeline = pipeline;
        }

        public async Task ValidateAsync(CreateDiscountRequest request)
        {
            var context = new DiscountContext(request);

            await _pipeline.ExecuteAsync(context);
        }
    }

    // -----------------------------
    // controller
    // -----------------------------

    public class DiscountController
    {
        private readonly CreateDiscountRequestValidator _requestValidator;
        private readonly DiscountValidationService _service;

        public DiscountController(
            CreateDiscountRequestValidator requestValidator,
            DiscountValidationService service)
        {
            _requestValidator = requestValidator;
            _service = service;
        }

        public async Task CreateDiscount(CreateDiscountRequest request)
        {
            _requestValidator.Validate(request);

            await _service.ValidateAsync(request);

            Console.WriteLine("discount created");
        }
    }

    // -----------------------------
    // DI
    // -----------------------------

    public static class DependencyInjection
    {
        public static IServiceCollection AddDiscountValidation(
            this IServiceCollection services)
        {
            services.AddScoped<CreateDiscountRequestValidator>();

            services.AddScoped<IValidationStep, CampaignValidationStep>();
            services.AddScoped<IValidationStep, DiscountTypeValidationStep>();

            services.AddScoped<ValidationPipeline>();

            services.AddScoped<IDiscountValidator, PercentageDiscountValidator>();
            services.AddScoped<IDiscountValidator, FixedDiscountValidator>();

            services.AddScoped<IDiscountRule<PercentageDiscountValidator>, PercentageRangeRule>();
            services.AddScoped<IDiscountRule<FixedDiscountValidator>, FixedAmountRule>();

            services.AddScoped<IDiscountRule<PercentageDiscountValidator>, ExpireDateRule>();
            services.AddScoped<IDiscountRule<FixedDiscountValidator>, ExpireDateRule>();

            services.AddScoped<DiscountValidatorFactory>();
            services.AddScoped<DiscountValidationService>();

            return services;
        }
    }
}
```

---

# 7. cách thêm discount mới

chỉ cần

```
1 tạo validator
2 tạo rule generic
3 register DI
```

ví dụ

```
TieredDiscountValidator
IDiscountRule<TieredDiscountValidator>
```

không sửa

```
controller
pipeline
factory
service
```

---

# 8. dấu hiệu kiến trúc sai

loại ngay nếu thấy

```
switch(discountType)
```

hoặc

```
AppliesTo()
```

hoặc

```
validator chứa nhiều discount type
```

---

# 9. cấu trúc thư mục đề xuất

```
src
├─ api
│   ├─ controllers
│   │     DiscountController.cs
│   ├─ requests
│   │     CreateDiscountRequest.cs
│   └─ validators
│         CreateDiscountRequestValidator.cs
├─ application
│   ├─ services
│   │     DiscountValidationService.cs
│   └─ validation
│        ├─ pipeline
│        │     ValidationPipeline.cs
│        └─ steps
│              CampaignValidationStep.cs
│              DiscountTypeValidationStep.cs
├─ domain
│   ├─ validators
│   │     IDiscountValidator.cs
│   ├─ rules
│   │     IDiscountRule.cs
│   │     shared
│   │         ExpireDateRule.cs
│   │     percentage
│   │         PercentageRangeRule.cs
│   │     fixed
│   │         FixedAmountRule.cs
│   └─ discounts
│        ├─ percentage
│        │     PercentageDiscountValidator.cs
│        ├─ fixed
│        │     FixedDiscountValidator.cs
│        ├─ tiered
│        │     TieredDiscountValidator.cs
│        ├─ buyxgety
│        │     BuyXGetYDiscountValidator.cs
│        └─ shipping
│              ShippingDiscountValidator.cs
└─ infrastructure
      DiscountValidatorFactory.cs
      DependencyInjection.cs
```

---

# kết luận

kiến trúc validation cuối

```
controller
↓
request validator
↓
validation pipeline
↓
discount validator (strategy)
↓
generic rule chain
```

đặc tính đạt được

- controller mỏng
- validation dài nhưng **không phình file**
- rule tách theo domain
- rule có thể **dùng cho nhiều discount type**
- thêm discount type **không sửa code cũ**
- hệ thống promotion **scale tốt khi rule tăng mạnh**
