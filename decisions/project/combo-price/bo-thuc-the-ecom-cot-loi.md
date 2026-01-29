# bộ thực thể ecom cốt lõi

## mục tiêu
- chuẩn hóa cách nghĩ để thiết kế product / price / store không lẫn vai
- đọc là map được ngay sang bảng db và luồng nghiệp vụ
- loại bỏ khái niệm thừa, chỉ giữ thứ ảnh hưởng quyết định thiết kế

---

## nguyên liệu nền
- product
- variant
- option
- price
- store

---

## ecomproduct
- đại diện cho "một món hàng" ở mức khái niệm
- không bán trực tiếp, không xuất kho
- dùng để nhóm variant và gắn metadata

dùng để làm gì:
- làm gốc cho toàn bộ variant, giá, tồn
- nếu thiếu → hệ thống rối vì không có master

loại:
- mọi thông tin không ảnh hưởng đến sinh variant hoặc hiển thị catalog

---

## ecomproductoption
- bộ thuộc tính tạo biến thể (size, color, ...)
- không tồn tại độc lập để bán

dùng để làm gì:
- sinh tổ hợp variant
- khóa logic cấu hình sản phẩm

loại:
- option không tạo khác biệt giá / tồn / hành vi mua

---

## ecomvariant
- thực thể bán được và xuất kho
- mỗi variant = 1 sku duy nhất

dùng để làm gì:
- gắn giá, tồn kho, barcode
- đơn vị giao dịch thực tế

loại:
- mọi thứ không ảnh hưởng đến bán hoặc tồn

---

## ecompricelist
- bối cảnh giá (theo kênh, khu vực, thời gian)
- không chứa con số giá

dùng để làm gì:
- tách logic giá khỏi product
- cho phép nhiều bảng giá song song

loại:
- pricelist không gắn store hoặc rule rõ ràng

---

## ecompricitem
- giá cụ thể của 1 variant trong 1 pricelist

dùng để làm gì:
- nơi duy nhất chứa số tiền thật
- quyết định khách trả bao nhiêu

loại:
- giá không có hiệu lực thời gian hoặc không gắn variant

---

## ecomstore
- bối cảnh bán hàng (vật lý hoặc online)
- quyết định giá mặc định, kho, ngôn ngữ

dùng để làm gì:
- nối product + price + fulfillment
- phân tách thị trường

loại:
- store không quyết định được gì → gộp hoặc bỏ

---

## mapping nhanh để quyết định thiết kế
- không bán được → product / option
- bán + tồn → variant
- đổi giá theo ngữ cảnh → pricelist
- số tiền cụ thể → priceitem
- thị trường vận hành → store

---

## từ vựng giữ lại (map thẳng db)
- product: catalog, master product, category
- option: attribute, configurable attribute
- variant: sku, inventory item
- pricelist: price book, pricing rule
- priceitem: unit price, currency
- store: channel, market, warehouse
