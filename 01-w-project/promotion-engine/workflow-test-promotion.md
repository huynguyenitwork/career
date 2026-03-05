# timeline

- [25-02-2026] chạy service remote với psexec
- [25-02-2026] kiểm tra case hoạt động
- [25-02-2026] set up env cho develop
- [09-02-2026] refactor code (skycrm-api n-tier)
- [05-02-2026] run source test
- [02-02-2026] test dữ liệu theo case
- [29-01-2026] test trên server 32
- [28-01-2026] tạo ip-public với refagent
- [28-01-2026] sửa org-id
- [28-01-2026] lưu ý chung
---


# chạy service remote với psexec

## bước 1 xác định session server

```
query session /server:SKYXQASERVER
```

## bước 2 attach vào session đó

- thấy ở local
```
psexec \\SKYXQASERVER cmd
```
## bước 3 chạy app

```
start "" "C:\huynp-dev\shortcut\skytransfer.lnk"
start "" "C:\huynp-dev\shortcut\refagent.lnk"
```
## bước 4 kiểm tra port
```
curl http://SKYXQASERVER:2340
curl http://SKYXQASERVER:2329
```
## bước 5 tắt app
```
netstat -ano | findstr 2340
netstat -ano | findstr 2329
taskkill /f /pid <pid>
```

# kiểm tra

## luồng auto

## skytransfer payload
{
  "name": "auto open discount 20260225144317",
  "code": "op-20260225144317",
  "status": "ACTIVE",
  "description": "auto open discount 20260225144317",
  "startTime": "2026-02-12T10:00:00+0700",
  "endTime": "Tue, 10 Feb 2026 10:00:00 GMT",
  "promotionType": "OPEN_DISCOUNT",
  "tenantId": "0192fda4-ba1b-76ef-bb1a-64c043a8e4a4",
  "eventType": "created",
  "storesSelection": "STORE_PREREQUISITE",
  "entitledStores": [
    "TPC_068_EST_HCM",
    "TPC_053_SVH_HCM"
  ]
}

## luồng manual


---

# set up env cho develop

## 1. thiết lập skytransfer
- tạo db chỉ dành cho môi trường dev trên server 32 (backup restore từ stg)
- cấu hình parameters skycrm dev (kết nối, orgid, discount group auto/manual ban đầu)

## 2. thiếp lập skycrmui
- thiết lập kết nối gián tiếp refagent tới rk7/trực tiếp tới rk7

## 3. thiết lập refagent
- chỉ run

---

# run source test

## discount-group

### auto
- code: 202602-auto
- code: 202602-auto-not-exists
- name: [dev] open discount 2.2026 (auto)
### manual
- code: 202602-manual
- code: 202602-manual-not-exists
- name: [dev] open discount 2.2026 (manual)

## nháp
{
	"name": "[dev] open discount 2.2026",
	"code": 202602,
	"description": null,
	"organizationId": 8547,
	"status": 1,
	"parentId": 0,
	"displayOrder": 0,
	"id": 24
}

{
  "name": "Promotion SkyCloud 20260206092311",
  "code": "PSCL20260206092311",
  "discountGroupId": 83,
  "description": "Nội dung Promotion SkyCloud 20260206092311",
  "organizationId": 8547
}

## dev
- orgid: 8582
- sửa config db skytransfer => localhost
- start skytransfer, masterdata-api, skycrm-api, refagent => quan sát rk7man

## staging
- orgid: 8547
- start skytransfer, refagent trên server 32

---

# test dữ liệu theo case

