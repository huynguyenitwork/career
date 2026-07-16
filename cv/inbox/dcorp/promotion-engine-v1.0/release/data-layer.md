## mục tiêu
- tạo schema + migration + seed
- tạo trường/bảng trên môi trường `staging` của `skycrm` (trên môi trường dev đã có)
- tạo bảng trên `skytransfer` (đã thêm trên server 32)
## skycrm
- bổ sung thêm `bảng/trường` trên môi trường `staging`
### 1. schema
* tạo lại bảng `"DiscountTypes"` → chuẩn hóa loại discount thêm trươnờ `Key` dùng mapping logic
* thêm `"ApplicableProduct"` vào `"Discounts"` → xác định phạm vi áp dụng
* tạo bảng `"DiscountInclusionCategories"` → mapping discount ↔ category
* tạo bảng `"DiscountInclusionDishes"` → mapping discount ↔ product/menu item
* thêm `"ApplicableConditionTypeId"` + `"ApplicableConditionValue"` → lưu điều kiện áp dụng
* tạo bảng `"ApplicableConditionTypes"` → chuẩn hóa loại điều kiện
* thêm `"IsCombinedProductDiscount"` + `"IsCombinedOrderDiscount"` → cấu hình áp dụng đồng thời
* thêm nhóm field special product `IsConfigAppliedTogetherWithSpecialProducts`, `DiscountSpecialProductTypeConfig`, `ConfigAppliedTogetherWithSpecialProductsValueIsCombo` và `ConfigAppliedTogetherWithSpecialProductsValueIsVariant` → kiểm soát tương tác với combo/variant
### 2. migration
#### 2.1 discount types
```sql
DROP TABLE IF EXISTS "DiscountTypes";
CREATE TABLE "DiscountTypes" (
	"Id" SERIAL PRIMARY KEY,
	"Name" CITEXT NOT NULL,
	"Key" CITEXT NOT NULL,
	"Status" INTEGER NOT NULL
);
```
#### 2.2 applicable product scope
```sql
ALTER TABLE "Discounts"
ADD COLUMN "ApplicableProduct" int4 NULL
CHECK ("ApplicableProduct" IN (0,1,2,3,4));
COMMENT ON COLUMN "Discounts"."ApplicableProduct"
IS '0=all, 1=category, 2=product, 3=combo, 4=variant';
```
#### 2.3 inclusion mapping
```sql
CREATE TABLE "DiscountInclusionCategories" (
	"Id" serial4 PRIMARY KEY,
	"DiscountId" int4 NOT NULL,
	"CategoryId" int4 NOT NULL,
	CONSTRAINT "FK_DiscountInclusionCategories_DiscountId"
		FOREIGN KEY ("DiscountId") REFERENCES "Discounts"("Id") ON DELETE CASCADE
);
CREATE INDEX "IX_DiscountInclusionCategories_DiscountId"
ON "DiscountInclusionCategories" ("DiscountId");
CREATE TABLE "DiscountInclusionDishes" (
	"Id" serial4 PRIMARY KEY,
	"DiscountId" int4 NOT NULL,
	"MenuItemId" int4 NOT NULL,
	CONSTRAINT "FK_DiscountInclusionDishes_DiscountId"
		FOREIGN KEY ("DiscountId") REFERENCES "Discounts"("Id") ON DELETE CASCADE
);
CREATE INDEX "IX_DiscountInclusionDishes_DiscountId"
ON "DiscountInclusionDishes" ("DiscountId");
```
#### 2.4 applicable condition
```sql
ALTER TABLE "Discounts"
ADD "ApplicableConditionTypeId" int4 NULL;
ALTER TABLE "Discounts"
ADD "ApplicableConditionValue" int4 NULL;
CREATE TABLE "ApplicableConditionTypes" (
	"Id" SERIAL PRIMARY KEY,
	"Key" CITEXT NOT NULL,
	"Name" CITEXT NOT NULL,
	"Status" INTEGER NOT NULL
);
```
#### 2.5 combined discount flags
```sql
ALTER TABLE "Discounts"
ADD "IsCombinedProductDiscount" bool NULL;
ALTER TABLE "Discounts"
ADD "IsCombinedOrderDiscount" bool NULL;
```
#### 2.6 special product config
```sql
ALTER TABLE "Discounts"
ADD "IsConfigAppliedTogetherWithSpecialProducts" bool NULL;
ALTER TABLE "Discounts"
ADD COLUMN "DiscountSpecialProductTypeConfig" int4 NULL
CHECK ("DiscountSpecialProductTypeConfig" IN (1,2));
COMMENT ON COLUMN "Discounts"."DiscountSpecialProductTypeConfig"
IS '1=exclude, 2=not_apply_with';
ALTER TABLE "Discounts"
ADD "ConfigAppliedTogetherWithSpecialProductsValueIsCombo" bool NULL;
ALTER TABLE "Discounts"
ADD "ConfigAppliedTogetherWithSpecialProductsValueIsVariant" bool NULL;
```
### 3. seed
#### 3.1 discount types
```sql
INSERT INTO "DiscountTypes" ("Id", "Name", "Key", "Status") VALUES
(1, 'Giảm giá order', 'ORDER_DISCOUNT', 3),
(2, 'Giảm giá món ăn', 'PRODUCT_DISCOUNT', 3),
(3, 'Đồng giá', 'FIXED_PRICE', 3),
(4, 'Mua 1 tặng 1', 'BUY_1_GET_1_DISCOUNT', 3),
(5, 'Mua X tặng Y', 'BUY_X_GET_Y_DISCOUNT', 3),
(6, 'MUA 2 tặng 1', 'BUY_2_GET_1_DISCOUNT', 0),
(7, 'Giảm giá mở', 'OPEN_DISCOUNT', 3);
```
#### 3.2 applicable condition types
```sql
INSERT INTO "ApplicableConditionTypes" ("Id", "Key", "Name", "Status") VALUES
(1, 'NO_APPLICABLE', 'Không có', 3),
(2, 'QUANTITY_ORDER', 'Số lượng sản phẩm tối thiểu', 3),
(3, 'AMOUNT_ORDER', 'Giá trị đơn hàng tối thiểu', 3),
(4, 'AMOUNT_ORDER_ITEM', 'Giá trị sản phẩm tối thiểu', 3);
```


