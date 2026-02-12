Mục tiêu cuối cùng:

```
solution
 ├ proto
 │   └ greet.proto
 ├ server
 └ client
```

Đi từng bước, build được chạy được luôn.

---

# 1. tạo solution root

## tạo folder + solution

```bash
mkdir GrpcSolution
cd GrpcSolution

dotnet new sln -n GrpcSolution
```

---

# 2. tạo proto project (chỉ chứa contract)

## tạo folder

```bash
mkdir proto
cd proto
```

## tạo proto file

Tạo file:

```
proto/greet.proto
```

```proto
syntax = "proto3";

option csharp_namespace = "GrpcDemo";

package greet;

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply);
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

👉 folder proto KHÔNG phải project .NET
👉 chỉ là contract share

---

# 3. tạo grpc server

## tạo project server

Quay lại root solution:

```bash
cd ..

dotnet new grpc -n server
```

## add vào solution

```bash
dotnet sln add server/server.csproj
```

---

## 3.1 copy proto vào server

Tạo folder:

```
server/Protos
```

Copy:

```
proto/greet.proto → server/Protos/greet.proto
```

---

## 3.2 sửa server.csproj

Mở `server/server.csproj`

Tìm đoạn protobuf → sửa thành:

```xml
<ItemGroup>
  <Protobuf Include="Protos\greet.proto" GrpcServices="Server" />
</ItemGroup>
```

---

## 3.3 implement service

Tạo file:

```
server/Services/GreeterService.cs
```

```csharp
using Grpc.Core;
using GrpcDemo;

namespace server.Services;

public class GreeterService : Greeter.GreeterBase
{
    public override async Task<HelloReply> SayHello(
        HelloRequest request,
        ServerCallContext context)
    {
        await Task.Delay(100);

        return new HelloReply
        {
            Message = $"Hello {request.Name}"
        };
    }
}
```

---

## 3.4 đăng ký service

Mở `server/Program.cs`

```csharp
using server.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddGrpc();

var app = builder.Build();

app.MapGrpcService<GreeterService>();

app.Run();
```

---

# 4. tạo grpc client

## tạo console client

```bash
dotnet new console -n client
```

## add vào solution

```bash
dotnet sln add client/client.csproj
```

---

## 4.1 thêm package client cần

```bash
dotnet add client package Grpc.Net.Client
dotnet add client package Google.Protobuf
dotnet add client package Grpc.Tools
```

---

## 4.2 copy proto sang client

Tạo folder:

```
client/Protos
```

Copy:

```
proto/greet.proto → client/Protos/greet.proto
```

---

## 4.3 sửa client.csproj

```xml
<ItemGroup>
  <Protobuf Include="Protos\greet.proto" GrpcServices="Client" />
</ItemGroup>
```

---

## 4.4 code client

Mở `client/Program.cs`

```csharp
using Grpc.Net.Client;

var channel = GrpcChannel.ForAddress("https://localhost:5110");

var client = new Greeter.GreeterClient(channel);

var reply = await client.SayHelloAsync(
    new HelloRequest { Name = "Huy" });

Console.WriteLine(reply.Message);
```

---

# 5. kiểm tra port server

Mở:

```
server/Properties/launchSettings.json
```

Tìm:

```
applicationUrl
```

Ví dụ:

```
https://localhost:5110
```

👉 client phải dùng đúng port này

---

# 6. build toàn bộ solution

```bash
dotnet build
```

---

# 7. chạy demo

## chạy server

```bash
dotnet run --project server
```

---

## chạy client

Mở terminal khác:

```bash
dotnet run --project client
```

---

# 8. execution flow thực tế

```
client
 -> protobuf serialize
 -> http/2 call
 -> server nhận request
 -> service xử lý async
 -> protobuf response
 -> client nhận object
```

---

# 9. best practice production (rất nên biết sớm)

## proto là single source of truth

KHÔNG để client/server tự copy tay. Thực tế sẽ:

* publish proto thành nuget
* hoặc git submodule
* hoặc contract repo riêng

---

## channel phải reuse

Sai lầm phổ biến:

```
new channel mỗi request ❌
```

Đúng:

```
singleton channel ✔
```

---

## tách domain service khỏi grpc service

Production thường:

```
GrpcService
   -> gọi ApplicationService
        -> gọi Domain logic
```

grpc chỉ là transport adapter.

---

# 10. cấu trúc cuối cùng

```
GrpcSolution
 ├ proto
 │   └ greet.proto
 ├ server
 │   ├ Protos
 │   ├ Services
 │   └ Program.cs
 ├ client
 │   ├ Protos
 │   └ Program.cs
 └ GrpcSolution.sln
```

---

Nếu đào sâu thêm một chút góc nhìn hệ thống:
Thiết kế này tạo ra **knowledge firewall** — server và client buộc phải đồng ý về contract trước khi nói chuyện. Nó làm giảm class bug cực kỳ khó truy vết: version drift giữa services, thứ thường phá nát microservice khi team scale lớn.

Nếu bạn muốn, tôi có thể dựng tiếp level thực chiến hơn như:

* streaming grpc (server stream / bi-directional stream)
* interceptor logging / tracing
* versioning proto không phá backward compatibility
* grpc + dependency injection + typed client
* grpc benchmark vs rest minimal api
* grpc retry + resilience policy

Chỉ cần nói hướng bạn muốn đào sâu.
