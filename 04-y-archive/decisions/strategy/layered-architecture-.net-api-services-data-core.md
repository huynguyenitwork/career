# layered architecture .net (api / services / data / core)

#tag: #layered-architecture #folder-structure #net #dependency #const-enum [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)

---

## mục tiêu

- mô tả rõ 4 layer đang dùng trong solution .net: core (business) ← data (dal) ← services (application) ← api (presentation). [stackify](https://stackify.com/n-tier-architecture/)
- thống nhất rule phụ thuộc, vị trí entity/dto/enum/const để giảm tranh luận thiết kế và rủi ro "god layer". [dev](https://dev.to/pouria_ghadiri/layered-architecture-in-aspnet-core-simple-structured-and-still-relevant-part-2-31m3)
- bám theo thực tế các hệ thống n‑tier .net: presentation layer, business/application layer, data access layer, core domain. [stackoverflow](https://stackoverflow.com/questions/10761440/example-of-4-tier-for-n-tier-architecture)

---

## structure chuẩn

### cấu trúc solution

```
src
├─ Api                # presentation/http layer
│  ├─ Controllers     # controller, endpoint
│  ├─ Dto             # request/response dto
│  ├─ Filters         # exception filter, action filter
│  └─ Middleware      # custom middleware
├─ Services           # application/service layer
│  ├─ Interfaces      # app/service interface
│  ├─ Services        # app service, orchestration use case
│  ├─ Dto             # dto nội bộ giữa services/api
│  └─ Common          # result, paging, mapper helper
├─ Data               # data access layer (dal)
│  ├─ Context         # dbcontext, unit of work
│  ├─ Repositories    # repository impl
│  ├─ Configurations  # ef configuration, mapping
│  └─ Migrations      # migrations
└─ Core               # core business layer
   ├─ Entities        # domain model, aggregate root
   ├─ ValueObjects    # value object
   ├─ Enums           # domain enum
   ├─ Rules           # business rule, invariant
   ├─ Exceptions      # domain exception
   └─ Interfaces      # repository, domain service interface
```

- cấu trúc này là dạng layered/n‑tier kinh điển trong .net: presentation, application/service, data access, domain/core. [aspnetboilerplate](https://aspnetboilerplate.com/Pages/Documents/NLayer-Architecture)
- core không tham chiếu lên bất kỳ layer nào; mọi layer còn lại đều có thể tham chiếu core để dùng model và rule. [c-sharpcorner](https://www.c-sharpcorner.com/article/building-a-clean-asp-net-core-api-with-c-sharp-13-ef-core-and-ddd/)

---

## sự phụ thuộc (dependency rules)

### mô hình bạn đang dùng

- data phụ thuộc core.
- services phụ thuộc data, core.
- api phụ thuộc core, data, services.

đóng thành bảng:

| project  | có thể tham chiếu tới | bị tham chiếu bởi   | cấm tham chiếu tới        |
| -------- | --------------------- | ------------------- | ------------------------- |
| Core     | — (chỉ .net base)     | Data, Services, Api | Data, Services, Api       |
| Data     | Core                  | Services, Api       | — (tránh vòng ngược Core) |
| Services | Core, Data            | Api                 | —                         |
| Api      | Core, Data, Services  | —                   | —                         |

- đây là biến thể "relaxed layered" – api có thể dùng trực tiếp data/service, tương tự nhiều ví dụ n‑tier cũ trong .net. [stackify](https://stackify.com/n-tier-architecture/)
- điểm cần ghim: mọi truy cập db đều phải đi qua project data, mọi khái niệm nghiệp vụ phải xuất phát từ core (entity/enum/rule). [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)

---

## hằng số và enum theo layer

| layer    | nên chứa enum/const gì?                                                                                       | ví dụ cụ thể                                                                   | câu hỏi tự check trước khi đặt                                  |
| -------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| core     | khái niệm business cốt lõi: trạng thái, loại, role, invariant; không chứa http status, không chứa tên bảng    | orderstatus, discounttype, userrole, paymentmethod                             | đây có phải "từ vựng nghiệp vụ"? đổi business là phải đổi theo? |
| data     | db/external: table/schema name, column, connection name, external status code, queue/topic name, provider key | "discounts" (table), "discount_rate" (column), "EmailQueue", externalerrorcode | chỉ liên quan db, external provider, message bus?               |
| services | rule cho use case/workflow: pagesize, limit kỹ thuật, retry, tên job, mã lỗi ở tầng service                   | defaultpagesize, maxretry, "recalculate-discount-job", serviceerrorcode        | thay đổi vì logic xử lý / performance / flow use case?          |
| api      | http/ui: route segment, query param key, header/cookie key, response message key hoặc ui error code           | "api/discounts", "page", "x-correlation-id", "discount.validation.failed"      | chỉ dùng trong controller/filter/middleware/client?             |

- nhiều hướng dẫn .net layered đề xuất: domain/business không chứa chi tiết persistence/ui; hằng số gắn db/http thì đẩy về data/api. [dev](https://dev.to/pouria_ghadiri/layered-architecture-in-aspnet-core-simple-structured-and-still-relevant-part-2-31m3)
- khi enum/const bị dùng chéo (vừa business vừa http/db), tách thành hai khái niệm rõ ràng và map qua services, tránh để core phụ thuộc chi tiết hạ tầng. [developersvoice](https://developersvoice.com/blog/layered-architecture-explained/)

---

## mapping với layered classic trong tài liệu .net

| layered classic (tài liệu) | project hiện tại | ghi chú                                                                                                                                                                                               |
| -------------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| presentation layer         | Api              | controller, http dto, filter, middleware, mapping http ↔ service. [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) |
| business/application layer | Services         | app services, orchestration use case, giao tiếp giữa api và data/core. [dev](https://dev.to/pouria_ghadiri/layered-architecture-in-aspnet-core-simple-structured-and-still-relevant-part-2-31m3)      |
| data access layer          | Data             | dbcontext, repository impl, ef configuration, migration. [red-gate](https://www.red-gate.com/simple-talk/development/dotnet-development/net-application-architecture-the-data-access-layer/)          |
| domain/core layer          | Core             | entities, valueobjects, enums, rules, domain interfaces. [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)          |

- ms docs về "common architectures" cũng mô tả pattern tương tự: presentation → business → data, với domain model riêng ở core. [learn.microsoft](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)
- nhiều article n‑layer .net (aspnetboilerplate, dev.to, stackify) dùng cấu trúc gần hệt: _Web_, _Application/Services_, _EntityFramework/Data_, _Core_. [aspnetboilerplate](https://aspnetboilerplate.com/Pages/Documents/NLayer-Architecture)

---

## ví dụ cấu trúc module "discount"

```
src
├─ Api
│  ├─ Controllers
│  │   └─ DiscountController.cs          # http endpoint
│  ├─ Dto
│  │   └─ DiscountRequestDto.cs          # input từ client
│  └─ Filters / Middleware               # cross-cutting http
├─ Services
│  ├─ Interfaces
│  │   └─ IDiscountService.cs            # contract cho workflow
│  ├─ Services
│  │   └─ DiscountService.cs             # orchestrate rule + repo
│  └─ Dto
│      └─ DiscountDto.cs                 # dto trả về api
├─ Data
│  ├─ Repositories
│  │   └─ DiscountRepository.cs          # impl IDiscountRepository
│  ├─ Context
│  │   └─ ApplicationDbContext.cs
│  └─ Configurations
│      └─ DiscountConfiguration.cs
└─ Core
   ├─ Entities
   │   └─ Discount.cs
   ├─ Enums
   │   └─ DiscountStatus.cs
   ├─ Rules
   │   └─ PercentageRangeRule.cs
   └─ Interfaces
       └─ IDiscountRepository.cs
```

- flow thực thi: api.discountcontroller → services.discountservice → core.idiscountrepository → data.discountrepository → db, phù hợp mẫu n‑tier trong các bài ví dụ. [stackoverflow](https://stackoverflow.com/questions/70658442/asp-net-core-3-layer-architecture-how-to-send-class-from-service-layer-to-api-l)
- thay đổi rule % giảm giá: chỉ sửa core.discount + core.rules, có thể không động đến api/data, giảm rủi ro bug lan. [woodruff](https://www.woodruff.dev/enterprise-patterns-for-asp-net-core-minimal-api-service-layer-pattern-making-http-a-client-not-the-boss/)

---

## rule reference (dán bàn)

```
core  ←  data  ←  services  ←  api

- file dính business rule → core
- file dính db/sql/ef       → data
- file orchestrate nhiều call, xử lý use case → services
- file dính http, routing, status code        → api
```

- đây là biến thể thực tế của layered architecture trong .net: không "sạch" như clean architecture, nhưng đơn giản, dễ onboard và quen thuộc với dev .net lâu năm. [dev](https://dev.to/pouria_ghadiri/layered-architecture-in-aspnet-core-simple-structured-and-still-relevant-part-2-31m3)

## cây dự án skycrm thực tế hiện tại

- mục tiêu: gom lại cây đang rối thành 4 layer rõ "api / services / data / core", nhưng chỉ đổi cách hiểu + guideline, chưa cần refactor folder ngay.

---

### tree chuẩn đề xuất (đủ chi tiết)

```
src
├─ Core                                 # core business layer
│  ├─ Domain                            # domain model chia theo bounded context
│  │   ├─ Advertisements
│  │   ├─ Apps
│  │   ├─ Campaigns
│  │   ├─ Customers
│  │   ├─ Discounts
│  │   │   ├─ Entities
│  │   │   ├─ ValueObjects
│  │   │   ├─ Rules
│  │   │   │   ├─ Policies
│  │   │   │   └─ Validators
│  │   │   └─ Events
│  │   ├─ Orders
│  │   ├─ Promotions
│  │   ├─ Segments
│  │   ├─ Stores
│  │   └─ Vouchers
│  ├─ Enums
│  ├─ Exceptions
│  ├─ Interfaces
│  │   ├─ Repositories
│  │   │   ├─ IDiscountRepository.cs
│  │   │   └─ ICustomerRepository.cs
│  │   └─ Services
│  ├─ Rules                             # rule cross-domain (security, permissions,…)
│  ├─ Caching                           # contract + key pattern cấp domain
│  ├─ Configuration                     # setting thuần nghiệp vụ
│  ├─ Events                            # domain event, integration event contract
│  ├─ Localization                      # resource key nghiệp vụ
│  └─ Helpers/Operator/ComponentModel   # helper không phụ thuộc http/db

├─ Data                                 # data access layer
│  ├─ Context                           # dbcontext, unit of work
│  ├─ Configuration                     # ef/linq2db mapping, convention
│  ├─ DataProviders
│  │   ├─ Interceptors
│  │   └─ LinqToDb
│  ├─ Mapping                           # map db schema ↔ core entity
│  │   ├─ Builders
│  │   │   ├─ Advertisements
│  │   │   ├─ Campaigns
│  │   │   ├─ Customers
│  │   │   ├─ Discounts
│  │   │   └─ ...
│  │   └─ Adapters                      # nếu có kiểu record/db model riêng
│  ├─ Repositories                      # impl cho Core.Interfaces.Repositories
│  │   ├─ Advertisements
│  │   ├─ Customers
│  │   ├─ Discounts
│  │   └─ ...
│  ├─ Migrations
│  │   └─ Installation
│  ├─ Extensions                        # extension cho db, transaction, retry
│  └─ Utilities                         # tiện ích data-only (id generator, type converter)

├─ Services                             # application/service layer
│  ├─ Abstractions
│  │   ├─ IAppService.cs
│  │   └─ IBackgroundJob.cs
│  ├─ Shared                            # hoặc common
│  │   ├─ Result
│  │   ├─ Paging
│  │   └─ Mapping                       # map core entity ↔ service dto/model
│  ├─ Validation
│  │   ├─ Pipeline                      # validation pipeline, behaviors
│  │   └─ Rules                         # rule cấp use case (không phải domain rule)
│  ├─ Discounts
│  │   ├─ Application                   # use cases chính
│  │   ├─ Background                    # job, cron xử lý batch
│  │   ├─ Models
│  │   │   ├─ Commands
│  │   │   ├─ Queries
│  │   │   ├─ Responses
│  │   │   └─ Adapters                  # map external model ↔ service model nếu cần
│  │   ├─ Strategies                    # chọn chiến lược, dùng core entity
│  │   ├─ External
│  │   │   └─ Clients                   # http/grpc client gọi ra ngoài
│  │   ├─ Handlers
│  │   │   └─ Abstractions
│  │   ├─ Factories
│  │   └─ Caching                       # cache logic cho discounts (key, policy)
│  ├─ Customers
│  │   ├─ Application
│  │   ├─ Models
│  │   └─ Caching
│  ├─ Notifications
│  │   └─ Message
│  ├─ RkCRM
│  │   ├─ Caching
│  │   └─ SyncData
│  ├─ Reports
│  ├─ ScheduleTasks
│  └─ Plugins / Firebase / Grpc / Protos

├─ Api                                  # presentation/http layer
│  ├─ Controllers
│  │   ├─ Discounts
│  │   ├─ Customers
│  │   └─ ...
│  ├─ Models                            # http dto (request/response)
│  │   ├─ Discounts
│  │   │   ├─ Dto
│  │   │   └─ Adapters                  # map service dto ↔ api dto
│  │   ├─ Customers
│  │   └─ ...
│  ├─ Mapping                           # config mapper cho http layer (automapper, mapstruct,…)
│  │   └─ Profiles
│  ├─ Facades                           # adapter/facade gọi xuống Services layer
│  │   ├─ Discounts
│  │   │   └─ Handlers                  # handler theo endpoint nếu tách khỏi controller
│  │   └─ ...
│  ├─ Factories                         # factory cho api model, response builder
│  ├─ Filters                           # exception filter, auth filter
│  ├─ Middleware                        # logging, correlation id, versioning
│  └─ Properties
│      └─ PublishProfiles
```

---

### cách dùng tree này để giảm rối

- quy tắc 1: thấy "business rule" → đặt vào core.domain hoặc core.rules, không đặt ở services/api/data. dùng để review code nhanh, chỉ cần nhìn folder.
- quy tắc 2: cái gì đụng trực tiếp db/sql/mapping → data.\*. không để mapper ef trong core/services/api.
- quy tắc 3: orchestrate nhiều repo, call external, transaction, retry → services.\* (application). api chỉ gọi services và map dto.
- quy tắc 4: mọi thứ dính http (controller, binding, status code, route, swagger) → api.\*. không cho nhảy logic xuống data từ api.