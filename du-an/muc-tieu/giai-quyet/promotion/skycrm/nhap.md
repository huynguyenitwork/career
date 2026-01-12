# api

## tài liệu api
http://192.168.2.199:5000/swagger/index.html

## thử nghiệm api


### get discount
#### endpoint

- **tất cả:** http://192.168.2.199:5000/discounts?orgId=1&offset=0&limit=20
- **tùy chọn:** http://192.168.2.199:5000/discounts?orgId=1&storeId=29&discountGroupId=2&discountTypeId=2&status=1&showHidden=0&offset=0&limit=20

#### tham số
**required**
	orgId=1
**optional**
	storeId=29 (31|32)
	discountGroupId=2 (4|6)
	discountTypeId=2 (3|4)
	status=1 (2|3)
	search=<tên của discount [Name]>
	showHidden=false (true)
	offset=0
	limit=20
	orderBy (default: id)
	
–--

# bảng internal
- Discounts
- Discount_DiscountTag_Mappings
- DiscountRules
- DiscountExclusionDishes
- DiscountExclusionCategories
- CouponTypes
- DiscountCombinations
- DiscountGroups

# bảng external
- StoreMappings

- DiscountBillTimes
- DiscountRuleGets
- DiscountRuleMappings
- DiscountTags
- DiscountTypes

# Lưu ý
- Không dùng được file backup tạo bởi dbeaver cả loại global và bình thường restore báo lỗi


