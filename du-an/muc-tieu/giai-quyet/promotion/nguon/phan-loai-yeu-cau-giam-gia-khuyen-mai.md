# phân loại yêu cầu giảm giá – khuyến mãi

-(theo nguyên lý 20/80 – quyết định nhanh & đúng)*

## mục tiêu

xác định **những loại khuyến mãi promotion engine nên nhận, có thể cân nhắc, và không nên nhận**, nhằm:

- giữ hệ thống **ổn định – dễ test – dễ vận hành**
- tránh rủi ro tài chính và tranh chấp nghiệp vụ
- định nghĩa rõ **scope ngay từ đầu**

---

## i. nhóm nên nhận (core – rủi ro thấp)

### đặc điểm

- quyết định được từ **bill snapshot tại checkout**
- không phụ thuộc lịch sử, trạng thái toàn cục
- cùng input → cùng output (deterministic)

### bao gồm

- **giảm giá sản phẩm / combo / đơn hàng (% hoặc số tiền)**
- **mua x tặng y**
- **điều kiện theo số lượng / giá trị đơn**
- **giảm phí vận chuyển**
- giới hạn thời gian, ngày trong tuần
- cho phép hoặc không cho phép combine rõ ràng

### rủi ro

- thấp, chủ yếu là lỗi cấu hình hoặc rule

### kết luận

=> **bắt buộc hỗ trợ** – đúng bản chất promotion engine

---

## ii. nhóm có thể cân nhắc (có điều kiện)

### đặc điểm

- có yếu tố phụ ngoài bill
- có thể “ép” vào snapshot nếu thiết kế chặt
- rủi ro tăng theo độ linh hoạt

### bao gồm

- khuyến mãi theo cửa hàng / khu vực
- khuyến mãi theo kênh bán (pos / app / web)
- combine nhiều promotion có điều kiện ưu tiên

### rủi ro

- lệch cấu hình giữa hệ thống
- khó debug khi nhiều promotion chạy song song

### điều kiện để nhận

- phạm vi áp dụng **cố định, rõ ràng**
- có rule ưu tiên minh bạch
- có log giải thích quyết định (explainable)

### kết luận

=> **nhận có kiểm soát**, phải ghi rõ điều kiện trong tài liệu

---

## iii. nhóm không nên nhận (rủi ro cao)

### đặc điểm

- cần lịch sử, hành vi, hoặc trạng thái toàn cục
- phụ thuộc hệ thống bên ngoài
- sai là ảnh hưởng **tiền thật / niềm tin khách hàng**

### bao gồm & rủi ro chính

-*1. theo khách hàng (vip, sinh nhật, first order)**

- rủi ro: cần customer history, pos khó đồng bộ
- lý do không nhận: promotion engine ≠ crm

-*2. theo hành vi (mua lần n, bỏ giỏ)**

- rủi ro: cần state & timeline, race condition
- lý do không nhận: phá nguyên lý snapshot

-*3. theo ngân sách (budget cap)**

- rủi ro: overspend, sync đa node, pos offline
- lý do không nhận: cần global state & lock

-*4. theo tồn kho / thời tiết / sự kiện ngoài hệ thống**

- rủi ro: dữ liệu external không ổn định
- lý do không nhận: không kiểm soát được input

-*5. giảm tay / manual override**

- rủi ro: không audit được, dễ tranh chấp
- lý do không nhận: đây là nghiệp vụ vận hành

### kết luận

=> **không nhận trong promotion engine**, nên xử lý ở hệ thống khác (crm, loyalty, pricing, operation)

---

## iv. nguyên tắc chốt

- promotion engine **chỉ xử lý những gì quyết định được tại thời điểm checkout**
- những gì cần lịch sử, hành vi, ngân sách toàn cục → **ngoài scope**
- từ chối sớm = **giảm rủi ro lâu dài**

> hệ thống tốt không phải hệ thống làm được mọi thứ,
> mà là hệ thống **biết rõ mình không làm gì**.
