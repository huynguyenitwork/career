# quy trình export dữ liệu sale sang SAP

## điều kiện cần
- đúng thời gian
- đúng hành động (xuất dữ liệu sale)

## phạm vi
- **lập lịch chạy tự động**: `saledatataskscheduleservices`
- **tạo file xml dữ liệu sale và eod**: `generatexmlservice`

## quy trình làm việc
1. **lấy ca chưa export**  
   - kiểm tra 15 ngày trước  
   - chưa có trong `sap_interfaces`
2. **xác thực dữ liệu**  
   - kiểm tra: đơn, món, giảm giá, thanh toán  
   - đánh dấu invalid nếu thiếu thông tin
3. **chuẩn bị gửi file xml**  
   - gom dữ liệu hợp lệ
4. **gửi file + đánh dấu kết quả**  
   - hoàn thành hoặc thất bại (có thể gửi lại nếu lỗi)
5. **lưu trữ lịch sử**  
   - đối soát dữ liệu, lưu log để kiểm tra sau

## lộ trình tổng quát
- **lấy ca chưa export → xác thực dữ liệu → tạo file xml → gửi → lưu lịch sử**

## điểm quan trọng
- dữ liệu đầy đủ và đúng thời gian  
- kết quả: gửi thành công hoặc log lỗi


# các bước/giai đoạn cần thực hiện (lưu trữ)
- rà soát flow và mapping sale data hiện hành.
- thu thập và phân tích file xml export mẫu (hiện trạng).
- xác định phạm vi source code đang xử lý sale data.

## 1. hiểu luồng và logic hiện tại

- đọc tài liệu về **flow sale data** và **xml export**, nắm các điểm dữ liệu chính.
- đọc sơ bộ **source code xử lý sale data** để biết các bước: lưu, sync, validate, transform…
- xác định các điểm **đầu ra quan trọng** và nơi api sẽ tương tác với rk7.

## 2. kiểm định dữ liệu và mapping

- so sánh **xml export mẫu** với yêu cầu rk7: trường nào đã có, trường nào cần bổ sung.
- đối chiếu bảng mapping 3–5 trường quan trọng (tên, % giảm, thời gian hiệu lực, mã sản phẩm…) xem có khớp với payload rk7 không.
- ghi chú những **bất đồng hoặc thiếu dữ liệu**.

## 3. kiểm tra cơ chế đồng bộ

- xác nhận cách **sync hiện tại**: realtime hay background job.
- ghi nhận các bước khi sync fail: log, retry hay ignore, để đảm bảo có cơ chế kiểm soát lỗi.

## 4. chuẩn bị checklist qc trước khi dev api

- liệt kê các trường dữ liệu **bắt buộc phải có** khi xuất xml.
- kiểm tra các **quy tắc xử lý lỗi** đã thống nhất: logging, retry, báo cáo lỗi.
- chuẩn bị các **tình huống test** giả định, ví dụ: tạo promotion thiếu trường, payload sai, network fail…

## 5. ghi nhận & đề xuất

- ghi ra các **vấn đề tiềm ẩn** khi sync data sang rk7.
- đề xuất các **bổ sung hoặc điều chỉnh** trước khi dev viết api.


# luồng code xử lý saledatataskscheduleservices

## 1. chức năng tổng quát

đây là một **background service** chạy ngầm.
nhiệm vụ: **mỗi 10 giây kiểm tra xem có task nào tới giờ chạy chưa**, nếu tới thì thực thi và cập nhật lịch chạy tiếp theo.

---

## 2. vòng đời hoạt động

1. service chạy.
2. cứ mỗi **10 giây** → gọi `doaction()`.
3. `doaction()` lấy danh sách các “action” hợp lệ từ database.
4. với mỗi action: kiểm tra **đúng thời điểm chạy** chưa (dựa trên schedule).
5. nếu đúng giờ → thực thi action tương ứng.
6. cập nhật lại thời điểm chạy tiếp theo.

---

## 3. các loại action

chỉ có 2 loại chính:

- **verifyglobalshift** → gọi dịch vụ xác thực ca (verify())
- **exportsaledata** → xuất file xml: saletransaction + saleeod

---

## 4. cách kiểm tra “đúng giờ chạy”

dựa theo loại schedule:

- **immediately** → chạy ngay.
- **daily** → chạy mỗi ngày vào giờ quy định.
- **weekly** → chạy đúng thứ + đúng giờ.
- **monthly** → chạy đúng ngày trong tháng.
- **periodically** → chạy mỗi x phút.

hoặc nếu **đã tới nexttime** → được chạy ngay.

---

## 5. sau khi chạy xong

action được cập nhật:

- `lasttime` = thời điểm chạy hiện tại
- `nexttime` = thời điểm chạy kế tiếp (tính theo schedule)

---

## 6. tinh thần 20/80 của cả hệ thống

- 20% quan trọng:
  – kiểm lịch
  – thực thi action
  – cập nhật lịch chạy

- 80% còn lại:
  – tính toán ngày giờ
  – lấy service từ di
  – lọc dữ liệu
  – log lỗi

---

## 7. hình dung đơn giản

service này giống **một con bot báo thức**.
cứ 10 giây nó mở mắt, xem “đã tới giờ làm nhiệm vụ x chưa”.
đúng giờ → nó làm.
làm xong → ghi lại “lần sau đánh thức lúc mấy giờ”.
rồi lại ngủ.

