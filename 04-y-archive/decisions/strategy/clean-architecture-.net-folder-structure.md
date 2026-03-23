# clean architecture .net - folder structure

#tag: #clean-architecture #folder-structure #net #perplexity-ai #dependency #const-enum

## mục tiêu

- tách biệt layer: domain thuần túy → application usecase → api http → infra external [web:17].
- dễ test, maintain, scale theo vertical slice.
- tham khảo từ perplexity.ai lọc từ nhiều nguồn uy tín để tổng hợp đầu ra

## structure chuẩn

### cấu trúc

```
src
├─ api                      # http layer
│   ├─ controllers          # controllers xử lý http
│   ├─ dto                  # request/response dto
│   ├─ middleware           # custom middleware
│   └─ validators           # fluentvalidation cho dto
├─ application              # usecase layer
│   ├─ interfaces           # iapplication service
│   ├─ services             # business service, usecase
│   ├─ common               # mapper, exception, result
│   └─ validation
│       ├─ pipeline         # validation pipeline
│       └─ behaviors        # mediatr behaviors
├─ domain                   # business layer (pure)
│   ├─ entities             # domain model, aggregate root
│   ├─ valueobjects         # value object
│   ├─ enums                # domain enum
│   ├─ exceptions           # domain exception
│   ├─ interfaces           # repository, domain service interface
│   ├─ rules                # business rule, validator
│   └─ events               # domain event
└─ infrastructure           # external layer
    ├─ persistence          # ef context, migrations, repository impl
    ├─ services             # external service impl (email, cache)
    ├─ validators           # domain validator factory/impl
    ├─ extensions           # di extension methods
    └─ dependencyinjection  # register services
```

### sự phụ thuộc

| project        | được phụ thuộc vào                     | cấm phụ thuộc vào       |
| -------------- | -------------------------------------- | ----------------------- |
| domain         | .net thuần                             | application, infra, api |
| application    | domain                                 | infra, api              |
| infrastructure | domain, application                    | api                     |
| api            | application (thêm domain nếu cần type) | infra trực tiếp         |

### hằng số và enum

| tầng           | nên chứa enum/const gì?                                                                             | ví dụ cụ thể                                                                             | câu hỏi tự check trước khi đặt vào tầng này                      |
| -------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| domain         | khái niệm business cốt lõi: trạng thái, loại, role, permission, invariant; không dính http/db       | orderstatus, discounttype, paymentmethod, userrole                                       | đây có phải "từ vựng nghiệp vụ" không? business đổi là phải đổi? |
| application    | rule cho use case + orchestration: pagesize, limit kỹ thuật, tên job, feature flag, mã lỗi use case | defaultpagesize, maxretry, "send-email-job", "feature_discount_v2", applicationerrorcode | thay đổi vì logic xử lý / performance / flow use case?           |
| api            | http/ui: route segment, query param, header/cookie key, response message key hoặc code ui           | "api/discounts", "page", "pagesize", "x-correlation-id", "discount.validation.failed"    | chỉ dùng trong controller/middleware/validator dto hoặc client?  |
| infrastructure | db/external: table/schema name, queue/topic name, external status code, provider key                | "discounts" (table), "email-queue", "payments-topic", externalerrorcode                  | chỉ liên quan db, message bus, external service, provider?       |

### mapping clean => layer classic architecture

| clean architecture | layer architecture classic  | ghi chú                                                                                                    |
| ------------------ | --------------------------- | ---------------------------------------------------------------------------------------------------------- |
| domain             | core                        | phần entity, valueobject, enum, rule, domain service interface trong core                                  |
| application        | core + services             | phần use case / app service trong core, và các service thuần orchestrate, không đụng infra, trong services |
| infrastructure     | data + services             | data (db, repo, context) + các service gọi external (email, cache, http...) trong services                 |
| api                | web.api                     | controller, dto, middleware, filter                                                                        |

