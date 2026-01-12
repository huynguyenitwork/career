ok, mình chốt cho bạn **một bản hướng dẫn gọn – đúng – dùng được ngay** cho combo hơi “cổ nhưng bền” này:

**automapper 10.1.1 + c# 7.3 + .net core 2.1 + asp.net web api**

không bay bướm, không magic, đọc là triển được.

---

## 1. bối cảnh kỹ thuật (để khỏi lệch pha)

* .net core 2.1 → **có startup.cs**
* di container: microsoft.extensions.dependencyinjection
* automapper **10.1.1** (ổn định, phổ biến)

---

## 2. cài package đúng bộ

```bash
dotnet add package AutoMapper --version 10.1.1
dotnet add package AutoMapper.Extensions.Microsoft.DependencyInjection --version 7.0.0
```

ghi chú thực chiến:
automapper 10.x **chạy tốt** với extensions 7.x trên net core 2.1.

---

## 3. tạo mapping profile (bắt buộc)

### ví dụ model

```csharp
public class DiscountDto
{
    public int Id { get; set; }
    public string Name { get; set; }
}

public class DiscountResponse
{
    public int Id { get; set; }
    public string Name { get; set; }
}
```

### profile trong thư mục mapping|mappings

```csharp
using AutoMapper;

public class DiscountProfile : Profile
{
    public DiscountProfile()
    {
        CreateMap<DiscountDto, DiscountResponse>();
    }
}
```

nguyên tắc:

* mỗi module / feature → 1 profile
* không nhét hết vào một file

---

## 4. đăng ký automapper trong `startup.cs`

### `startup.cs`

```csharp
using AutoMapper;

public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddAutoMapper(typeof(Startup));
        services.AddMvc();
    }

    public void Configure(IApplicationBuilder app, IHostingEnvironment env)
    {
        app.UseMvc();
    }
}
```

`typeof(Startup)` = scan toàn bộ assembly chứa startup để tìm `Profile`.

---

## 5. kiểm tra mapping fail sớm (rất nên làm)

thêm vào `configure`:

```csharp
public void Configure(
    IApplicationBuilder app,
    IHostingEnvironment env,
    IMapper mapper)
{
    mapper.ConfigurationProvider.AssertConfigurationIsValid();
    app.UseMvc();
}
```

→ mapping sai là **app không chạy**, phát hiện sớm.

---

## 6. dùng automapper trong web api

### controller

```csharp
[ApiController]
[Route("api/discounts")]
public class DiscountController : ControllerBase
{
    private readonly IMapper _mapper;

    public DiscountController(IMapper mapper)
    {
        _mapper = mapper;
    }

    [HttpGet]
    public IActionResult Get()
    {
        var dto = new DiscountDto
        {
            Id = 1,
            Name = "summer sale"
        };

        var response = _mapper.Map<DiscountResponse>(dto);

        return Ok(response);
    }
}
```

---

## 7. dùng trong model extension (đúng như case của bạn)

```csharp
public static class DiscountModelExtensions
{
    public static DiscountResponse ToResponse(
        this DiscountDto dto,
        IMapper mapper)
    {
        return mapper.Map<DiscountResponse>(dto);
    }
}
```

dùng:

```csharp
var response = dto.ToResponse(_mapper);
```

---

## 8. những lỗi hay gặp (để né)

* quên `Profile` → automapper không map
* mapping nằm ở project khác nhưng không scan assembly
* new `MapperConfiguration` trong code business
* dùng static mapper global

---

## 9. 20/80 chốt lại cho nhớ

* profile = luật chuyển dữ liệu
* startup = nơi đăng ký luật
* controller / extension = nơi sử dụng
* domain = **không dính automapper**

automapper là **xe trung chuyển dữ liệu**, không phải người ra quyết định nghiệp vụ.
