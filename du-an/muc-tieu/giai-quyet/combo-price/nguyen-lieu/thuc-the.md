# nguyên liệu
**product/**price**/store/**combo
---

# Bộ mô tả thực thể 20/80


## EcomProduct

- Nguyên bản của mọi thứ. Một “nhân vật chính” đại diện cho **một món hàng**: nó tên gì, thuộc danh mục nào, mô tả ra sao, xuất hiện ở collection nào.
- Trong codebase: đây là **master product**, cái mà mọi luồng giá – variant – inventory đều xoay quanh.

## EcomVariant

- Phiên bản cụ thể của product.
- Nếu product là “Áo thun”, thì variant là “Áo thun / Size M / Màu Đỏ”.
- Nó mang SKU riêng, barcode riêng, weigh, unit… Tức là **thực thể bán được**, xuất kho được.
- Trong hệ thống: variant chính là “stock keeping unit”.

## EcomProductOption

- Bộ khung để tạo ra variant.
- Option = “Color”, “Size”, “Material”.
- Variant = combination của các option values.
- Trong hệ thống: option chính là **attribute set** giúp generate combination.

## EcomPriceList

- Một bối cảnh giá.
- Hiểu như “price book”: bảng giá cho đại lý, bảng giá theo khu vực, giá ngày lễ, giá theo kênh bán.
- Nó không chứa giá trực tiếp, chỉ là “khung”.

## EcomPriceItem

- Giá cụ thể của **một variant** trong **một pricelist**.
- Nơi con số thật sự nằm: price, compareAtPrice, validFrom/validTo.
- Hiểu nôm na: “variant A = 120.000đ theo bảng giá X”.

## EcomStore

- Cửa hàng – bối cảnh vật lý hoặc kênh bán.
- Store quyết định location, kênh, kho, ngôn ngữ, giá mặc định.
- Trong hệ thống: store = “market context” và là điểm nối giữa product – giá – fulfillment.

---

# Cách hình dung cả thế giới

* **Product**: nhân vật gốc.
* **Option**: thuộc tính mở khóa biến hình.
* **Variant**: hình dạng cuối cùng để đem lên kệ.
* **PriceList / PriceItem**: bảng giá + con số thật.
* **Store**: sân khấu mọi thứ diễn ra.

---

# Từ vựng 20% nhưng mở khóa 80% code

(*tất cả đều map tự nhiên vào từng bảng SQL ở trên*)

**Product**
- catalog
- master product
- metadata
- category
- collection
- publishStatus

**Variant**
- variant sku
- attributes
- combination
- inventory item
- barcode
- stock keeping unit

**Product Option**
- option name
- option value
- attribute set
- configurable attribute

**PriceList**
- pricing rule
- price book
- tier pricing
- region pricing
- effective date
- expiration date

**PriceItem**
- unit price
- compare price
- discounted price
- override price
- pricing scope
- currency

- Store
- location
- branch
- channel
- warehouse
- fulfillment
- locale
- market
- default currency
 
---
