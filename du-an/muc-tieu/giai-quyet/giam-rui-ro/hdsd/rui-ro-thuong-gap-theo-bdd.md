# test theo hướng người dùng bdd ngoài trường hợp cơ bản như cud

## đặt vấn đề
bạn đang test **đúng tư duy của người lái xe thật**, không phải người vẽ bản đồ. bdd ở đây không phải "code cho vui", mà là **mô phỏng đời sống dữ liệu**: có trễ, có kẹt xe, có mất sóng, có người bấm lại nút.

luồng là:

**ecom → service trung gian → job scheduler → rk7 (pos)**

cud chỉ là lớp da. **rủi ro thật nằm ở mạch máu**. mình khoanh đúng 20/80, chỉ nói những chỗ *người dùng ngoài đời* sẽ làm hệ thống đau đầu.

---

## 1. rủi ro "người dùng làm lại cùng một hành động"

### nghiệp vụ
vấn đề: trùng hành động
câu hỏi:
=> một hành động của người dùng có bị hiểu nhầm thành nhiều hành động không?

nếu không test:
- 1 store → pos có 2 store
- mapping loạn → sửa rất mệt

mục tiêu test:
=> dù user bấm bao nhiêu lần, hệ thống chỉ tạo 1 kết quả duy nhất.

### kỹ thuật
bdd hay bỏ sót cái này, đời thì không.

ví dụ:

* user bấm "lưu store" 2 lần
* ecom retry vì timeout
* job bị chạy lại sau khi fail

quan sát được:

* store được tạo 2 lần bên rk7
* mapping store_id ↔ rk7_id bị lệch

cách test bdd:

> given store đã gửi
> when gửi lại cùng payload
> then pos chỉ có **1 store duy nhất**

keyword cần check: **idempotency** (xử lý trùng lặp).

---

## 2. rủi ro "đến nơi không đúng thứ tự"

### nghiệp vụ
vấn đề: sai thứ tự xử lý
câu hỏi:
=> hệ thống có làm đúng việc, đúng thời điểm không?

nếu không test:
- update khi chưa create
- disable trước khi sync xong
→ job "xanh" nhưng dữ liệu "chết"

mục tiêu test:
=> chỉ xử lý khi điều kiện trước đó đã xong.

### kỹ thuật
scheduler là kẻ hay gây họa nhất.

ví dụ:

* update store chạy trước create
* disable chạy trước sync thành công

quan sát được:

* pos log báo "store not found"
* job success nhưng pos không có dữ liệu

bdd nên có:

> given store chưa tồn tại ở pos
> when nhận update
> then job phải wait hoặc fail có lý do

từ khóa: **ordering & dependency**.

---

## 3. rủi ro "hẹn giờ nhưng quên người nhận" không muốn nhận nữa

### nghiệp vụ
vấn đề: điều kiện tiền đề không còn đúng
câu hỏi:
=> hệ thống có đang làm một việc vô nghĩa không?

ví dụ rất đời:
- store đã disable
- mapping bị xóa
- pos đang downtime

nếu vẫn chạy:
→ tốn tài nguyên, dữ liệu lệch, khó debug

mục tiêu test:
=> không làm gì cả nếu không còn người nhận hợp lệ.

quan trọng: case này **không retry**.

### kỹ thuật
scheduler lập lịch nhưng:

* store đã bị disable
* mapping đã bị xóa
* pos tạm downtime

quan sát được:

* job chạy success
* nhưng pos không nhận gì

bdd test:

> given store bị disable trước giờ chạy
> when scheduler trigger
> then job phải skip, không push

từ khóa: **pre-condition check**.

---

## 4. rủi ro "pos nhận nhưng không xác nhận"

### nghiệp vụ
vấn đề: không có xác nhận từ pos
câu hỏi:
=> ai nói là giao hàng xong?

nếu không test:
- service nghĩ đã xong
- pos không nhận
→ lệch trạng thái vĩnh viễn

mục tiêu test:
=> chỉ khi pos xác nhận thì mới gọi là thành công.

### kỹ thuật
luồng chuẩn phải có **ký nhận hàng**.

