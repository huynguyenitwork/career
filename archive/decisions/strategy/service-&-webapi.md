# tài liệu ngắn gọn về service & cấu hình webapi

## 1. vòng đời service

- singleton: tạo 1 lần khi app khởi chạy, sống đến khi app tắt. dùng cho shared data, config, logger.
- scoped: tạo 1 lần cho mỗi request http, tự hủy sau request. dùng cho xử lý request, truy xuất db.
- transient: tạo mới mỗi lần gọi, tự hủy sau khi xong. dùng cho service ngắn hạn, lightweight.
- hostedservice / backgroundservice: chạy nền, sống cùng app. dùng cho task định kỳ (cache, export data…).

nguyên tắc 20/80: 20% service quan trọng nhất tạo ra 80% tác động, thường là dbcontext, core services, background tasks.

## 2. nhóm service chính trong startup.cs

- dbcontext: kết nối và thao tác database.
- httpcontextaccessor: lấy thông tin request hiện tại.
- repositories: thao tác crud với database.
- services: xử lý business logic, gọi repository.
- hosted services: chạy task nền, ví dụ cacheservices, saledatataskscheduleservices.
- mvc + formatter: hỗ trợ trả json và xml.
- cors + https + hsts: bảo mật, cho phép truy cập đa domain.
- logger: ghi log sự kiện, lỗi (log4net).

## 3. nguyên tắc 20/80

- 20% service tạo ra 80% giá trị: dbcontext, core services, hostedservices.
- repository phụ trợ, formatter, logger: hỗ trợ, không quyết định trực tiếp hoạt động chính.

## 4. luồng request và task nền

- request đến webapi → mvc controller → scoped service → repository → dbcontext → trả kết quả.
- task nền → hostedservice chạy độc lập → service → repository → dbcontext → thực hiện job định kỳ (ví dụ export sales, cache refresh).
