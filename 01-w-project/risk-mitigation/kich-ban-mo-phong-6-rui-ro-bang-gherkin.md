# kịch bản mô phỏng 6 rủi ro bằng gherkin (tối giản)

## mục tiêu
- nhìn thấy hành vi lỗi qua kịch bản
- đặt tên rủi ro → gắn monitoring + auto-healing
- bỏ code, giữ logic quyết định

---

## bối cảnh chung
- hệ thống nhận event theo entity
- mỗi entity có state
- có monitor ghi nhận rủi ro
- có autohealer quyết định retry / skip

---

## scenario 1: duplicate event

given entity "store_1" chưa tồn tại  
when hệ thống nhận event "create store_1" lần 1  
then entity được tạo và xử lý bình thường  

when hệ thống nhận lại event "create store_1" lần 2  
then event bị bỏ qua  
and monitor ghi nhận "duplicate_event"  

dùng để làm gì:
- phát hiện trùng
- không xử lý lại

---

## scenario 2: out of order

given entity "store_x" chưa tồn tại  
when hệ thống nhận event "update store_x"  
then event bị bỏ qua  
and monitor ghi nhận "out_of_order"  

dùng để làm gì:
- bảo vệ thứ tự xử lý
- tránh tạo state rác

---

## scenario 3: precondition failed

given entity "store_2" đã tồn tại  
and entity ở trạng thái disabled  
when hệ thống nhận event mới cho "store_2"  
then xử lý dừng lại  
and monitor ghi nhận "precondition_failed"  
and autohealer skip entity với lý do "disabled"  

dùng để làm gì:
- không xử lý khi điều kiện nền sai

---

## scenario 4: contract mismatch

given entity "store_3" vừa được tạo  
when hệ thống nhận event với payload sai contract  
then entity chuyển sang failed_non_retryable  
and monitor ghi nhận "contract_mismatch"  

dùng để làm gì:
- phân biệt lỗi nghiệp vụ
- không retry vô ích

---

## scenario 5: no ack từ pos

given entity "store_4" đã được gửi sang pos  
when pos không trả ack  
then entity chuyển sang failed_retryable  
and monitor ghi nhận "ack_timeout"  
and autohealer quyết định retry  

dùng để làm gì:
- xử lý lỗi hạ tầng tạm thời

---

## scenario 6: not visible với user

given entity "store_5" đã được ack thành công  
when dữ liệu chưa hiển thị cho user  
then entity vẫn chưa hoàn tất  
and monitor ghi nhận "not_visible"  
and autohealer quyết định retry  

dùng để làm gì:
- tách ack kỹ thuật và trải nghiệm người dùng

---

## happy path

given entity "store_ok" được create đúng thứ tự  
and không vi phạm điều kiện nào  
when xử lý hoàn tất  
then entity ở trạng thái visible  
and monitor ghi nhận "success"  

---

## quy tắc rút gọn cho toàn bộ kịch bản
- mỗi scenario = 1 rủi ro
- mỗi rủi ro phải có tên
- mỗi tên dẫn tới 1 quyết định (retry / skip / stop)
- không suy đoán từ log, chỉ dựa state

---

## câu chốt
- monitoring là đặt tên rủi ro
- auto-healing là chọn phản xạ
- state machine là bản đồ duy nhất đáng tin