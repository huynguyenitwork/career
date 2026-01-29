# promotion engine – phạm vi hỗ trợ & payload chuẩn

## mục tiêu
- chốt nhanh loại khuyến mãi **nhận / cân nhắc / loại**
- khóa scope từ đầu để **ổn định – dễ test – tránh rủi ro tiền**
- mọi thông tin phải quyết định được **tại checkout snapshot**

---

## 1. phân loại yêu cầu khuyến mãi

### 1.1 nhóm bắt buộc nhận
- tiêu chí: quyết định từ bill snapshot, deterministic, không cần lịch sử
- nhận:
  - giảm giá product / order / combo (% | amount)
  - buy x get y
  - điều kiện theo số lượng / giá trị đơn
  - giảm phí vận chuyển
  - giới hạn thời gian, ngày trong tuần
  - cho / không cho combine rõ ràng
- kết luận: **core của promotion engine, phải hỗ trợ**

---

### 1.2 nhóm nhận có điều kiện
- tiêu chí: có yếu tố phụ nhưng ép được vào snapshot
- nhận khi:
  - scope cố định (store / region / channel)
  - rule ưu tiên rõ
  - có log giải thích quyết định
- rủi ro cần chấp nhận:
  - lệch cấu hình
  - debug khó khi chạy song song
- kết luận: **nhận nhưng phải ghi điều kiện rõ trong tài liệu**

---

### 1.3 nhóm loại bỏ
- tiêu chí loại:
  - cần lịch sử / hành vi / trạng thái toàn cục
  - phụ thuộc external system
  - sai là mất tiền hoặc tranh chấp
- loại:
  - theo khách hàng (vip, sinh nhật, first order) → crm
  - theo hành vi (mua lần n, bỏ giỏ) → behavior engine
  - theo ngân sách (budget cap) → cần global state / lock
  - theo tồn kho / thời tiết / sự kiện ngoài hệ thống → external data
  - giảm tay / override → operation
- kết luận: **ngoài scope promotion engine**

---

### 1.4 nguyên tắc chốt
- chỉ xử lý thứ **quyết định được tại checkout**
- cần lịch sử / hành vi / ngân sách toàn cục → loại sớm
- từ chối sớm = giảm rủi ro dài hạn

---

## 2. promotion payload – luồng tối thiểu

### 2.1 promotion có tồn tại không
- kiểm:
  - status
  - starttime / endtime
  - tenantid
- ghi chú:
  - gia hạn = cập nhật endtime
  - stop / expired là trạng thái dẫn xuất

---

### 2.2 scope áp dụng
- kiểm:
  - storesselection + entitledstores
  - shippingtypeselection + entitledshippingtypes
- không đúng scope → **loại ngay**

---

### 2.3 thời gian chi tiết
- thứ tự kiểm:
  - starttime → endtime
  - limitbyweekdays → applicabletimes
  - excludespecialdates → excludeddates
- ưu tiên cao nhất: excludeddates

---

### 2.4 bản chất khuyến mãi
- promotiontype:
  - product_discount
  - order_discount
  - buy_x_get_y_discount
  - shipment_discount
- loại này khóa toàn bộ logic phía sau

---

### 2.5 điều kiện kích hoạt
- applicableconditiontype
- applicableconditionvalue
- vai trò: **cổng kiểm**, không quyết định giá trị giảm

---

### 2.6 đối tượng tham gia điều kiện
- productsselection:
  - all
  - collection_prerequisite
  - product_prerequisite
  - variant_prerequisite
- entitled* chỉ là data theo selection, không phải logic mới

---

### 2.7 đối tượng được giảm
- productspromotionselection
- entitledpromotionproducts / variants / collections
- lưu ý: **sản phẩm điều kiện ≠ sản phẩm được giảm**

---

### 2.8 giá trị giảm
- applicablevaluetype:
  - percent
  - amount
  - free
- value:
  - percent / amount
- applicablevaluevaluelimitmaxamount:
  - rào bảo vệ tài chính

---

### 2.9 áp dụng đồng thời
- iscombinedproductdiscount
- iscombinedorderdiscount
- iscombinedshipmentdiscount
- đây là **policy hệ thống**, không phải config lẻ

---

### 2.10 có thể bỏ qua ban đầu
- special products
- combo / variant nâng cao
- rule loại trừ chéo phức tạp

---

## 3. tóm tắt 1 dòng
- promotion chạy khi: **thời gian đúng → scope đúng → điều kiện đạt → đúng sản phẩm → đúng giá trị → kiểm soát combine**

- nắm dòng này là xử lý được **80% case thực tế**
