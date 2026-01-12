## case 1: bấm lại một việc nhiều lần

### 1.1 UI không phản hồi đủ nhanh

* không disable nút sau khi click
* không loading / không feedback trạng thái
* người dùng tưởng hệ thống chưa nhận

> người dùng không sai, họ chỉ không được trấn an

---

### 1.2 client retry nhưng không gắn định danh

* retry do timeout mạng
* mỗi request là một payload “mới tinh”
* backend không phân biệt được cùng một ý định

> hệ thống thấy 3 request, nhưng người dùng chỉ có 1 suy nghĩ

---

### 1.3 backend không idempotent

* không có idempotency key
* không check request đã xử lý chưa
* mỗi lần vào là xử lý tiếp

> máy móc rất chăm chỉ, nhưng không biết kiềm chế

---

### 1.4 async trả kết quả trễ

* job chạy nền
* client chưa thấy kết quả → bấm lại
* kết quả cũ và mới chồng lên nhau

> chậm một nhịp là sinh thêm một hành động

---

## case 2: làm việc sau khi việc trước chưa xong

### 2.1 thiếu ràng buộc thứ tự

* xử lý song song trong khi business cần tuần tự
* không có dependency check
* “cứ chạy trước đi”

> nhanh hơn không đồng nghĩa với đúng hơn

---

### 2.2 trạng thái trung gian không được lưu

* chỉ lưu trạng thái đầu và cuối
* không biết đang ở bước nào
* hành động sau không biết nên chờ hay chạy

> hệ thống không nhớ mình đang làm dở

---

### 2.3 event đến nhanh hơn xử lý

* queue không giới hạn tốc độ
* consumer xử lý chậm
* event sau vượt mặt event trước

> đời không chờ ta, event cũng vậy

---

### 2.4 giả định ngầm “chắc xong rồi”

* không check completion
* không verify điều kiện
* code tin vào may mắn

> bug sinh ra từ niềm tin mù quáng

---

## case 3: gửi cho nơi đã không còn nhận nữa

### 3.1 dữ liệu cache bị lỗi thời

* đối tượng đã disable / delete
* cache chưa refresh
* hệ thống tin vào dữ liệu cũ

> quá khứ quay lại phá hiện tại

---

### 3.2 không validate trạng thái trước khi gửi

* chỉ cần có ID là gửi
* không check active / available
* fail xảy ra muộn

> gửi thư cho người đã chuyển nhà

---

### 3.3 async job chạy trễ

* job tạo lúc đối tượng còn sống
* chạy khi đối tượng đã “chết”
* không có bước re-check

> quá khứ gửi quà cho hiện tại không còn tồn tại

---

### 3.4 receiver không reject rõ ràng

* không trả lỗi cụ thể
* chỉ im lặng hoặc timeout
* sender không biết nên dừng

> bị từ chối nhưng không ai nói thẳng

---

## case 4: rủi ro "giao rồi nhưng không ai xác nhận"
ack (acknowledgement) = xác nhận
### 4.1. ack không bao giờ được gửi

* bên nhận xử lý xong nhưng **không implement ack**
* hiểu sai khái niệm: *nhận được request = đã xong*
* thiếu contract kỹ thuật ngay từ đầu

> nguyên nhân này rất hay gặp ở hệ thống “làm được là mừng rồi”

---

### 4.2. ack có gửi nhưng gửi sai nơi

* callback URL sai
* config env nhầm (dev / staging / prod)
* NAT, firewall, IP whitelist chặn mất

> ack tồn tại trong vũ trụ song song, sender không bao giờ thấy

---

### 4.3. ack gửi rồi nhưng sender không nhận được

* network chập chờn
* retry phía receiver nhưng **sender đã đánh dấu failed**
* ack bị timeout / dropped ở gateway

> hai bên đều nghĩ mình đúng, log thì mỗi đứa một câu chuyện

---

### 4.4. ack gửi thiếu hoặc sai định danh

* thiếu `messageId / correlationId`
* gửi nhầm id của request khác
* format không đúng contract

> có thư trả lời nhưng không biết trả lời cho ai

---

### 4.5. ack bị gửi nhiều lần hoặc không idempotent

* receiver retry ack
* sender không xử lý trùng
* kết quả: sender bỏ ack hợp lệ vì đã “fail trước đó”

> tin nhắn tới trễ nhưng lại bị block cửa

---

### 4.6. ack phụ thuộc vào luồng bất định

* chỉ ack khi business xử lý xong 100%
* business treo, lock, deadlock
* ack không bao giờ được phát ra

> chờ mọi thứ hoàn hảo rồi mới rep, và rồi… không bao giờ rep

---

### 4.7. hiểu sai khái niệm “thành công”

* sender nghĩ: HTTP 200 là xong
* receiver nghĩ: ghi DB xong mới là success
* không thống nhất **success = thời điểm nào**

> mỗi người một định nghĩa, hệ thống thành thơ siêu thực

---

## case 5: có dữ liệu nhưng người dùng không thấy

### 5.1 dữ liệu đúng nhưng query sai

* filter sai điều kiện
* join thiếu
* sort / paging che mất dữ liệu

> dữ liệu có đó, nhưng bị giấu kỹ quá

---

### 5.2 cache / index chưa cập nhật

* DB có nhưng cache chưa sync
* index rebuild chậm
* người dùng thấy “chưa có gì”

> sự thật đến trễ hơn kỳ vọng

---

### 5.3 phân quyền hiển thị không khớp

* data thuộc user A
* user B đang xem
* không lỗi kỹ thuật, chỉ là không thấy

> không phải không tồn tại, chỉ là không dành cho bạn

---

### 5.4 UI không refresh theo thay đổi

* state cũ
* không subscribe event
* cần reload mới thấy

> dữ liệu thay đổi, màn hình thì không

---

## case 6: mỗi hệ thống hiểu khác nhau cùng một khái niệm

### 6.1 cùng tên field, khác ý nghĩa

* `status = 1` mỗi bên hiểu một kiểu
* enum không đồng bộ
* mapping ngầm trong code

> cùng một chữ, mỗi người đọc một nghĩa

---

### 6.2 thiếu contract business rõ ràng

* chỉ thống nhất schema
* không thống nhất semantics
* đúng JSON nhưng sai tinh thần

> nói đúng câu, nhưng sai ý

---

### 6.3 thay đổi một phía, không báo phía kia

* update logic
* không bump version
* hệ thống còn lại không biết gì

> một người đổi luật, cả làng vẫn chơi theo luật cũ

---

### 6.4 test riêng lẻ, thiếu end-to-end

* mỗi hệ thống pass test của mình
* ghép lại thì lệch
* lỗi chỉ lộ ra ở production

> từng mảnh đều đẹp, ghép lại thành tranh trừu tượng

---


