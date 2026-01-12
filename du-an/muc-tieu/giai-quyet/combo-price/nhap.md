SetComboGroups


# combo
--select combo
select * from EcomCombo WHERE Id = 21;
select * from EcomComboExcludedDate WHERE ComboId = 21;
select * from EcomComboApplicableTime WHERE ComboId = 21;
select * from EcomComboGroup WHERE ComboId = 21;
select * from EcomComboProduct WHERE ComboId = 21;
select * from EcomComboVariant WHERE ComboId = 21;

select * from EcomCombo WHERE Id in (23,24);
select * from EcomComboExcludedDate WHERE ComboId in (23,24);
select * from EcomComboApplicableTime WHERE ComboId in (23,24);
select * from EcomComboGroup WHERE ComboId in (23,24);
select * from EcomComboProduct WHERE ComboGroupId in (28,29,30,31);
select * from EcomComboVariant WHERE ComboId in (23,24);
–delete combo
delete from EcomCombo WHERE Id in (23,24);
delete from EcomComboExcludedDate WHERE ComboId in (23,24);
delete from EcomComboApplicableTime WHERE ComboId in (23,24);
delete from EcomComboGroup WHERE ComboId in (23,24);
delete from EcomComboProduct WHERE ComboGroupId in (28,29,30,31);
delete from EcomComboVariant WHERE ComboId in (23,24);

# product
--select product
select * from EcomProduct WHERE Id in (111,112,113);
select * from EcomVariant WHERE ProductId in (111,112,113);
select * from EcomProductOption WHERE ProductId in (111,112,113);

--delete product
delete from EcomProductOption WHERE ProductId in (114);
delete from EcomVariant WHERE ProductId in (114);
delete from EcomProduct WHERE Id in (114);

# items
[data]EcomComboVariant
## mapping
(COMBO-Modifier Group)genSAPComponentMASTER[SAP]=>ComboSku[ECOM]
(ITEM-Menu Items)genSAPCODE[SAP]VariantSku[ECOM]

=> kiểm tra trong items (items này ở đâu)
# data rk7
COMBO genSAPCODE
"28999998"

ITEM genSAPCODE
"21001247"
=> dữ liệu rk7


# data ecom
ComboSku
35000000
35000000
35000000
35000000
35000000
21001247
21001247
21001247

VariantSku
16000228
16000228
35000035
35000035
35000035
35000035
35000035
35000035

# regex
(genSAPCODE=")(.+?)(")

# store proc

##SP_EcomVariant

SELECT
	A.Id,
	A.ProductId,
	CASE 
			WHEN B.ProductType = 'VARIANT' THEN CONCAT(B.ProductName, '-', A.VariantName)
			ELSE A.VariantName
	END AS VariantName,
	A.Sku,
	A.Barcode,
	A.Option1,
	A.Option2,
	A.Option3,
	A.Weight,
	B.TaxRate,
	B.IsPriceIncludedVat,
	A.Unit,
	A.Status,
	A.Created,
	A.Updated,
	A.ProcessStatus,
	B.Category AS ArticleType,
	CASE 
			WHEN B.Category = 'CB' THEN '2'
			ELSE '0'
	END AS SaleType
FROM
	EcomVariant A
	JOIN EcomProduct B ON A.ProductId = B.Id
WHERE
	A.ProcessStatus = 0
ORDER BY
	A.Id ASC;
			

## SP_EcomCombo
SELECT	A.* FROM EcomCombo A
JOIN EcomVariant B ON A.Sku = B.Sku
WHERE A.ProcessStatus = 0
ORDER BY A.Id ASC

			
## SP_EcomComboVariant
SELECT	
	B.Sku AS ComboSku,
	B.Name, 
	A.* 
FROM EcomComboVariant A
JOIN EcomCombo B ON A.ComboId = B.Id
JOIN EcomVariant C ON A.VariantSku = C.Sku
JOIN EcomVariant D ON B.Sku = D.Sku
WHERE A.ProcessStatus = 0
ORDER BY A.Id ASC