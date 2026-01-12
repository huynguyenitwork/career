# SkyCloud REST JSON Service – Tài liệu chuẩn hoá dùng chung

## 1. Bối cảnh & mục tiêu

Hệ SkyCloud sử dụng **RESTful API + JSON** và được bảo vệ bởi **Bearer Token (JWT)**. Mục tiêu tài liệu này là:

-  Chuẩn hoá **cách gọi API REST JSON** trong .NET Core 2.1 (C# 4.3)
-  Dùng **1 service duy nhất** cho CRUD
-  Tách rõ: Auth – Request – Cache – Deserialize

Nguyên tắc 20/80: làm đúng xương sống, phần còn lại chỉ là đổi DTO và endpoint.

---

## 2. Thiết kế Service dùng chung (JSON + REST)

### 2.1. Interface chuẩn

```csharp
public interface ISkyCloudService
{
    Task<T> GetAsync<T>(string url, string bearerToken) where T : class;
    Task<T> PostAsync<T>(string url, object body, string bearerToken) where T : class;
    Task<T> PutAsync<T>(string url, object body, string bearerToken) where T : class;
    Task<bool> DeleteAsync(string url, string bearerToken);
}
```

---

## 3. Generic Executor (xương sống 80%)

### 3.1. Lý do tồn tại

-  Tránh lặp cache logic
-  Dùng chung cho GET/Search
-  Không phụ thuộc domain

### 3.2. Triển khai

```csharp
private async Task<TResponse> ExecuteSkyCloudRequest<TRequest, TResponse>(
    string cacheKey,
    TRequest requestBody,
    Func<Task<TResponse>> apiCall,
    int cacheMinutes = 3.)
    where TResponse : class
{
    // 1. Cache
    var cached = _cacheProvider.GetFromCache<TResponse>(cacheKey);
    if (cached != null)
        return cached;

    // 2. Call API
    var result = await apiCall();

    // 3. Cache
    if (result != null)
    {
        _cacheProvider.SetCache(
            cacheKey,
            result,
            DateTimeOffset.Now.AddMinutes(cacheMinutes));
    }

    return result;
}
```

### 3.3. Vì sao phải `where TResponse : class`

-  Cache chỉ làm việc với **reference type**
-  Tránh lỗi CS042.
-  REST API response luôn là object

---

## 4. Áp dụng CRUD thực tế

### 4.1. GET (có cache)

```csharp
public async Task<Organization> GetOrganizationByName(
    string name,
    string bearerToken)
{
    var cacheKey = $"org:{name}";

    return await ExecuteSkyCloudRequest<object, Organization>(
        cacheKey,
        null,
        async () =>
        {
            var url = $"/api/organizations?name={name}";
            return await _skyCloudService.GetAsync<Organization>(url, bearerToken);
        });
}
```

### 4.2. POST

```csharp
public Task<Organization> CreateOrganization(
    OrganizationCreateDto dto,
    string bearerToken)
{
    return _skyCloudService.PostAsync<Organization>(
        "/api/organizations",
        dto,
        bearerToken);
}
```

### 4.3. PUT

```csharp
public Task<Organization> UpdateOrganization(
    Guid id,
    OrganizationUpdateDto dto,
    string bearerToken)
{
    return _skyCloudService.PutAsync<Organization>(
        $"/api/organizations/{id}",
        dto,
        bearerToken);
}
```

### 4.4. DELETE

```csharp
public Task<bool> DeleteOrganization(
    Guid id,
    string bearerToken)
{
    return _skyCloudService.DeleteAsync(
        $"/api/organizations/{id}",
        bearerToken);
}
```

---

## 5. Checklist cho team

-  Không dùng XML
-  Không nhét logic business vào Service gọi API
-  Token lấy từ Auth Server, không hard-code
-  **GET/Search mới cache**
-  **POST/PUT/DELETE không cache**

---

## 6. Kết luận

Khi đã tách đúng:

-  Auth là Auth
-  REST là REST
-  Cache là Cache

Mọi API mới chỉ còn là đổi endpoint và DTO.
