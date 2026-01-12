# tài liệu: design-pattern và các vấn đề thực tế mà nó giải quyết

## 1. mục tiêu của tài liệu

tài liệu này giúp bạn:

- hiểu vì sao design-pattern tồn tại
- biết mỗi pattern sinh ra để chữa "nỗi đau" thực tế nào
- thấy các biến thể khác nhau của từng nhóm pattern
- áp dụng được khi gặp bài toán mới chứ không chỉ nhớ tên

ý tưởng trung tâm
→ pattern chỉ là cách đặt tên cho những giải pháp mà lập trình viên đã dùng từ lâu
→ khác dự án, khác ngôn ngữ, bản chất vẫn giống nhau

---

## 2. tổng quan: pattern không phải thần dược, nó là ngôn ngữ chung

design-pattern sinh ra vì:

- hệ thống phức tạp dần lên
- những lỗi giống nhau lặp đi lặp lại
- người ta cần cách nói chuyện ngắn gọn với nhau

nói "áp dụng pattern observer" gọn hơn nhiều so với:

"có mấy thành phần đăng ký theo dõi, khi thằng kia thay đổi thì tất cả đều cập nhật theo".

pattern giúp:

- giảm code trùng lặp
- tăng khả năng bảo trì
- tạo từ vựng chung trong team

---

## 3. chia nhóm pattern theo gốc rễ

cốt lõi có ba nhóm lớn:

### 1) creational pattern

tập trung vào **khởi tạo đối tượng linh hoạt**

### 2) structural pattern

tập trung vào **ghép nối và tổ chức cấu trúc đối tượng**

### 3) behavioral pattern

tập trung vào **hành vi, giao tiếp giữa các đối tượng**

các biến thể chỉ quay quanh ba trục này.

---

## 4. creational pattern – khi việc tạo object trở nên rắc rối

mục tiêu cốt lõi
→ ẩn đi chi tiết khởi tạo, giúp hệ thống linh hoạt khi thay đổi

### 4.1 factory method

vấn đề thực tế

- tạo object nhưng không muốn lộ class cụ thể
- muốn chọn loại object dựa trên dữ liệu hoặc ngữ cảnh runtime

tư duy cốt lõi
"đừng new trực tiếp, hãy nhờ nhà máy tạo hộ"

biến thể

- factory method
- abstract factory
- static factory

ứng dụng thực tế

- tạo service khác nhau theo config
- tạo client api theo version
- khởi tạo job khác nhau theo actname

### 4.2 builder

vấn đề thực tế

- object có quá nhiều tham số
- constructor trở nên dài và xấu
- khó đọc, khó hiểu, dễ truyền thiếu

giải pháp
tách quá trình xây object thành từng bước có ý nghĩa

biến thể

- builder pattern
- fluent builder

ứng dụng

- build request http
- build job (như code bạn gửi)
- build config phức tạp

### 4.3 singleton

vấn đề thực tế

- chỉ muốn tồn tại duy nhất một instance
- ví dụ: logger, cache, config

nguy cơ
lạm dụng dễ thành "biến global biết điều"

---

## 5. structural pattern – khi cần tổ chức nhiều phần với nhau

mục tiêu cốt lõi
→ đơn giản hóa cấu trúc mà không làm thay đổi logic bên trong

### 5.1 adapter

vấn đề

- có hai hệ thống interface không khớp nhau
- bạn không thể sửa cả hai
- nhưng vẫn cần chúng nói chuyện với nhau

giải pháp
viết lớp trung gian chuyển đổi

ứng dụng

- tích hợp legacy system
- thay đổi sdk của bên thứ ba
- chuyển đổi request/response giữa microservices

### 5.2 facade

vấn đề

- hệ thống có quá nhiều module con
- api phức tạp đến mức ai cũng sợ

giải pháp
tạo một "mặt tiền đơn giản" cho cả đống phức tạp phía sau

ứng dụng

- gateway api
- service orchestration
- cung cấp một entry cho hệ thống lớn

### 5.3 decorator

vấn đề

- muốn mở rộng hành vi class
- nhưng không được sửa code gốc

giải pháp
bọc đối tượng bằng lớp khác để "độn thêm chức năng"

ứng dụng

- logging cho repository
- timing cho service
- thêm cache cho api call

---

## 6. behavioral pattern – khi đối tượng phải tương tác với nhau

mục tiêu cốt lõi
→ quản lý cách các đối tượng nói chuyện và phối hợp hành vi

### 6.1 observer

vấn đề

- một đối tượng thay đổi
- nhiều đối tượng khác cần biết và cập nhật theo

giải pháp
cơ chế đăng ký–nhận thông báo

biến thể

- event
- pub/sub
- webhook

liên hệ với job
→ bản chất job callback là observer ở cấp hệ thống

ứng dụng

- ui binding
- event sourcing
- notification cascade

### 6.2 strategy

vấn đề

- nhiều thuật toán khác nhau cho cùng 1 mục tiêu
- muốn thay đổi thuật toán linh hoạt khi runtime

giải pháp
đóng gói từng "chiến lược" vào object riêng

ứng dụng

- tính phí ship theo vùng
- chọn retry policy
- biến đổi dữ liệu theo format

### 6.3 command

vấn đề

- muốn đóng gói hành động thành đối tượng
- có thể xếp hàng, log, undo, retry

liên hệ mạnh với job
job = command chạy ở nền

ứng dụng

- queue job system
- task scheduling
- undo trong editor

---

## 7. nhìn từ trên cao: pattern và job liên quan thế nào

job system thực chất là nơi:

- producer tạo **command**
- queue đóng vai **invoker**
- worker đóng vai **executor**
- observer nhận callback
- factory tạo loại job khác nhau

kết luận hay ho
→ job không nằm ngoài pattern
→ nó là sự phối hợp của nhiều pattern cùng lúc

---

## 8. 20/80 để áp dụng nhanh

học 20% sau là xử lý 80% tình huống:

- factory để tạo thứ linh hoạt
- builder để xây thứ phức tạp
- facade để đơn giản hóa hệ thống lớn
- adapter để tích hợp thứ không tương thích
- observer để phản ứng theo sự kiện
- strategy để hoán đổi thuật toán
- command để đóng gói hành động thành job

phần còn lại chỉ là… biến thể có makeup đẹp hơn.

---

## 9. kết luận

design-pattern không phải là nghi lễ học thuộc tên tiếng anh kỳ lạ.
nó chỉ là:

- gọi tên những cách giải quyết vấn đề đã tồn tại
- giúp chúng ta nói chuyện bằng cùng một ngôn ngữ
- giúp hệ thống dễ mở rộng, dễ bảo trì hơn

thực tế có vô số biến thể, framework, library
nhưng cốt lõi vẫn xoay quanh những nhóm pattern này.

khi gặp bài toán mới, đừng tìm pattern trước
hãy tìm **nỗi đau thực tế** cần giải quyết
pattern chỉ là cái tên bạn gắn lên giải pháp sau đó.

---
