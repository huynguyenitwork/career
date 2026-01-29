# script SP_EcomPromotion_OpenDiscount_SkyCRM
– kiểm tra danh sách promotion đang chờ đồng bộ từ ecom đối với loại discount mở
CREATE PROCEDURE [dbo].[SP_EcomPromotion_OpenDiscount_SkyCRM]
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM EcomPromotion
    WHERE ProcessStatus = 0
      AND PromotionType = 'OPEN_DISCOUNT'
    ORDER BY Id ASC;
END
