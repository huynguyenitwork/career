## mục tiêu
- hiểu được yêu cầu nghiệp vụ => yêu cầu kỹ thuật của promotion engine áp dụng cho loại discount open/order
- hiểu được kiến trúc, thiết kế api, db, logic hệ thống, testing và vận hành

## cách dùng tài liệu
- sử dụng vscode với 2 `extension yzhang.markdown-all-in-one`, `shd101wyy.markdown-preview-enhanced` để viết và preview tệp markdown
- xem tuần tự theo chiều dọc trên -> xuống tài liệu này
## user-story

1. [[QSR] [Promotion] Sync promotion from SkyCRM to RK7](https://app.clickup.com/t/9018236177/DC-14291)

> ## Description
>
> - Đồng bộ discount từ ECom về RK7 thông qua Promotion engine trên SkyCRM
> - Mục đích: Promotion quản lý tại 1 nơi là ECOM (Source of truth), master data sẽ được đồng bộ tới các nơi sử dụng (Online order, POS - dine in, ...)
> - Do RK7 chỉ đáp ứng các promotion / discount đơn giản - không quản lý các Promotion phức tạp. Do đó cần xây dựng 1 promotion engine trên SkyCRM để xử lý Validate promotion thay cho RK7
> 
>
> ## Acceptance criteria
>
> - [Transfer Server] Xử lý nhận Promotion từ ECOM về Transfer server (raw data)
> - [SkyCRM] Lưu Promotion về CRM. Promotion được đồng bộ sẽ hiển thị trên danh sách Promotion trên SkyResto
> - [RefAgent] Viết API trên RefAgent để nhận promotion vừa tạo/update và xử lý trước khi lưu promotion vào RefServer
> - [RefAgent] Lưu Promotion vào RK7 theo thông tin: ECOMCODE, Tên promotion, Loại promotion, Ngày bắt đầu, ngày kết thúc và trả về REFCODE và REFID sau khi insert/update thành công
>     - Trả lỗi nếu lưu xuống RK7 không thành công
>     - Trả success nếu lưu xuống RK7 thành công
>     - Cần có cơ chế retry trong trường hợp sync xuống RK7 không thành công
>     
> 
>
> ## Promotion Sheme
>
> Cần đảm bảo các sheme sau được đồng bộ từ ECOM xuống RK7
>
> - Open discount (Giảm giá mở)
> - Giảm giá tổng đơn (% and Amount)
> - Giảm giá item (% and Amount)
> - Mua X tặng Y
> - ...
> - ...
> 

2. [DC-14135 [QSR] [masterdata] Sync Promotions](https://app.clickup.com/t/9018236177/DC-14135)

- [[DEV] Đồng bộ Discount mở từ ECOM](https://app.clickup.com/t/9018236177/DC-14285) [đã hoàn thành]
- [[DEV] Đồng bộ Discount order từ ECOM](https://app.clickup.com/t/9018236177/DC-14464) [đang xử lý]

## tham khảo
### tài liệu nghiệp vụ
[bbd](https://docs.google.com/document/d/1ZW0Zm9dFhJJrK-4ZChvBjkUXSlf5yDzf/edit)

### diagram
#### flow
![[diagram-flow.jpg]]
#### sequence
![[sequence-flow.jpg]]
### tài liệu kỹ thuật
- context hệ thống (business + phạm vi + bdd + link + sơ đồ tổng quan) [[bdd-order-discount]] và [[bdd-open-discount]]
- kiến trúc + module mapping (flow + dependency) [[#diagram]]
- api layer (endpoint + contract + auth) [[bdd-order-discount]] và [[bdd-open-discount]]
- data layer (schema + migration + seed) [[data-layer]]
- logic layer (business rule + edge case + error code) [[bdd-order-discount]] và [[bdd-open-discount]]
- testing (test case + e2e + regression) [[bdd-order-discount]] và [[bdd-open-discount]]
- vận hành (env + run local + deploy + branch) [[van-hanh]]
- tracking (clickup task + trạng thái) [[#user-story]]