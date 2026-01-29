# ide & extension
- vscode favorites path: d:\dcorp\skytransfer\.favorites.json
- visual studio favorites path: d:\dcorp\skytransfer\skytransfer.favdoc.user

# language & coding constraints
- c# max version 7.3 → không dùng null-check hiện đại
- ưu tiên code chạy đúng, không lỗi → tối ưu sau
- hệ thống phục vụ thị trường việt nam
- hiểu tới đâu triển khai tới đó, không chờ đủ tài liệu
- hỏi đúng người, đúng vai trò để tránh nhiễu

# data & schema rules
- bảng promotion chính tạo trước
- các field created, updated xử lý sau
- tiếp cận database-first:
  - không migration
  - không seed mẫu
  - bảng tạo tay
  - dữ liệu test = dữ liệu thật từ ecom
  - input lấy đúng hệ thống → map → process

# dotnet / ef core
- update database:
  - dotnet ef database update --project appserver.csproj --verbose
- cài / gỡ ef tool:
  - dotnet tool install --global dotnet-ef --version 2.1.0
  - dotnet tool uninstall --global dotnet-ef --version 2.1.0
- scaffold model từ database:
  - dùng ef scaffold
  - không migration
  - sinh entity + dbcontext
  - dùng data-annotations
  - chọn đúng bảng cần thao tác