# discount / surcharge – r-keeper v7  

---

## mục tiêu tài liệu
- xác định đúng **điểm can thiệp** khi debug / tích hợp giá
- mỗi mục = 1 bước trong **vòng đời giá tiền**
- đọc sai bước → sửa sai chỗ

---

## 1. type (discount / surcharge)
- phân loại: discount hay surcharge
- định dạng giá trị: % hoặc số tiền
- quy tắc: cho sửa giá trị? cho kết hợp discount khác?
- kết luận: type = metadata, **không tham gia tính tiền**
- dùng để làm gì: quyết định **hành vi phía sau**, không phải số tiền

---

## 2. discount detail (rule)
- discount không có detail → không chạy
- detail gồm: giá trị, điều kiện, priority
- kết luận: detail = **rule thực thi**
- dùng để làm gì: xác định **discount có được kích hoạt hay không**

---

## 3. usage rule (quyền sử dụng)
- chế độ: allow / deny / automatic
- automatic: hệ thống tự gắn, có thể bị xóa nếu đủ quyền
- kết luận: phải phân biệt **auto vs manual**
- dùng để làm gì: tránh nhầm discount hệ thống với discount người dùng

---

## 4. composition (kết hợp discount)
- discount không tự do cộng dồn
- composition quy định: cộng, lấy lớn nhất, lấy cái đầu, giảm dần
- thiếu composition hợp lệ → discount **bị loại**
- dùng để làm gì: xử lý **xung đột discount**

---

## 5. bonus type
- bonus chỉ sinh khi discount hợp lệ
- discount = 0 vẫn có thể có bonus
- bonus phụ thuộc pds mapping
- kết luận: bonus **không độc lập**
- dùng để làm gì: debug điểm thưởng sai nguồn

---

## 6. pds integration
- discount / bonus đến từ hệ ngoài (thẻ, pds)
- áp dụng qua mcr / interface
- luôn tính trên **số tiền chưa thanh toán**
- kết luận: giá phụ thuộc **external state**
- dùng để làm gì: xác định lỗi do nội bộ hay hệ ngoài

---

## 7. calculation engine (final price)
- scope tính: item / seat / scope
- áp dụng composition theo thứ tự
- thiếu composition → reject
- kết luận: đây là **điểm kết thúc pipeline giá**
- dùng để làm gì: chỉ debug số tiền **sau khi** qua hết các bước trên

---

## bản đồ debug 20/80
- sai loại → kiểm tra type
- không chạy → kiểm tra detail
- không cho dùng → kiểm tra usage rule
- sai cộng dồn → kiểm tra composition
- sai điểm thưởng → kiểm tra bonus + pds
- sai số tiền cuối → kiểm tra calculation engine

---

## kết luận
- mỗi mục = 1 gate
- qua đủ gate → giá hợp lệ
- debug theo thứ tự → **đi nhanh, không vòng**
