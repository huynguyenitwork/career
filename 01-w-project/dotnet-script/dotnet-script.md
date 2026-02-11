# dotnet-script hướng dẫn

## mục tiêu

- chạy nhanh file c# dạng script
- không cần tạo project
- hỗ trợ nuget package
- dùng để test logic nhỏ

---

## cài đặt

- cài tool global

```bash
dotnet tool install -g dotnet-script
````

* kiểm tra cài thành công

```bash
dotnet script --version
```

---

## ví dụ cơ bản

* tạo file

```
hello.csx
```

* nội dung file

```csharp
Console.WriteLine("hello world from dotnet-script");
```

* chạy script

```bash
dotnet script hello.csx
```

---

## ví dụ import nuget package

* tạo file

```
json-test.csx
```

* nội dung file

```csharp
#r "nuget: Newtonsoft.Json, 13.0.3"

using Newtonsoft.Json;

var obj = new { name = "huy", age = 30 };

Console.WriteLine(JsonConvert.SerializeObject(obj));
```

* chạy script

```bash
dotnet script json-test.csx
```

---

## workflow khuyến nghị

* viết logic thử nghiệm trong `.csx`
* xác nhận output đúng
* copy logic sang project thật
* thêm unit test sau

---

## tối ưu tốc độ

* chạy lại script để reuse cache compile
* hạn chế import nuget không cần thiết
* tách script nhỏ theo mục tiêu test

---

## khi nên dùng

* test thuật toán
* test parse / transform data
* test thư viện mới
* viết automation script nhỏ

---

## khi nên loại

* debug integration
* benchmark performance chuẩn
* phát triển app production

---

## template script chuẩn

```csharp
#r "nuget: Newtonsoft.Json, 13.0.3"

using System;

Console.WriteLine("ready script");
```

---

## lỗi thường gặp

* không nhận lệnh `dotnet script` → kiểm tra global tool path
* nuget restore chậm → kiểm tra mạng
* script chạy chậm lần đầu → compile warmup