## skytransfer
### 1. schema
* `"EcomSyncTaskStatus"` → tracking trạng thái sync (error + lifecycle)
* `"EcomPromotion"` → aggregate chính (toàn bộ config promotion)
* `"EcomPromotionApplicableTime"` → rule theo weekday + time range
* `"EcomPromotionExcludedDate"` → blacklist theo date range
* `"EcomSyncTaskTimeline"` → event log theo task (audit/debug)
### 2. migration
#### 2.1 sync task status
```sql
create table dbo.EcomSyncTaskStatus (
    SyncTaskId int identity(1,1) primary key,
    RetryCount int null constraint DF_EcomSyncTaskStatus_RetryCount default 0,
    LastErrorCode nvarchar(50) null,
    LastErrorMessage nvarchar(500) null,
    CreatedAt datetime null,
    UpdatedAt datetime null,
    CompletedAt datetime null,
    Service nvarchar(50) null
);
```
#### 2.2 promotion (aggregate root)
```sql
create table dbo.EcomPromotion (
    Id int identity(1,1) primary key,
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
    CustomersSelection nvarchar(max) null,
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
    constraint FK_EcomPromotion_EcomSyncTaskStatus
        foreign key (SyncTaskId)
        references dbo.EcomSyncTaskStatus(SyncTaskId)
        on delete set null
);
```
#### 2.3 applicable time
```sql
create table dbo.EcomPromotionApplicableTime (
    Id int identity(1,1) primary key,
    PromotionId int not null,
    DayOfWeek int not null,
    StartTime datetime not null,
    EndTime datetime not null,
    constraint FK_EcomPromotionApplicableTime_Promotion
        foreign key (PromotionId)
        references dbo.EcomPromotion(Id)
);
```
#### 2.4 excluded date
```sql
create table dbo.EcomPromotionExcludedDate (
    Id int identity(1,1) primary key,
    PromotionId int not null,
    Timezone nvarchar(max) null,
    StartTime datetime not null,
    EndTime datetime not null,
    constraint FK_EcomPromotionExcludedDate_Promotion
        foreign key (PromotionId)
        references dbo.EcomPromotion(Id)
);
```
#### 2.5 sync task timeline
```sql
create table dbo.EcomSyncTaskTimeline (
    Id int identity(1,1) primary key,
    SyncTaskId int not null,
    EventCode nvarchar(50) null,
    EventMessage nvarchar(4000) null,
    CreatedAt datetime null,
    ActName nvarchar(100) null constraint DF_EcomSyncTaskTimeline_ActName default null,
    constraint FK_EcomSyncTaskTimeline_EcomSyncTaskStatus
        foreign key (SyncTaskId)
        references dbo.EcomSyncTaskStatus(SyncTaskId)
        on delete cascade
);
```
### 3. seed
#### 3.1 system parameters
* `SkyCRMApiServer`: base url gọi skycrm api (ví dụ: `https://api-stg.dcorp.com.vn`)
* `SkyCRMApiPort`: port override nếu khác mặc định (ví dụ: `3000`)
* `SkyCRMApiSuffixApiName`: prefix path để version hóa api (ví dụ: `crm/`)
* `SkyCRMApiDiscountGroupName`: tên group hiển thị bên crm (ví dụ: `[dev] open discount`)
* `SkyCRMApiDiscountGroupCode`: mã group để mapping discount bên crm search id (ví dụ: `666666`)
* `MasterDataOrganizationId`: id tenant/org xác định scope dữ liệu (ví dụ: `8547`)

```sql
insert into "Parameters" ("name", "status", "parentId", "description", "paramName", "intVal", "strVal") values
(N'Sky CRM Api Server', 4, 0, NULL, N'SkyCRMApiServer', 0, N'https://api-stg.dcorp.com.vn'),
(N'Sky CRM Api Port', 4, 0, NULL, N'SkyCRMApiPort', NULL, NULL),
(N'Sky CRM Api Suffix Api Name', 4, 0, NULL, N'SkyCRMApiSuffixApiName', NULL, N'crm/'),
(N'Sky CRM Api Discount Group Name', 4, 0, NULL, N'SkyCRMApiDiscountGroupName', NULL, N'[dev] open discount'),
(N'Sky CRM Api Discount Group Code', 4, 0, NULL, N'SkyCRMApiDiscountGroupCode', 666666, NULL),
(N'Master Data Organization Id', 4, 0, NULL, N'MasterDataOrganizationId', 8547, NULL);
```
