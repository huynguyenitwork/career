# discount / surcharge engine (r-keeper v7)

**góc nhìn kỹ sư tích hợp & đồng bộ hệ thống**

---

## i. bản chất hệ thống (hiểu đúng để không sai từ đầu)

**discount / surcharge = rule engine tính giá**, không phải phép toán đơn giản.

hệ thống gồm:

* tập **rule**
* có **điều kiện**
* có **thứ tự ưu tiên**
* có **phạm vi tác động**
* có **quy tắc kết hợp**

=> khi tích hợp: phải coi đây là **pricing engine có trạng thái**, không phải field cộng thêm.

---

## ii. các thực thể cốt lõi (20% dữ liệu quyết định 80% logic)

### 1. discount / surcharge

* có thể là **%** hoặc **số tiền**
* có thể **giảm** hoặc **phụ thu**
* một discount **không tự hoạt động** nếu không có detail

---

### 2. detail (detallization) – quan trọng nhất

mỗi discount có **1 hoặc nhiều detail**, mỗi detail gồm:

* giá trị (% / amount)
* điều kiện áp dụng
* priority (thứ tự xét)

**quy tắc cốt lõi**:

* duyệt detail **theo priority**
* gặp detail đầu tiên thỏa → áp dụng
* với % discount: có thể áp dụng **nhiều detail trên nhiều item**

=> đây là **rule evaluation có short-circuit**

---

## iii. phạm vi tác động (scope) – bắt buộc phải map đúng

### 1. order scope

* áp dụng cho toàn bộ đơn
* chỉ tồn tại **1 instance**

### 2. seat / guest scope

* áp dụng theo từng khách
* có thể nhiều seat trong 1 order

### 3. item scope

* áp dụng theo **từng dòng item**
* cùng món nhưng khác dòng → scope khác

⚠️ **sai scope = sai toàn bộ tiền**

---

## iv. distributed vs non-distributed (điểm hay gây lệch báo cáo)

### 1. distributed

* discount / surcharge **phân bổ vào item**
* tổng đúng, item thay đổi

### 2. non-distributed

* tạo **dòng riêng**
* có thể:

  * có tax riêng
  * không fiscal
  * không bị discount khác tác động

ví dụ:

* tip
* phí dịch vụ
* phí vào cửa

=> khi tích hợp:

> non-distributed **không phải item bán hàng**

---

## v. composition (kết hợp discount) – nguồn gốc của lỗi

### 1. hai loại discount

* **freely combinable** → luôn cộng
* **non-combinable** → phải có composition

### 2. composition định nghĩa:

* lấy **lớn nhất**
* **cộng**
* **chỉ lấy cái đầu**
* **giảm dần**

### 3. nguyên tắc sống còn

* không có composition phù hợp → **discount không áp dụng**
* composition chỉ có hiệu lực **trên vùng scope giao nhau**

=> 80% case “sao không ra tiền” là do thiếu composition

---

## vi. rule áp dụng (manual vs automatic)

### 1. rule type

* allow (mặc định)
* deny
* automatic

### 2. automatic discount

* không cho sửa giá trị
* có thể bị xóa nếu có quyền
* nếu nhiều auto → lấy discount có **code nhỏ hơn**

=> khi sync:
**automatic ≠ manual**, dù cùng discount code

---

## vii. điều kiện detail (logic nghiệp vụ ẩn)

detail có thể phụ thuộc:

* category item
* min amount
* min quantity
* guest count
* restaurant
* guest type
* bonus type (pds)

### flag quan trọng

**apply on exceeding**

* chỉ áp dụng phần vượt ngưỡng
* phụ thuộc **thứ tự item trong order**

=> không thể tính lại chỉ từ tổng tiền

---

## viii. discount ở mức thanh toán (payment level)

* gắn với **currency**
* áp dụng **khi thanh toán**
* có thể auto
* không áp dụng lại nếu đã gắn manual cùng scope

=> payment ≠ order
=> có thể xuất hiện **sau khi order đã đóng**

---

## ix. tip / gratuity (case đặc biệt)

* là **non-distributed surcharge**
* có thể:

  * không fiscal
  * không tax
  * không đi qua rule detail
* có logic riêng khi “change → tip”

⚠️ không bao giờ map tip thành item bán hàng

---

## x. checklist 20/80 cho kỹ sư tích hợp

### bắt buộc phải lưu / sync

* item line identity
* scope (order / seat / item)
* distributed flag
* applied discount list
* auto vs manual
* final calculated value (sau composition)

### khi debug lệch tiền

1. không áp dụng → kiểm composition
2. tổng đúng, item sai → kiểm distributed
3. thanh toán lệch → kiểm payment discount
4. tip lệch → kiểm non-fiscal flag

---

## xi. kết luận ngắn gọn (để nhớ lâu)

> đây **không phải hệ thống discount**
> mà là **pricing rule engine có ưu tiên, phạm vi và trạng thái**

nếu bạn nhớ **5 từ khóa này**, là đủ làm integration an toàn:
**rule – detail – scope – composition – distribution**
