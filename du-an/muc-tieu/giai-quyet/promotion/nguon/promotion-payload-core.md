# promotion payload – core

## 1. sự tồn tại của promotion

promotion có chạy hay không chỉ phụ thuộc vào:

* `status`
* `starttime`, `endtime`
* `tenantid`

gia hạn = cập nhật `endtime`.
stop / expired chỉ là trạng thái dẫn xuất từ thời gian.

---

## 2. phạm vi áp dụng (scope)

promotion chỉ được xét khi đơn hàng nằm trong phạm vi:

* `storesselection` + `entitledstores`
* `shippingtypeselection` + `entitledshippingtypes`

không đúng scope → loại ngay, không kiểm tra gì thêm.

---

## 3. thời gian áp dụng chi tiết

luồng kiểm tra chuẩn:

1. `starttime` → `endtime`
2. nếu `limitbyweekdays = true` → kiểm tra `applicabletimes`
3. nếu `excludespecialdates = true` → loại trừ theo `excludeddates`

`excludeddates` có ưu tiên cao nhất.

---

## 4. loại khuyến mãi (bản chất)

* `promotiontype`

  * product_discount
  * order_discount
  * buy_x_get_y_discount
  * shipment_discount

loại này quyết định toàn bộ logic phía sau.

---

## 5. điều kiện áp dụng

promotion chỉ kích hoạt khi điều kiện đạt:

* `applicableconditiontype`
* `applicableconditionvalue`

điều kiện chỉ là cổng kiểm tra, không ảnh hưởng giá trị giảm.

---

## 6. đối tượng áp dụng

### chọn sản phẩm tham gia điều kiện

* `productsselection`

  * all
  * collection_prerequisite
  * product_prerequisite
  * variant_prerequisite

các `entitled*` chỉ là dữ liệu theo lựa chọn, không phải logic mới.

---

## 7. đối tượng được giảm

* `productspromotionselection`
* `entitledpromotionproducts / variants / collections`

sản phẩm điều kiện và sản phẩm được giảm là hai khái niệm tách biệt.

---

## 8. giá trị khuyến mãi

* `applicablevaluetype`

  * percent
  * amount
  * free
* `applicablevaluevaluepercent / amount`
* `applicablevaluevaluelimitmaxamount`

limit max là rào bảo vệ tài chính.

---

## 9. áp dụng đồng thời (stacking)

* `iscombinedproductdiscount`
* `iscombinedorderdiscount`
* `iscombinedshipmentdiscount`

đây là policy hệ thống, không phải cấu hình riêng lẻ.

---

## 10. có thể bỏ qua khi đọc lần đầu

chỉ xử lý khi làm rule phức tạp:

* special products
* combo / variant nâng cao
* cấu hình loại trừ chéo

---

## tóm tắt một dòng

promotion = thời gian đúng → scope đúng → điều kiện đạt → áp đúng sản phẩm → giảm đúng giá trị → kiểm soát chồng khuyến mãi.

nắm được dòng này là đủ làm việc với 80% case thực tế.