nếu không:

* service tưởng đã giao
* pos thì… im lặng

quan sát được:

* không có ack từ rk7
* nhưng job đã mark done

bdd bắt buộc:

> given pos trả lỗi / timeout
> then job = fail
> and có retry / manual handling

từ khóa: **acknowledgement**.

---

## 5. rủi ro "giao đúng nhưng người dùng không thấy"

### nghiệp vụ
vấn đề: người dùng không thấy dù dữ liệu có
câu hỏi:
=> dữ liệu có thật sự dùng được không?

nếu không test:
- dev bảo "có record rồi"
- cửa hàng bảo "không bán được"

mục tiêu test:
=> người dùng mở pos là thấy và thao tác được.

### kỹ thuật
cái này rất đời.

ví dụ:

* store có ở pos
* nhưng sai timezone / sai trạng thái
* nhân viên không thấy để bán

quan sát được:

* pos có record
* nhưng ui không hiển thị

bdd test:

> given store sync thành công
> when mở pos ui
> then store phải selectable

từ khóa: **functional visibility**, không chỉ "có record".

---

## 6. rủi ro "mỗi hệ thống hiểu store một kiểu"

### nghiệp vụ
vấn đề: mỗi hệ thống hiểu store một kiểu
câu hỏi:
=> cùng một từ "store" nhưng có đang nói cùng một thứ không?

nếu không test:
- thiếu thuế
- thiếu ca bán
- pos mở không được

mục tiêu test:
=> dữ liệu gửi sang phải đủ để pos vận hành.

### kỹ thuật
ecom hiểu store là:

* nơi bán

rk7 hiểu store là:

* đơn vị vận hành, ca bán, thuế

service trung gian mà không normalize → toang.

quan sát:

* thuế sai
* ca bán không mở được

bdd:

> given store sync
> then các field bắt buộc cho pos phải đầy đủ

từ khóa: **contract mismatch**.

---

## tóm lại – các nhóm rủi ro bdd cần cover

### nghiệp vụ

1. **bấm lại một việc nhiều lần** [DONE]
   → hệ thống phải hiểu đây vẫn là *một hành động*, không tạo kết quả trùng.
2. **làm việc sau khi việc trước chưa xong** [DONE-queue dự phòng]
   → hệ thống chỉ xử lý khi đúng thứ tự cần thiết.
3. **gửi cho nơi đã không còn nhận nữa** [PENDING-clarify thuộc phần test basic]
   → nếu đối tượng đã bị tắt / xóa / không sẵn sàng thì *đừng xử lý*.
4. **giao rồi nhưng không ai xác nhận** [PROCESSING-retry]
   → chưa có xác nhận từ nơi nhận thì *chưa được coi là thành công*.
5. **có dữ liệu nhưng người dùng không thấy** [PROCESSING-retry] (như mục 4)
   → dữ liệu chỉ có giá trị khi người dùng nhìn thấy và dùng được.
6. **mỗi hệ thống hiểu khác nhau cùng một khái niệm** [LOGIC-2 hệ thống confirm contract với nhau]
   → dữ liệu gửi đi phải đủ và đúng theo cách hệ thống nhận cần để vận hành.
   
---

### kỹ thuật
1. trùng hành động (retry, double click)
2. sai thứ tự (scheduler)
3. điều kiện tiền đề không còn đúng
4. không có xác nhận giao hàng
5. người dùng không thấy dù dữ liệu có
6. hai hệ thống hiểu khác nhau cùng một khái niệm

---

## quyết định nhanh cho bạn lúc này

nếu mục tiêu là **test đúng như có bdd ngoài đời** thì:

> **chỉ cần chứng minh 1 điều:**
> "một store đi hết luồng – được pos xác nhận – và người dùng nhìn thấy & dùng được."

làm được điều đó với **1 store duy nhất**, mọi thứ còn lại chỉ là nhân bản.

bạn không lan man đâu. bạn đang **đặt đúng câu hỏi của kiến trúc sư hệ thống**, không phải tester gạch đầu dòng.
dòng chảy mà thẳng, thì xe nhiều cũng không kẹt.
