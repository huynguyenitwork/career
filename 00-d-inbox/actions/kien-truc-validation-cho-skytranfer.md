# kiến trúc validation cho skytranfer

## mục tiêu kiến trúc

- payload request dài → cần validation nhiều bước
- discount type sẽ **tăng dần theo thời gian**
- controller phải **mỏng**
- validation **không phình thành file 500–1000 dòng**
- thêm discount mới **không sửa code cũ**

kiến trúc dùng kết hợp các pattern:

- Pipeline Pattern
- Strategy Pattern
- Factory Pattern
- Chain of Responsibility

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
    common discount validation step
    ↓
    discount type validation step
        ↓
        discount validator (strategy)
            ↓
            rule chain
↓
business logic
```

---

# 2. phân tầng validation

## request validator (schema)

mục tiêu

- bảo vệ API contract
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

validation dài → chia thành step

pipeline

```
validation pipeline
   ├─ campaign validation step
   ├─ common discount validation step
   └─ discount type validation step
```

mỗi step

```
1 domain rule group
```

---

# 4. discount validator (strategy)

mỗi discount type có validator riêng

ví dụ

```
percentage discount validator
fixed amount validator
buy-x-get-y validator
```

---

# 5. rule chain

validator nhiều rule → chia nhỏ

```
percentage validator
   ↓
   percentage range rule
   ↓
   campaign limit rule
   ↓
   user eligibility rule
```

---

# 6. ví dụ code (1 file)

ví dụ minh họa toàn bộ flow trong **1 file**

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

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
    // pipeline step interface
    // -----------------------------

    public interface IValidationStep
    {
        Task ExecuteAsync(DiscountContext context);
    }

    // -----------------------------
    // pipeline runner
    // -----------------------------

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
            {
                await step.ExecuteAsync(context);
            }
        }
    }

    // -----------------------------
    // campaign validation step
    // -----------------------------

    public class CampaignValidationStep : IValidationStep
    {
        public Task ExecuteAsync(DiscountContext context)
        {
            // giả lập rule
            bool campaignActive = true;

            if (!campaignActive)
                throw new Exception("campaign inactive");

            return Task.CompletedTask;
        }
    }

    // -----------------------------
    // common discount validation
    // -----------------------------

    public class CommonDiscountValidationStep : IValidationStep
    {
        public Task ExecuteAsync(DiscountContext context)
        {
            if (context.Request.ExpireDate <= DateTime.UtcNow)
                throw new Exception("discount expired");

            return Task.CompletedTask;
        }
    }

    // -----------------------------
    // discount validator interface
    // -----------------------------

    public interface IDiscountValidator
    {
        string DiscountType { get; }

        Task ValidateAsync(DiscountContext context);
    }

    // -----------------------------
    // percentage rule
    // -----------------------------

    public interface IDiscountRule
    {
        Task ValidateAsync(DiscountContext context);
    }

    public class PercentageRangeRule : IDiscountRule
    {
        public Task ValidateAsync(DiscountContext context)
        {
            var value = context.Request.Value;

            if (value <= 0 || value > 100)
                throw new Exception("percentage must be 1-100");

            return Task.CompletedTask;
        }
    }

    // -----------------------------
    // percentage validator
    // -----------------------------

    public class PercentageDiscountValidator : IDiscountValidator
    {
        public string DiscountType => "percentage";

        private readonly IEnumerable<IDiscountRule> _rules;

        public PercentageDiscountValidator(IEnumerable<IDiscountRule> rules)
        {
            _rules = rules;
        }

        public async Task ValidateAsync(DiscountContext context)
        {
            foreach (var rule in _rules)
            {
                await rule.ValidateAsync(context);
            }
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
            var validator = _validators
                .FirstOrDefault(v => v.DiscountType.Equals(type, StringComparison.OrdinalIgnoreCase));

            if (validator == null)
                throw new Exception($"unsupported discount type {type}");

            return validator;
        }
    }

    // -----------------------------
    // discount type validation step
    // -----------------------------

    public class DiscountTypeValidationStep : IValidationStep
    {
        private readonly DiscountValidatorFactory _factory;

        public DiscountTypeValidationStep(DiscountValidatorFactory factory)
        {
            _factory = factory;
        }

        public async Task Execute(DiscountContext context)
        {
            var validator = _factory.Get(context.Request.DiscountType);

            await validator.ValidateAsync(context);
        }
    }

    // -----------------------------
    // service validation entry
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
    // controller example
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
}
```

---

# 7. cách thêm discount mới

chỉ cần

```
1 tạo validator class
2 implement IDiscountValidator
3 register DI
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
controller chứa business rule
```

hoặc

```
validator kiểm tra nhiều discount type
```

---

# kết luận

kiến trúc validation cuối

```
controller
↓
request validator
↓
service validation pipeline
↓
discount validator
↓
rule chain
```
cấu trúc thư mục đề xuất

```
src
├─ api
│   ├─ controllers
│   │    DiscountController.cs
│   │
│   ├─ requests
│   │    CreateDiscountRequest.cs
│   │
│   └─ validators
│        CreateDiscountRequestValidator.cs
│
├─ application
│   ├─ services
│   │    DiscountValidationService.cs
│   │
│   └─ validation
│        ├─ pipeline
│        │    ValidationPipeline.cs
│        │
│        └─ steps
│             CampaignValidationStep.cs
│             CommonDiscountValidationStep.cs
│             DiscountTypeValidationStep.cs
│
├─ domain
│   ├─ validators
│   │    IDiscountValidator.cs
│   │
│   ├─ rules
│   │    IDiscountRule.cs
│   │
│   └─ discounts
│        ├─ percentage
│        │     PercentageDiscountValidator.cs
│        │     PercentageRangeRule.cs
│        │
│        ├─ fixed
│        │     FixedAmountDiscountValidator.cs
│        │
│        └─ buyxgety
│              BuyXGetYDiscountValidator.cs
│
└─ infrastructure
    DiscountValidatorFactory.cs
```

đặc tính đạt được

- controller mỏng
- validation dài nhưng **không phình file**
- rule tách theo domain
- thêm discount type **không sửa code cũ**
- hệ thống promotion **scale tốt khi rule tăng mạnh**.
