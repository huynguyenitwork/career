# vấn đề trùng promotion do người dùng thao tác lặp

## bối cảnh

-  hệ thống phản hồi chậm
-  người dùng bấm **tạo promotion** nhiều lần
-  kết quả: promotion bị tạo trùng hoặc request chạy song song

đây là vấn đề **hành vi người dùng + độ trễ hệ thống**, không phải lỗi người dùng.

---

## mục tiêu

-  một ý định tạo promotion → **chỉ tạo 1 promotion**
-  không chặn nhầm ý định hợp lệ
-  tránh duplicate ở cả tầng api và db

---

## giải pháp khuyến nghị (20/80)

### 1. idempotency bằng cache (chặn đầu)

-  cache theo **ý định tạo promotion**, không chỉ theo user
-  ttl: **2–5 phút**

ví dụ key:

```
createpromotion:{shopid}:{promotioncode}
```

hoặc hash từ các field chính của promotion.

---

### 2. kiểm tra db (chặn cuối)

-  trước khi insert:

  * kiểm tra promotion đã tồn tại chưa
-  khuyến nghị:

  * unique key ở db (shopid + promotioncode)

db là **lớp bảo hiểm cuối**, cache chỉ là giảm tải.

---

## luồng xử lý chuẩn

1. nhận request tạo promotion
2. kiểm tra cache:

   * có → trả về promotion đang xử lý / đã tồn tại
3. chưa có → set cache (ttl 2–5 phút)
4. kiểm tra db:

   * có → trả về promotion đã tồn tại
5. chưa có → tạo promotion
6. trả kết quả

---

## thời gian cache hợp lý

-  < 30 giây: không đủ chặn thao tác lặp
-  2–5 phút: **vùng an toàn**
-  > 10 phút: dễ chặn nhầm ý định mới

---

## lưu ý

-  cache **không thay thế** unique constraint
-  cache chỉ dùng cho:

  * chống thao tác lặp
  * chống request song song
-  duplicate luôn phải được chặn ở db

---

## kết luận

-  trùng promotion là vấn đề **thường gặp**
-  cách xử lý đúng:

  * khoan dung với người dùng
  * nghiêm khắc với dữ liệu
-  thiết kế tốt là thiết kế **hiểu hành vi con người** chứ không đòi hỏi họ hoàn hảo

---