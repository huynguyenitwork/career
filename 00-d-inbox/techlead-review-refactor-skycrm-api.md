# flow sau refactor (chuẩn production)

```
controller
   ↓
command handler
   ↓
validation pipeline
   ↓
domain service (create/update/delete)
   ↓
integration resolver
   ↓
integration handler (rk7 | refagent | future)
   ↓
tracking + log
```

điểm quan trọng:
**integration decision không nằm trong service business nữa.**

---

# flow cũ (vấn đề thật sự nằm ở đây)

thường code hiện tại sẽ kiểu:

```
controller
   ↓
service
   ↓
validate
   ↓
business logic
   ↓
check useRefAgent
        ↓
     if else
        ↓
   call rk7 / refagent
```

vấn đề:

- service vừa làm **domain + infra**
- if/else sẽ lan ra nhiều method
- test integration khó
- sau này thêm source mới (POS khác) là nổ.

---

# flow mới (tách trách nhiệm)

## step 1 — command handler

chỗ này điều phối toàn bộ.

```csharp
public class PromotionCommandHandler
{
    private readonly PromotionValidationPipeline _validation;
    private readonly DiscountDomainService _domainService;
    private readonly IntegrationResolver _integrationResolver;

    public async Task Handle<T>(SkyCrmDiscountIntegrationCommand<T> cmd)
        where T : SkyCrmDiscountReqBase
    {
        var validation = await _validation.Execute(cmd);

        if (!validation.Success)
            return;

        var context = validation.Context;

        await _domainService.Execute(cmd, context);

        var handler = await _integrationResolver.Resolve(cmd.OrganizationId);

        await handler.Execute(
            context.Mapper,
            cmd.OrganizationId,
            context.TrackLog,
            cmd.Action
        );
    }
}
```

điểm khác biệt lớn:

- pipeline trả về context luôn
- domain không biết integration
- integration không biết domain

tách sạch.

---

# integration resolver (đây mới là phần nên làm chuẩn)

thay vì:

```
IsUseRefAgent
if else
```

ta resolve **runtime strategy**

```csharp
public class IntegrationResolver
{
    private readonly IRefAgentApiClient _refAgentClient;
    private readonly RefAgentIntegrationHandler _refAgent;
    private readonly Rk7IntegrationHandler _rk7;

    public async Task<IDiscountIntegrationHandler> Resolve(int orgId)
    {
        var server = await _refAgentClient.GetRefAgentServer(orgId, false);

        if (server?.UseRefAgent == true)
            return _refAgent;

        return _rk7;
    }
}
```

sau này thêm POS mới:

```
Micros
Simphony
KiotViet
SAP
```

chỉ sửa resolver.

không đụng domain.

---

# domain service (giữ logic hiện tại của a)

```csharp
public class DiscountDomainService
{
    public async Task Execute<T>(
        SkyCrmDiscountIntegrationCommand<T> cmd,
        SkyCrmDiscountValid context)
        where T : SkyCrmDiscountReqBase
    {
        switch (cmd.Action)
        {
            case "create":
                await Create(cmd, context);
                break;

            case "update":
                await Update(cmd, context);
                break;

            case "delete":
                await Delete(cmd, context);
                break;
        }
    }
}
```

điểm quan trọng:

domain service **không gọi rk7 nữa**.

---

# kiến trúc dependency sau refactor

```
Controller
   ↓
CommandHandler
   ↓
Pipeline
   ↓
Domain
   ↓
IntegrationResolver
   ↓
IntegrationHandler
```

dependency graph sạch:

```
domain -> 0 infra dependency
integration -> infra only
```

đây là kiến trúc chuẩn clean architecture.

---

# chỗ refactor đáng làm thêm (techlead level)

## 1 bỏ string action

rất nên sửa:

```csharp
enum PromotionAction
{
    Create,
    Update,
    Delete
}
```

---

## 2 context object nên giữ tất cả state

hiện tại context của a chưa đủ.

nên thành:

```csharp
public class PromotionExecutionContext
{
    public SkyCrmDiscountValid Validation { get; set; }

    public ShareDiscountIntegrationMapper Mapper { get; set; }

    public EcomTrackSyncItem TrackLog { get; set; }

    public Discount Discount { get; set; }
}
```

pipeline + domain share chung context.

---

## 3 pipeline nên support parallel load

step này của a đang đúng hướng rồi.

có thể mở rộng:

```csharp
await Task.WhenAll(
    LoadDiscount(),
    LoadGroup(),
    LoadOrg()
);
```

---

# payoff thực tế sau refactor

impact thật sự:

| tiêu chí             | trước             | sau             |
| -------------------- | ----------------- | --------------- |
| thêm integration mới | sửa nhiều service | thêm handler    |
| test unit            | khó               | test từng layer |
| đọc code             | khó               | flow rõ         |
| risk bug             | cao               | thấp            |
| scaling team         | khó               | dễ              |

---

# đánh giá nhanh code a đang viết

thực ra a đang đi đúng hướng rồi, nhưng còn 3 điểm chưa "techlead level":

1. factory vẫn bị inject concrete handler
2. domain service vẫn hơi dính infra
3. action vẫn là string

fix 3 cái này là code lên level production thật sự.

---

# nếu refactor sâu thêm một bước (best version)

kiến trúc sẽ thành:

```
command
handler
pipeline
domain
event
integration subscriber
```

tức là:

```
domain emit event
integration subscribe
```

đây là pattern **domain event driven integration**.

system lớn thường dùng cách này.

---

# nhận xét thẳng

refactor này đáng làm vì:

- code hiện tại của a đang bắt đầu **scale**
- integration branching sẽ tăng nhanh
- nếu không tách bây giờ sau này sửa rất đau.

nếu muốn, mình có thể:

- vẽ luôn **architecture diagram chuẩn production**
- chỉ ra chính xác chỗ trong code hiện tại của a nên cắt ra trước (ít risk nhất).