## pm-dev
| stt | trường hợp | hành động | trạng thái discount_group | trạng thái discount | skycrm quyết định & lưu | rk7 gói tin    | rk7 mong đợi | mục đích                    |
|-----|------------|-----------|---------------------------|---------------------|-------------------------|----------------|--------------|-----------------------------|
| 1   | c1         | create    | not_exist                 | not_exist           | allow_bootstrap         | parent + child | both active  | tạo mới đầy đủ              |
| 2   | c2         | create    | active                    | active              | reject_duplicate        | none           | unchanged    | chống trùng                 |
| 3   | c3         | create    | active                    | soft_deleted        | reject                  | none           | unchanged    | không revive                |
| 4   | c4         | create    | active                    | not_exist           | allow                   | child          | child active | tạo child hợp lệ            |
| 5   | c5         | create    | soft_deleted              | not_exist           | reject                  | none           | unchanged    | chặn tạo dưới parent đã xóa |
| 6   | u1         | update    | not_exist                 | any                 | reject                  | none           | unchanged    | chặn update mồ côi          |
| 7   | u2         | update    | soft_deleted              | active              | reject                  | none           | unchanged    | giữ vòng đời                |
| 8   | u3         | update    | active                    | active              | allow                   | child_updated  | synced       | sync dữ liệu                |
| 9   | u4         | update    | active                    | not_exist           | reject                  | none           | unchanged    | chống create trá hình       |
| 10  | u5         | update    | active                    | soft_deleted        | reject                  | none           | unchanged    | không revive                |
| 11  | d1         | delete    | not_exist                 | any                 | noop_or_reject          | none           | unchanged    | an toàn                     |
| 12  | d2         | delete    | soft_deleted              | active              | noop                    | none           | unchanged    | không xóa dây               |
| 13  | d3         | delete    | active                    | active              | allow_soft_delete       | child_inactive | soft_deleted | xóa mềm chuẩn               |
| 14  | d4         | delete    | active                    | soft_deleted        | noop                    | none           | unchanged    | chống lặp                   |
| 15  | d5         | delete    | active                    | not_exist           | noop_or_reject          | none           | unchanged    | tránh log rác               |

## business-ops
| case | thao tác | trạng thái nhóm giảm giá | trạng thái giảm giá | skycrm xử lý | dữ liệu sang rk7    | kết quả thấy được  | dùng để          |
|------|----------|--------------------------|---------------------|--------------|---------------------|--------------------|------------------|
| c1   | tạo      | chưa tồn tại             | chưa tồn tại        | cho phép     | tạo nhóm + giảm giá | hiển thị đầy đủ    | tạo mới chuẩn    |
| c2   | tạo      | đang dùng                | đang dùng           | từ chối      | không có            | không thay đổi     | tránh trùng      |
| c3   | tạo      | đang dùng                | đã xóa              | từ chối      | không có            | không khôi phục    | tránh nhầm       |
| c4   | tạo      | đang dùng                | chưa tồn tại        | cho phép     | tạo giảm giá        | giảm giá xuất hiện | thêm hợp lệ      |
| c5   | tạo      | đã xóa                   | chưa tồn tại        | từ chối      | không có            | không thay đổi     | giữ dữ liệu sạch |
| u1   | sửa      | không tồn tại            | bất kỳ              | từ chối      | không có            | không đổi          | tránh sửa sai    |
| u2   | sửa      | đã xóa                   | đang dùng           | từ chối      | không có            | không đổi          | giữ vòng đời     |
| u3   | sửa      | đang dùng                | đang dùng           | cho phép     | cập nhật            | thấy thay đổi      | đồng bộ          |
| u4   | sửa      | đang dùng                | không tồn tại       | từ chối      | không có            | không phát sinh    | tránh tạo nhầm   |
| u5   | sửa      | đang dùng                | đã xóa              | từ chối      | không có            | không khôi phục    | giữ vòng đời     |
| d1   | xóa      | không tồn tại            | bất kỳ              | bỏ qua       | không có            | không đổi          | an toàn          |
| d2   | xóa      | đã xóa                   | đang dùng           | bỏ qua       | không có            | giữ nguyên         | tránh xóa dây    |
| d3   | xóa      | đang dùng                | đang dùng           | cho phép     | đánh dấu xóa        | không còn hiệu lực | xóa chuẩn        |
| d4   | xóa      | đang dùng                | đã xóa              | bỏ qua       | không có            | không đổi          | chống lặp        |
| d5   | xóa      | đang dùng                | không tồn tại       | bỏ qua       | không có            | không phát sinh    | tránh rác        |

