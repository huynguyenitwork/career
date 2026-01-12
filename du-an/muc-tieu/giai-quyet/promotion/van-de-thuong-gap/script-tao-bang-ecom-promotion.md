# EcomPromotion 
CREATE TABLE EcomPromotion (
    Id INT IDENTITY(1,1) PRIMARY KEY,

    Code NVARCHAR(450) NOT NULL,
    Name NVARCHAR(450) NOT NULL,

    Status NVARCHAR(MAX),
    Description NVARCHAR(MAX),

    StartTime DATETIME NOT NULL,
    EndTime DATETIME NULL,

    LimitByWeekdays BIT NOT NULL,
    ExcludeSpecialDates BIT NOT NULL,

    PromotionType NVARCHAR(MAX),

    StoresSelection NVARCHAR(MAX),
    EntitledStores NVARCHAR(MAX),

    ShippingTypeSelection NVARCHAR(MAX),
    EntitledShippingTypes NVARCHAR(MAX),

    ApplicableConditionType NVARCHAR(MAX),
    ApplicableConditionValue DECIMAL(18,0),

    ProductsSelection NVARCHAR(MAX),
    EntitledCollections NVARCHAR(MAX),
    EntitledCombos NVARCHAR(MAX),
    EntitledProducts NVARCHAR(MAX),
    EntitledVariants NVARCHAR(MAX),

    IsRequiredSpecialProducts BIT,
    ApplicableConditionMinimumNumberOfSpecialProducts DECIMAL(18,0),

    ProductsConditionSelection NVARCHAR(MAX),
    EntitledConditionProducts NVARCHAR(MAX),
    EntitledConditionVariants NVARCHAR(MAX),
    EntitledConditionCombos NVARCHAR(MAX),

    ProductsPromotionSelection NVARCHAR(MAX),
    EntitledPromotionCollections NVARCHAR(MAX),
    EntitledPromotionProducts NVARCHAR(MAX),
    EntitledPromotionVariants NVARCHAR(MAX),

    ApplicableValueType NVARCHAR(MAX),
    ApplicableValueValueAmount DECIMAL(18,0),
    ApplicableValueValuePercent DECIMAL(18,0),
    ApplicableValueValueLimitMaxAmount DECIMAL(18,0),

    MaxUsageCount INT,

    IsConfigAppliedTogetherWithSpecialProducts BIT,
    ConfigAppliedTogetherWithSpecialProductsType NVARCHAR(MAX),
    ConfigAppliedTogetherWithSpecialProductsValueIsCombo BIT,
    ConfigAppliedTogetherWithSpecialProductsValueIsVariant BIT,
    EntitledSpecialVariantIds NVARCHAR(MAX),

    IsCombinedProductDiscount BIT,
    IsCombinedShipmentDiscount BIT,
    IsCombinedOrderDiscount BIT,

    TenantId NVARCHAR(MAX),
    EventType NVARCHAR(MAX),
	Created datetime NULL,
	Updated datetime NULL,
	ProcessStatus int NULL,
    CONSTRAINT UQ_EcomPromotion_Code UNIQUE (Code),
    CONSTRAINT UQ_EcomPromotion_Name UNIQUE (Name)
);

# EcomPromotionApplicableTime 
CREATE TABLE EcomPromotionApplicableTime (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    PromotionId INT NOT NULL,

    DayOfWeek INT NOT NULL,       -- 0=Sunday … 6=Saturday
    StartTime DATETIME NOT NULL,
    EndTime DATETIME NOT NULL,
    CONSTRAINT FK_EcomPromotionApplicableTime_Promotion
        FOREIGN KEY (PromotionId)
        REFERENCES EcomPromotion(Id)
);

# EcomPromotionExcludedDate 
CREATE TABLE EcomPromotionExcludedDate (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    PromotionId INT NOT NULL,

    Timezone NVARCHAR(MAX),
    StartTime DATETIME NOT NULL,
    EndTime DATETIME NOT NULL,
    CONSTRAINT FK_EcomPromotionExcludedDate_Promotion
        FOREIGN KEY (PromotionId)
        REFERENCES EcomPromotion(Id)
);
