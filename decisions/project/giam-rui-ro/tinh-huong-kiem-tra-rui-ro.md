# kết quả tình huống kiểm tra theo timeline + gherkin (bdd)

## mục tiêu
- dùng để kiểm chứng đúng/sai
- phân loại retry / không retry
- làm chuẩn giao tiếp dev / vận hành

---

## timeline tổng quát (nhìn để định vị vấn đề)

- t0: user / hệ gửi thực hiện hành động
- t1: backend xử lý kỹ thuật
- t2: dữ liệu ghi / truyền
- t3: hệ nhận / cache / index xử lý
- t4: user nhìn thấy / business xác nhận
- t5: kết luận success / failed

=> **kết luận luôn ở t4–t5, không ở t1–t2**

---

# case 5 — có dữ liệu nhưng user không thấy  
[failed – có thể retry]

## scenario 5.1 — ghi db thành công nhưng ui không hiển thị

given backend ghi db thành công  
and user reload ui  
when user không nhìn thấy dữ liệu  
then trạng thái là failed  
and lý do là not visible  
and cho phép retry  
and không được đánh success

---

## scenario 5.2 — backend xong nhưng cache/index chưa sync

given backend xử lý xong  
and cache hoặc search index chưa cập nhật  
when user truy cập dữ liệu  
then user không thấy dữ liệu  
and trạng thái là failed  
and retry được phép  
and success chỉ khi user nhìn thấy

---

## scenario 5.3 — retry cùng payload cho đến khi user thấy

given payload được retry nhiều lần  
and hệ thống idempotent  
when user đã nhìn thấy dữ liệu  
then trạng thái chuyển sang success  
and không tạo dữ liệu trùng

---

## kết luận case 5

- success = user dùng được
- ghi db không đủ
- retry dùng cho lệch thời điểm (timing / eventual consistency)
- không đánh done sớm

---

# case 6 — hai hệ hiểu khác nhau cùng một khái niệm  
[failed – không retry]

## scenario 6.1 — sender gửi thiếu semantic cần thiết

given sender gửi promotion  
and thiếu field business bắt buộc  
when receiver xử lý  
then không thể áp dụng nghiệp vụ  
and trạng thái là failed  
and không retry

---

## scenario 6.2 — cùng payload nhưng hiểu khác ý nghĩa

given sender hiểu promotion là giảm %  
and receiver hiểu là mua x tặng y  
when receiver xử lý  
then kết quả nghiệp vụ sai  
and failed vĩnh viễn  
and không retry

---

## scenario 6.3 — retry payload sai semantic

given payload sai semantic  
when retry nhiều lần  
then kết quả không thay đổi  
and retry bị coi là lãng phí

---

## kết luận case 6

- retry không sửa lỗi hiểu sai
- semantic contract là bắt buộc
- đúng dữ liệu > đúng thời điểm

---

# case 4 — giao rồi nhưng không ai xác nhận  
[failed – có thể retry]

## định nghĩa trạng thái (khóa não)

- processing = đang xử lý
- success = có xác nhận business
- failed = không đủ bằng chứng thành công

---

## scenario 4.1 — sender gửi xong, không có ack

given sender gửi thành công  
and không nhận được ack  
when hết thời gian chờ  
then trạng thái là failed  
and cho phép retry

---

## scenario 4.2 — receiver xử lý xong nhưng không callback

given receiver xử lý xong  
and không callback  
when sender kiểm tra trạng thái  
then sender không được suy đoán success  
and trạng thái là failed

---

## scenario 4.3 — retry khi thiếu ack

given retry cùng payload  
and receiver không idempotent  
when retry xảy ra  
then rủi ro duplicate nằm ở receiver  
and sender không sai

---

## kết luận case 4

- ack là điều kiện bắt buộc để success
- không có trạng thái treo
- retry chỉ cho failed do thiếu xác nhận

---

# case người dùng thêm / sửa / xóa cơ bản

## scenario — receiver đã xóa, sender gửi lại cùng mã

given receiver đã xóa store  
and sender gửi lại store cùng mã  
when receiver xử lý  
then phải tạo mới store  
not cập nhật bản ghi đã xóa

---

## kết luận

- hiện tại chưa đạt
- trạng thái pending
- cần làm rõ rule delete vs recreate

---

# case 1 — user lặp lại cùng hành động tạo

## scenario 1.1 — bấm tạo hai lần cùng mã

given user tạo store cùng mã  
when action lặp  
then hệ nhận chỉ update  
not tạo bản ghi mới

---

## scenario 1.2 — xóa rồi tạo lại cùng mã

given store đã bị xóa (status = 0)  
when user tạo lại  
then trạng thái phải chuyển sang new  
not giữ trạng thái đã xóa

---

# case 2 — đến nơi không đúng thứ tự

## scenario 2.1 — update trước create

given update chạy trước create  
when handler xử lý  
then phải failed  
and không được giả định create đã tồn tại

---

## scenario 2.2 — sự kiện chỉ bắn một lần

given create và update cùng store  
when chỉ một event được bắn  
then hệ thống xử lý thiếu  
and đây là lỗi thiết kế luồng

---

## kết luận chung

- kết luận chỉ dựa trên business observable
- retry chỉ dùng cho timing, không cho semantic
- queue/log/db timestamp là công cụ quan sát
- không suy đoán, không hy vọng
- hệ thống đúng khi tự kết luận được success/failed
