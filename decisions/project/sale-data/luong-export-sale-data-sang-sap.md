# luồng export sale data sang sap

## 1. khóa điều kiện chạy
- chỉ chạy khi "đúng thời gian" + "đúng action export sale"
- thiếu 1 trong 2 → không chạy

## 2. khóa phạm vi code
- lập lịch → `saledatataskscheduleservices`
- tạo xml sale + eod → `generatexmlservice`
- ngoài 2 service này → loại

## 3. flow quyết định xuất dữ liệu
- lấy ca chưa export trong 15 ngày → đã có trong `sap_interfaces` → loại
- validate dữ liệu (đơn, món, giảm giá, thanh toán) → thiếu → invalid
- gom dữ liệu hợp lệ → tạo xml
- gửi xml → success hoặc fail
- lưu log + lịch sử để đối soát

## 4. nguyên tắc xử lý lỗi
- lỗi validate → không gửi
- lỗi gửi → cho phép gửi lại
- không log → coi như không tồn tại

## 5. checklist bắt buộc trước khi dev
- xác định trường dữ liệu bắt buộc trong xml → thiếu → dừng
- đối chiếu xml hiện tại với yêu cầu sap → lệch → ghi ra
- xác nhận sync là background job → không realtime
- xác nhận cơ chế fail: log ở đâu, retry hay không

## 6. công thức rà soát nhanh flow
- dữ liệu lấy từ đâu? → không rõ → đọc code
- mapping có khớp sap? → không → ghi vấn đề
- fail có bị mất dấu? → có → bổ sung log
- ảnh hưởng 7–30 ngày? → không → hoãn

---

# saledatataskscheduleservices – bản hành động

## 1. nhiệm vụ cốt lõi
- mỗi 10 giây kiểm tra task tới giờ chưa
- tới giờ → chạy action
- chạy xong → cập nhật lịch

## 2. vòng lặp sống còn
- service chạy
- gọi `doaction()`
- lấy action hợp lệ
- check thời gian
- execute
- cập nhật `lasttime` / `nexttime`

## 3. action hợp lệ
- `verifyglobalshift` → xác thực ca
- `exportsaledata` → export xml sale + eod
- action khác → không quan tâm

## 4. quyết định "đúng giờ"
- immediately → chạy
- daily / weekly / monthly / periodically → so lịch
- tới `nexttime` → chạy ngay

## 5. 20/80 cần giữ
- kiểm lịch
- chạy action
- cập nhật lịch

## 6. nhiễu cần bỏ
- logic tính giờ phức tạp
- di wiring
- log chi tiết không ảnh hưởng quyết định

## 7. test nhanh trước release
- task tới giờ → có chạy không
- chạy xong → `nexttime` có cập nhật không
- export fail → có log không
- restart service → có mất lịch không