**cơ sở tài liệu?**
- domain = core: nhiều hướng dẫn gộp domain vào core: entities, valueobjects, rule, domain interfaces. [ardalis](https://ardalis.com/clean-architecture-asp-net-core/)  
- application = core + services:  application layer = use case + service interface/impl; có thể nằm chung trong core, đôi khi tách thêm project services/usecases. [c-sharpcorner](https://www.c-sharpcorner.com/article/clean-architecture-in-asp-net-core-web-api/)
- infrastructure = data + services: infrastructure layer = persistence (data) + external service impl (email, cache, http client) như các bài hướng dẫn mô tả. [c-sharpcorner](https://www.c-sharpcorner.com/article/clean-architecture-in-asp-net-core-web-api/)
- api = web.api :presentation/web api layer = controllers, dto, filters, middleware. [c-sharpcorner](https://www.c-sharpcorner.com/article/clean-architecture-in-asp-net-core-web-api/) 

### ví dụ

```
src
├─ MyApp.Api
│  ├─ Controllers
│  │   └─ DiscountController.cs
│  ├─ Dto
│  │   └─ DiscountRequestDto.cs
│  ├─ Middleware
│  └─ Validators
│      └─ DiscountRequestValidator.cs
├─ MyApp.Application
│  ├─ Interfaces
│  │   └─ IDiscountValidationService.cs
│  ├─ Services
│  │   └─ DiscountValidationService.cs
│  ├─ Common
│  │   └─ Result.cs
│  └─ Validation
│      ├─ Pipeline
│      └─ Behaviors
├─ MyApp.Domain
│  ├─ Entities
│  │   └─ Discount.cs
│  ├─ ValueObjects
│  │   └─ Percentage.cs
│  ├─ Rules
│  │   └─ PercentageRangeRule.cs
│  ├─ Events
│  ├─ Exceptions
│  └─ Interfaces
│      └─ IDiscountRepository.cs
└─ MyApp.Infrastructure
   ├─ Persistence
   │   ├─ ApplicationDbContext.cs
   │   └─ DiscountRepository.cs
   ├─ Services
   │   └─ EmailService.cs
   ├─ Validators
   │   └─ DiscountValidatorFactory.cs
   ├─ Extensions
   │   └─ ServiceCollectionExtensions.cs
   └─ DependencyInjection
       └─ InfrastructureServiceRegistration.cs
```

- tối giản rule kèm folder (để dán bàn):

| project              | chứa gì chính                              | ví dụ file                               |
| -------------------- | ------------------------------------------ | ---------------------------------------- |
| MyApp.Domain         | model, rule, interface                     | Discount, PercentageRangeRule            |
| MyApp.Application    | use case, service, result, pipeline        | DiscountValidationService, Result        |
| MyApp.Infrastructure | ef, repo impl, external service            | ApplicationDbContext, DiscountRepository |
| MyApp.Api            | controller, dto, middleware, validator dto | DiscountController, DiscountRequestDto   |

## rule reference

```
api → application → domain
infrastructure → domain + application
```

## discount project mapping

```
domain/discounts/ ← PercentageDiscountValidator.cs
domain/rules/percentage/ ← PercentageRangeRule.cs
application/services/ ← DiscountValidationService.cs
api/controllers/ ← DiscountController.cs
infrastructure/validators/ ← DiscountValidatorFactory.cs
```

## bước tiếp

```
1. dotnet new sln
2. dotnet new classlib -n Domain
3. add reference theo rule
4. implement từng layer
```

## tham khảo

- dùng file này họp team/explain. [dev](https://dev.to/ismcagdas/an-opinionated-solution-structure-for-aspnet-core-projects-8ld)
- print ra dán desk để reference khi code. [youtube](https://www.youtube.com/watch?v=ipyJPdaZ10w)
- sau 2 ngày: đã setup xong solution. [telerik](https://www.telerik.com/blogs/getting-started-domain-driven-design-aspnet-core)
