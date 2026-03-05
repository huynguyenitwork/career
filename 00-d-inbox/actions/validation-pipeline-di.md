# validation pipeline + di

## loại 1: gom step thủ công (manual pipeline composition)

**dùng khi cần kiểm soát pipeline rõ ràng**

đăng ký step:

```csharp
services.AddScoped<RequestValidationStep>();
services.AddScoped<BusinessRuleStep>();
```

build pipeline:

```csharp
services.AddScoped(sp =>
{
    return new ValidationPipeline(new IPipelineStep<DiscountValidationContext>[]
    {
        sp.GetRequiredService<RequestValidationStep>(),
        sp.GetRequiredService<BusinessRuleStep>(),
    });
});
```

cơ chế:

- di chỉ **lưu object**
- pipeline **tự chọn step**
- thứ tự nằm ở:

```csharp
new IPipelineStep[]
```

kết luận:

- import step =

```csharp
sp.GetRequiredService<Step>()
```

---

## loại 2: di gom step tự động (auto pipeline composition)

**dùng khi pipeline cố định**

đăng ký step:

```csharp
services.AddScoped<IPipelineStep<DiscountValidationContext>, RequestValidationStep>();
services.AddScoped<IPipelineStep<DiscountValidationContext>, BusinessRuleStep>();
```

pipeline:

```csharp
services.AddScoped<ValidationPipeline>();
```

constructor:

```csharp
public ValidationPipeline(IEnumerable<IPipelineStep<DiscountValidationContext>> steps)
{
    _steps = steps;
}
```

cơ chế:

- di tự gom tất cả step
- inject vào pipeline
- thứ tự = thứ tự register

kết luận:

- import step =

```csharp
services.AddScoped<IPipelineStep<...>, Step>()
```

---

## bảng so sánh

| tiêu chí                            | tự gom step          | di tự gom step             |
| ----------------------------------- | -------------------- | -------------------------- |
| nơi quyết định step                 | pipeline factory     | di container               |
| nơi import step                     | `GetRequiredService` | `AddScoped<IPipelineStep>` |
| kiểm soát thứ tự                    | rõ ràng              | theo thứ tự register       |
| thêm step mới                       | phải sửa pipeline    | chỉ cần register           |
| pipeline động (config/feature flag) | tốt                  | kém                        |
| độ sạch code                        | trung bình           | tốt                        |

---

## rule chọn nhanh

- cần kiểm soát step / pipeline thay đổi → dùng **tự gom**
- pipeline cố định / nhiều step → dùng **di tự gom**

---

## lỗi phổ biến

- đăng ký step nhưng pipeline không inject `IEnumerable`
- pipeline tự gom nhưng step chưa đăng ký trong di
- thứ tự register sai → validation chạy sai thứ tự
