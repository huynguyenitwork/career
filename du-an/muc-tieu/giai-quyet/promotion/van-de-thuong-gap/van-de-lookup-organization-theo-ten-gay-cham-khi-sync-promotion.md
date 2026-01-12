# lookup organization theo tên gây chậm khi sync promotion

## bối cảnh

-  flow sync promotion cần: tìm `organizationId` theo `organizationName`
-  thao tác này bị gọi **lặp lại nhiều lần**
-  query theo tên thường:

  * không tối ưu index
  * tốn db round-trip
-  kết quả: **chậm delivery khi sync hàng loạt**

---

## vấn đề

-  lookup organization theo tên là:

  * master data
  * ít thay đổi
  * bị dùng lặp
-  không cache → db bị gọi vô ích → tăng latency

---

## giải pháp khuyến nghị

### cache mapping OrganizationName → OrganizationId

-  key:

  ```
  OrgByName:{NormalizedOrganizationName}
  ```
-  value:

  ```
  organizationId
  ```

normalize tên trước khi cache:

-  trim
-  lowercase
-  chuẩn hóa ký tự

---

## thời gian cache

-  ttl khuyến nghị: **10–60 phút**
-  organization hiếm khi đổi tên
-  trễ cập nhật ngắn hạn là chấp nhận được

nếu có event update organization → xóa cache chủ động.

---

## luồng xử lý chuẩn

1. normalize organization name
2. kiểm tra cache:

   * Có → lấy `organizationId`
3. không có → query db
4. lưu cache với ttl
5. tiếp tục xử lý promotion

---

## lưu ý

-  cache này dùng để **giảm latency**
-  không liên quan đến chống duplicate promotion
-  không thay thế kiểm tra tồn tại ở db

---

## kết luận

-  lookup theo tên là điểm nghẽn phổ biến
-  cache đúng chỗ giúp:

  * giảm tải db
  * tăng tốc sync
  * delivery ổn định hơn

thiết kế tốt là thiết kế **không để db trả lời những câu hỏi lặp lại**.
