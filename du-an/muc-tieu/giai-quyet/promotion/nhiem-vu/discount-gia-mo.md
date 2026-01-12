## 1. yêu cầu

* đồng bộ **promotion/discount giá mở** từ **ecom sang rk7**
* promotion giá mở là loại **không có rule, không validate điều kiện**
* cho phép **nhập số tiền giảm thủ công tại pos**

---

## 2. cần làm gì

* viết **webhook** để nhận dữ liệu promotion giá mở từ ecom
* mapping và **lưu promotion xuống rk7**
* đánh dấu đúng **loại discount = giá mở (open / manual discount)**

---

## 3. các bước thực hiện

1. ecom gửi promotion giá mở qua webhook
2. webhook tiếp nhận và parse dữ liệu
3. lưu promotion vào rk7 với các thông tin tối thiểu:

   * mã
   * tên
   * loại promotion/discount: giá mở
4. đảm bảo pos nhận diện được promotion này là **discount nhập tay**

---

## 4. kết quả mong muốn

* rk7 có promotion giá mở giống ecom
* pos hiển thị được promotion giá mở
* thu ngân có thể **nhập số tiền giảm trực tiếp**
* hệ thống **không validate rule hay điều kiện**

---

## 5. lưu ý

* không xử lý logic tính tiền
* không validate điều kiện áp dụng
* không nằm trong scope promotion engine
* chỉ tập trung **đồng bộ dữ liệu và nhận diện đúng loại discount**

---

## 6. hỏi đáp
Hi Chị Khanh cho em hỏi bên ECOM có **promotionType** cho promotion giá mở (open/manual discount) là gì vậy ạ?
Em cần thông tin field nhận diện này để mapping webhook sang RK7. Em cảm ơn chị.

## 7. vấn đề thường gặp
- tạo promotion trên rk7 như thế nào api thế nào?
- các trường hợp sửa xóa sẽ thế nào?