--- 
# test trên server 32
## build source
skytransfer: 
- D:\dcorp\publish\skytransfer
- \\SKYXQASERVER\huynp-dev\skytransfer
refagent:
- D:\dcorp\publish\skytransfer
- \\SKYXQASERVER\huynp-dev\refagent

## test local
kịch bản local dev
# bắt đầu

## flow
=>skytransfer=>crm=>masterdata (local)
=>refagent=>rk7(server 32)

## cấu hình ban đầu skytransfer
sửa api skycrm server (ví dụ: http://localhost:6001)
sửa lại mã discount group (ví dụ: 666668)
bắt đầu với dữ liệu ngày 10.1
* lưu ý: sửa lại chạy lại skytransfer (lý do cache)
## test

### tạo mới
- case 1: trạng thái discount_group + trạng thái discount (not_exist + not_exist) 
mong đợi: tạo được cả 2 (ok)
- case 2: trạng thái discount_group + trạng thái discount (active + active) 
mong đợi: không tạo báo lỗi. block 1 tại skytransfer (ok) => block 2 sau cùng sửa (cần xóa dữ liệu skytransfer)
- case 3: trạng thái discount_group + trạng thái discount (active + soft_deleted)
mong đợi: không tạo báo lỗi. block 1 tại skytransfer (ok) => block 2 sau cùng sửa (cần xóa dữ liệu skytransfer)
- case 4: trạng thái discount_group + trạng thái discount (active + not_exist)
mong đợi: tạo được discount (ok) <đổi dữ liệu ngày 11.1>
- case 5: trạng thái discount_group + trạng thái discount (soft_deleted + not_exist)
mong đợi: không tạo báo lỗi <đổi dữ liệu ngày 12.1>

### sửa [mở lại discount group skytransfer. ví dụ: 666669]
- case 1: trạng thái discount_group + trạng thái discount (not_exist + any) 
mong đợi: không tạo báo lỗi (ok)
- case 2: trạng thái discount_group + trạng thái discount (soft_deleted + active)
[xóa lại discount group/skycrm. ví dụ: 666668+sửa lại mã discount group/skytransfer 666668 và restart service skytransfer]
mong đợi: không tạo báo lỗi (ok)
- case 3: trạng thái discount_group + trạng thái discount (active + active)
mong đợi: không tạo báo lỗi (ok)


## checklist
- kiểm tra ip-public
- kiểm tra port trống đặt inbound rule
- publish truyền file qua server giao thức smb (port 445)
- url service
- tạo bảng dữ liệu (dùng sql server)
- kiểm tra bind address http trên windows

## vấn đề không truy cập được vào service mặc dù đặt inbound rule
- kiểm tra gọi url từ máy khác test port thuần (tcp có mở không)

``` powershell
test-netconnection 118.69.108.41 -port 6000
```
- kiểm tra dải port có hỗ trợ hay không
``` powershell
6000..7000 | % {
	if (Test-NetConnection <public_ip> -Port $_ -InformationLevel Quiet) {
	  "$_ open"
	}
}
```

``` powershell
1..65535 | % { Test-NetConnection <public_ip> -Port $_ -InformationLevel Quiet }
```

## tạo bảng dữ liệu (dùng sql server)

### skytransfer
```sql
-- ecomsynctaskstatus
create table dbo.EcomSyncTaskStatus (
    SyncTaskId int identity(1,1) not null,
    RetryCount int null constraint DF_EcomSyncTaskStatus_RetryCount default 0,
    LastErrorCode nvarchar(50) null,
    LastErrorMessage nvarchar(500) null,
    CreatedAt datetime null,
    UpdatedAt datetime null,
    CompletedAt datetime null,
    Service nvarchar(50) null,
    constraint PK_EcomSyncTaskStatus primary key clustered (SyncTaskId)
) on [primary];

-- ecompromotion
create table dbo.EcomPromotion (
    Id int identity(1,1) not null,
    Code nvarchar(450) not null,
    Name nvarchar(450) not null,
    Status nvarchar(max) null,
    Description nvarchar(max) null,
    StartTime datetime not null,
    EndTime datetime null,
    LimitByWeekdays bit not null,
    ExcludeSpecialDates bit not null,
    PromotionType nvarchar(max) null,
    StoresSelection nvarchar(max) null,
    EntitledStores nvarchar(max) null,
    ShippingTypeSelection nvarchar(max) null,
    EntitledShippingTypes nvarchar(max) null,
    ApplicableConditionType nvarchar(max) null,
    ApplicableConditionValue decimal(18,0) null,
    ProductsSelection nvarchar(max) null,
    EntitledCollections nvarchar(max) null,
    EntitledCombos nvarchar(max) null,
    EntitledProducts nvarchar(max) null,
    EntitledVariants nvarchar(max) null,
    IsRequiredSpecialProducts bit null,
    ApplicableConditionMinimumNumberOfSpecialProducts decimal(18,0) null,
    ProductsConditionSelection nvarchar(max) null,
    EntitledConditionProducts nvarchar(max) null,
    EntitledConditionVariants nvarchar(max) null,
    EntitledConditionCombos nvarchar(max) null,
    ProductsPromotionSelection nvarchar(max) null,
    EntitledPromotionCollections nvarchar(max) null,
    EntitledPromotionProducts nvarchar(max) null,
    EntitledPromotionVariants nvarchar(max) null,
    ApplicableValueType nvarchar(max) null,
    ApplicableValueValueAmount decimal(18,0) null,
    ApplicableValueValuePercent decimal(18,0) null,
    ApplicableValueValueLimitMaxAmount decimal(18,0) null,
    MaxUsageCount int null,
    IsConfigAppliedTogetherWithSpecialProducts bit null,
    ConfigAppliedTogetherWithSpecialProductsType nvarchar(max) null,
    ConfigAppliedTogetherWithSpecialProductsValueIsCombo bit null,
    ConfigAppliedTogetherWithSpecialProductsValueIsVariant bit null,
    EntitledSpecialVariantIds nvarchar(max) null,
    IsCombinedProductDiscount bit null,
    IsCombinedShipmentDiscount bit null,
    IsCombinedOrderDiscount bit null,
    TenantId nvarchar(max) null,
    EventType nvarchar(max) null,
    Created datetime null,
    Updated datetime null,
    ProcessStatus int null,
    CallbackUrl nvarchar(max) null constraint DF_EcomPromotion_CallbackUrl default null,
    SyncTaskId int null,
    constraint PK_EcomPromotion primary key clustered (Id),
    constraint FK_EcomPromotion_EcomSyncTaskStatus
        foreign key (SyncTaskId)
        references dbo.EcomSyncTaskStatus(SyncTaskId)
        on delete set null
) on [primary] textimage_on [primary];

-- ecompromotionapplicabletime
create table dbo.EcomPromotionApplicableTime (
    Id int identity(1,1) not null,
    PromotionId int not null,
    DayOfWeek int not null,
    StartTime datetime not null,
    EndTime datetime not null,
    constraint PK_EcomPromotionApplicableTime primary key clustered (Id),
    constraint FK_EcomPromotionApplicableTime_Promotion
        foreign key (PromotionId)
        references dbo.EcomPromotion(Id)
) on [primary];

-- ecompromotionexcludeddate
create table dbo.EcomPromotionExcludedDate (
    Id int identity(1,1) not null,
    PromotionId int not null,
    Timezone nvarchar(max) null,
    StartTime datetime not null,
    EndTime datetime not null,
    constraint PK_EcomPromotionExcludedDate primary key clustered (Id),
    constraint FK_EcomPromotionExcludedDate_Promotion
        foreign key (PromotionId)
        references dbo.EcomPromotion(Id)
) on [primary] textimage_on [primary];

-- ecomsynctasktimeline
create table dbo.EcomSyncTaskTimeline (
    Id int identity(1,1) not null,
    SyncTaskId int not null,
    EventCode nvarchar(50) null,
    EventMessage nvarchar(2000) null,
    CreatedAt datetime null,
    ActName nvarchar(100) null constraint DF_EcomSyncTaskTimeline_ActName default null,
    constraint PK_EcomSyncTaskTimeline primary key clustered (Id),
    constraint FK_EcomSyncTaskTimeline_EcomSyncTaskStatus
        foreign key (SyncTaskId)
        references dbo.EcomSyncTaskStatus(SyncTaskId)
        on delete cascade
) on [primary];

insert into "Parameters" ("name", "status", "parentId", "description", "paramName", "intVal", "strVal") values (N'Sky CRM Api Server', 4, 0, NULL, N'SkyCRMApiServer', 0, N'https://api-stg.dcorp.com.vn/crm');
insert into "Parameters" ("name", "status", "parentId", "description", "paramName", "intVal", "strVal") values (N'Sky CRM Api Port', 4, 0, NULL, N'SkyCRMApiPort', NULL, NULL);
insert into "Parameters" ("name", "status", "parentId", "description", "paramName", "intVal", "strVal") values (N'Sky CRM Api Suffix Api Name', 4, 0, NULL, N'SkyCRMApiSuffixApiName', NULL, N'');
insert into "Parameters" ("name", "status", "parentId", "description", "paramName", "intVal", "strVal") values (N'Sky CRM Api Discount Group Name', 4, 0, NULL, N'SkyCRMApiDiscountGroupName', NULL, N'[dev] open discount');
insert into "Parameters" ("name", "status", "parentId", "description", "paramName", "intVal", "strVal") values (N'Sky CRM Api Discount Group Code', 4, 0, NULL, N'SkyCRMApiDiscountGroupCode', 666666, NULL);
insert into "Parameters" ("name", "status", "parentId", "description", "paramName", "intVal", "strVal") values (N'Master Data Organization Id', 4, 0, NULL, N'MasterDataOrganizationId', 8547, NULL);

-- store procedure
create procedure [dbo].[SP_EcomPromotion_OpenDiscount_SkyCRM]
as
begin
    set NOCOUNT on;

    select *
    from EcomPromotion
    where ProcessStatus = 0
      and PromotionType = 'OPEN_DISCOUNT'
    order by Id ASC;
end

```
## url service

### stg/dev
skytransfer: http://118.69.108.41:2340
refagent: http://118.69.108.41:2329
skycrm: 
	https://api-stg.dcorp.com.vn/crm
	https://api-dev.dcorp.com.vn/crm
rk7: https://118.69.108.41:2323
### local
skytransfer: http://localhost:2340
refagent: http://localhost:2329
skycrm: http://localhost:6001
rk7: https://118.69.108.41:2323


## publish truyền file qua server giao thức smb (port 445)
- bước 1: server → chọn folder → properties → sharing → advanced sharing → bật share
- bước 2: server → set share permission + ntfs permission → có write/modify
- bước 3: server → windows firewall → inbound rule → allow tcp 445 (local subnet)
- bước 4: client → file explorer → nhập `\\ip_server\share_name`
- bước 5: client → copy file vào thư mục share

skytransfer share path: \\SKYXQASERVER\huynp-dev\skytransfer
refagent share path: \\SKYXQASERVER\huynp-dev\refagent

## kiểm tra port trống
``` bat
netstat -ano | findstr :5000
netstat -ano | findstr :5901
```
**dùng cổng**
skytransfer: 2340
refagent: 2329

## kiểm tra ip-public
``` powershell
Invoke-RestMethod -Uri "https://api.ipify.org"
```
fallback
``` powershell
Invoke-RestMethod -Uri "https://ifconfig.me/ip
```
- ip-public: 118.69.108.41


# tạo ip-public với refagent
``` bat
./cloudflared.exe tunnel --url http://localhost:5901
```
# sửa org-id
- cập nhật bằng api parameters key là **MasterDataOrganizationId**, cache là 120' trong cacheservice(get-all-parameters)

# lưu ý chung
- cache lưu theo từng process/service và trên ram không có cách can thiệp bên ngoài trừ api