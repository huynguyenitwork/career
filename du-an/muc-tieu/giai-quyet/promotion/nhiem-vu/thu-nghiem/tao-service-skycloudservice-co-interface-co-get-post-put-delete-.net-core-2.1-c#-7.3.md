## 1. Interface – hợp đồng dùng chung

```csharp
using System.Threading.Tasks;

namespace SkyCloud.Infrastructure
{
    public interface ISkyCloudServices
    {
        Task<T> GetAsync<T>(string url, string bearerToken);
        Task<T> PostAsync<T>(string url, object body, string bearerToken);
        Task<T> PutAsync<T>(string url, object body, string bearerToken);
        Task<bool> DeleteAsync(string url, string bearerToken);
    }
}
```

---

## 2. Implementation – SkyCloudServices (đủ CRUD)

```csharp
using Newtonsoft.Json;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace SkyCloud.Infrastructure
{
    public class SkyCloudServices : ISkyCloudServices
    {
        private readonly HttpClient _httpClient;

        public SkyCloudServices(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<T> GetAsync<T>(string url, string bearerToken)
        {
            var request = CreateRequest(HttpMethod.Get, url, bearerToken);
            return await SendAsync<T>(request);
        }

        public async Task<T> PostAsync<T>(string url, object body, string bearerToken)
        {
            var request = CreateRequest(HttpMethod.Post, url, bearerToken, body);
            return await SendAsync<T>(request);
        }

        public async Task<T> PutAsync<T>(string url, object body, string bearerToken)
        {
            var request = CreateRequest(HttpMethod.Put, url, bearerToken, body);
            return await SendAsync<T>(request);
        }

        public async Task<bool> DeleteAsync(string url, string bearerToken)
        {
            var request = CreateRequest(HttpMethod.Delete, url, bearerToken);
            var response = await _httpClient.SendAsync(request);
            return response.IsSuccessStatusCode;
        }

        // ===== Helper methods =====

        private HttpRequestMessage CreateRequest(
            HttpMethod method,
            string url,
            string bearerToken,
            object body = null)
        {
            var request = new HttpRequestMessage(method, url);
            request.Headers.Authorization =
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", bearerToken);

            if (body != null)
            {
                request.Content = new StringContent(
                    JsonConvert.SerializeObject(body),
                    Encoding.UTF8,
                    "application/json");
            }

            return request;
        }

        private async Task<T> SendAsync<T>(HttpRequestMessage request)
        {
            var response = await _httpClient.SendAsync(request);
            response.EnsureSuccessStatusCode();

            var json = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<T>(json);
        }
    }
}
```

---

## 3. Đăng ký DI (Startup.cs)

```csharp
services.AddHttpClient<ISkyCloudServices, SkyCloudServices>();
```

---

## 4. Cách dùng thực tế

```csharp
var token = accessToken;

// GET
var list = await _skyCloudServices
    .GetAsync<List<DiscountGroupDto>>(url, token);

// POST
await _skyCloudServices
    .PostAsync<DiscountGroupDto>(url, model, token);

// PUT
await _skyCloudServices
    .PutAsync<DiscountGroupDto>(url, model, token);

// DELETE
await _skyCloudServices
    .DeleteAsync($"{url}/{id}", token);
```

---

## 5. Vì sao thiết kế này là “đúng mức”?

* Có **interface** → test, mock, thay implementation dễ
* Có đủ **REST verbs**
* Không lẫn auth logic
* Không over-engineer
* Đúng tinh thần **service dùng chung**

Bạn có thể xem `SkyCloudServices` là:

> “cổng ra ngoài hệ thống SkyCloud”

---

### Tổng kết
* 1 interface rõ ràng
* 1 implementation gọn
* đủ CRUD
* đúng runtime (.NET Core 2.1 / C# 7.3)
* gắn Bearer token chuẩn OAuth2

Từ đây, chỉ việc **viết service nghiệp vụ bọc ngoài** (nếu cần), còn lõi gọi API thì **không đụng lại nữa**.
