# workflow tổng quan grpc

## mục tiêu
- định nghĩa contract giao tiếp giữa client và server
- generate code tự động từ contract
- implement logic xử lý request
- expose grpc endpoint
- test endpoint xác nhận hoạt động

---

## workflow

- tạo project grpc server
- tạo và chuẩn hóa `.proto` làm contract
- cấu hình build để generate code grpc
- build project để sinh skeleton client/server
- implement logic bằng cách kế thừa base class sinh ra
- đăng ký service vào pipeline grpc
- chạy server grpc
- test rpc method bằng tool grpc

---

## bước thực hiện

### 1. chuẩn bị môi trường

- cài `.net sdk` có hỗ trợ grpc
- cài visual studio + workload `"asp.net and web development"`
- cài tool test `grpcurl` hoặc `grpcui`
- chạy `dotnet --version` để xác nhận sdk hoạt động

---

### 2. tạo project grpc server

- mở visual studio → `new project`
- chọn template `"grpc service"`
- tạo solution và project
- chạy `f5` xác nhận project mặc định chạy được

---

### 3. tạo proto contract (nguồn sự thật)

- right click project → `add → protocol buffers file`
- khai báo `syntax = "proto3"`
- khai báo `option csharp_namespace`
- định nghĩa `service`
- định nghĩa `rpc method`
- định nghĩa `message input/output`
- review proto vì mọi thay đổi api phải bắt đầu từ đây

---

### 4. cấu hình generate code từ proto

- mở properties file `.proto`
- đặt `build action = protobuf compiler`
- đặt `grpc stub class = server only`
- mở `.csproj`
- verify tồn tại `<Protobuf Include="..." GrpcServices="Server" />`

---

### 5. build để sinh grpc skeleton

- build solution
- mở `obj/Debug/net*/Protos`
- verify tồn tại file generate `.cs`
- verify tồn tại `[service]Base`
- nếu thiếu base class → dừng workflow và sửa cấu hình proto

---

### 6. implement server logic

- tạo class service kế thừa `[service].[service]Base`
- override đúng tên method khai báo trong `rpc`
- viết logic xử lý request
- trả response đúng schema proto

---

### 7. đăng ký service vào grpc pipeline

- mở `program.cs`
- thêm `app.MapGrpcService<[service]Service>();`
- verify service được inject vào pipeline

---

### 8. chạy grpc server

- chạy `f5` hoặc `dotnet run`
- ghi lại port grpc server
- verify server đang listen endpoint

---

### 9. bật reflection phục vụ test

- cài package `grpc.aspnetcore.server.reflection`
- thêm `builder.Services.AddGrpcReflection();`
- thêm `app.MapGrpcReflectionService();`
- rebuild project

---

### 10. test grpc endpoint

- chạy `grpcurl` để list service
- gọi rpc method bằng json input
- hoặc chạy `grpcui` để test gui
- verify response trả về đúng schema

---

### 11. verify hệ thống hoạt động

- grpc tool hiển thị service và method
- rpc gọi thành công
- response deserialize đúng model
- không có lỗi mapping hoặc serialization

---

## checklist loại lỗi nhanh
- không thấy base class → proto chưa generate code
- override lỗi → tên rpc không khớp proto
- grpc tool không thấy service → reflection chưa bật
- client gọi fail → sai port hoặc protocol http/https

---

## rule vận hành

- `.proto` là nguồn sự thật duy nhất
- không viết tay interface grpc
- mọi thay đổi api phải sửa từ `.proto`
- build thành công mới implement logic
- test rpc là bước xác nhận cuối cùng

---

## output kỳ vọng

- base class generate đầy đủ
- service implement đầy đủ rpc
- grpc endpoint hoạt động ổn định
- grpc tool test thành công
