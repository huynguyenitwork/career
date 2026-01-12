# luồng test

## store sync

### checklist
- kiểm thử luồng dl ecom-skytransfer


### api
- rk7-api-endpoint: 
	http://localhost:5000/ecom/
	
- {{rk7-api-endpoint}}/store-sync
### method
POST
### payload
{
  code: "[TEST]-LVT",
  name: "[TEST] The Pizza Company Lê Văn Việt - TP.Thủ Đức",
  address: "[TEST] 185 đường Lê Văn Việt, Phường Hiệp Phú, TP Thủ Đức, HCM.",
  eHoaDonName: "[TEST] The Pizza Company Lê Văn Việt - TP.Thủ Đức",
  eHoaDonAddress: "[TEST] The Pizza Company Lê Văn Việt - TP.Thủ Đức",
  tenantId: "0192fda4-ba1b-76ef-bb1a-64c043a8e4a4",
  status: "ACTIVE",
  eventType: "created"
}
### db
#### skytransfer
EcomStore
 

# code

## tổng quan
- hệ thống được xây theo 3 tầng: entity + service → webhook + sync → refactor + log.
- các commit diễn ra liên tục trong 25/11 – 8/12, nghĩa là team đang chạy sprint khá đều.
- giai đoạn đầu xây khung, giữa hoàn thiện logic sync, cuối tối ưu & quan sát.
- commit cuối là log → dấu hiệu chuẩn bị đóng sprint / release
## timeline

### 25 nov 2025 – giai đoạn xử lý webhook & services

- feat: webhook, ecomservices (09:14)
điểm khởi đầu của module: dựng pipeline xử lý webhook + service lõi.

- refactor: update property entity (14:35)
dọn lại entity, cập nhật field theo yêu cầu mới → rõ ràng là đang hoàn thiện mô hình dữ liệu.

- refactor: ecomservices (21:10)
lượt refactor thứ hai → tối ưu logic service sau khi test lần đầu.

### 28 nov 2025 – giai đoạn sync real data & combo

- feat: webhook sync-combo & update product (10:06)
bổ sung xử lý combo, sync sản phẩm → bước chuyển từ “chạy được” sang “chạy với data thật”.

- refactor: entity & startup (10:17)
sau khi sync thực tế, hệ thống cần chỉnh cấu trúc và boot process → rất đúng flow phát triển.

### 2 dec 2025 – gom nhánh, chuẩn hóa

- origin/qsr-ecom (14:54)
đây có thể là nhánh chính hoặc nhánh chung để merge về.
dấu hiệu: ổn định hóa trước khi bổ sung log.

### 8 dec 2025 – giai đoạn quan sát, bổ sung log

- feat: add logs for ecomservices & refactor code (13:16)
khi hệ thống gần như ổn định, team bổ sung log → phục vụ monitor, test & debug.
đây là bước 80% giá trị còn lại: đảm bảo chất lượng trước khi bàn giao/triển khai.