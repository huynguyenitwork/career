# timeline

## discount / surcharge – r-keeper v7

---

## chương 1 – thuộc tính type discount / surcharge

**mục đích:** định nghĩa *loại* giảm giá / phụ thu.

* xác định: discount hay surcharge
* kiểu giá trị: % hay số tiền
* cho phép hay không cho:

  * sửa giá trị
  * kết hợp với discount khác

=> **giá trị cho tích hợp:**
type = metadata, **không tham gia tính tiền**, nhưng quyết định hành vi phía sau.

---

## chương 2 – sổ discount / surcharge

**mục đích:** tạo discount cụ thể và các detail của nó.

* discount không chạy nếu thiếu detail
* detail chứa:

  * giá trị
  * điều kiện
  * priority

=> **giá trị cho tích hợp:**
detail = **rule thực thi**, phải hiểu thứ tự và điều kiện.

---

## chương 3 – usage rules (sử dụng discount)

**mục đích:** quyết định *khi nào* discount được phép áp dụng.

* 3 chế độ:

  * allow
  * deny
  * automatic
* automatic:

  * hệ thống tự gắn
  * có thể bị xóa nếu có quyền

=> **giá trị cho tích hợp:**
phân biệt **auto vs manual**, không được coi là một.

---

## chương 4 – composition discounts

**mục đích:** giải quyết xung đột giữa các discount.

* discount không tự do kết hợp → cần composition
* composition quy định:

  * cộng
  * lấy lớn nhất
  * lấy cái đầu
  * giảm dần

=> **giá trị cho tích hợp:**
không có composition hợp lệ → discount **không áp dụng**.

---

## chương 5 – bonus types

**mục đích:** định nghĩa logic thưởng điểm.

* bonus chỉ phát sinh khi:

  * discount hợp lệ
  * type bonus khớp pds
* discount có thể = 0 nhưng bonus ≠ 0

=> **giá trị cho tích hợp:**
bonus **phụ thuộc discount**, không độc lập.

---

## chương 6 – tích hợp pds

**mục đích:** kết nối hệ thống giảm giá bên ngoài.

* discount / bonus đến từ thẻ
* áp dụng qua mcr / interface
* discount luôn tính trên **số tiền chưa thanh toán**

=> **giá trị cho tích hợp:**
giá tiền phụ thuộc **external state**.

---

## chương 7 – tính toán composition (calculation engine)

**mục đích:** thuật toán tính tiền cuối cùng.

* tính theo:

  * từng item
  * từng seat
  * từng scope
* composition xét theo thứ tự
* thiếu composition → reject

=> **giá trị cho tích hợp:**
đây là **điểm kết thúc pipeline giá**.

---

## tóm tắt 1 dòng / chương (để nhớ nhanh)

* **ch1:** định nghĩa hành vi
* **ch2:** rule thực thi
* **ch3:** khi nào được dùng
* **ch4:** giải quyết xung đột
* **ch5:** logic thưởng
* **ch6:** phụ thuộc hệ ngoài
* **ch7:** thuật toán cuối

---

## kết luận 20/80

> mỗi chương tương ứng **1 bước trong vòng đời giá tiền**
> đọc đúng chương = debug đúng chỗ

nếu bạn muốn, mình có thể:

* gộp toàn bộ timeline này thành **1 bảng a4**
* hoặc rút tiếp thành **flow 10 bước cực ngắn cho dev dùng hằng ngày**
