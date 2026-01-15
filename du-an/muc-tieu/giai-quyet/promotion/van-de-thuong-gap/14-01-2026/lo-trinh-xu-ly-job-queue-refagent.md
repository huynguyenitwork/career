# lộ trình xử lý job queue refagent

mục tiêu:
- đọc 1 phút là hiểu
- giải thích cho người không đọc code vẫn nắm được
- xuất phát từ quy trình 5 bước có sẵn: 1.QueueWorker[ExecuteAsync-ProcessQueueAsync] => 2.IQueueMessageHandler[ProcessMessageAsync] 
=> 3.1.ISetRefDataProcessor[ProcessAsync] => 4.BaseActNameHandler[ExecuteAsync] => 5.SaveDiscountHandler[ExecuteCoreAsync]
=> 3.2.IQueueMessageHandler[CallbackAsync]
---
## timeline
- 13-01-2026: bổ sung thêm callback api url từ gateway sau xử lý job
- 12-01-2026: luồng xử lý 5 bước của job

## luồng xử lý thực tế

1. **queueworker**  
   là người trực hàng chờ.  
   thấy có job mới thì lấy ra, không xử lý nội dung.

2. **queue message handler**  
   là người mở phong bì.  
   đọc job thuộc loại gì, rồi chuyển tiếp cho đúng luồng xử lý.

3. **set ref data processor**  
   là người điều phối.  
   dựa vào actname để quyết định handler nào sẽ làm việc.

4. **base act name handler**  
   là quy trình chung.  
   chuẩn bị trước khi xử lý: log, validate, bắt lỗi chung.

5. **save discount handler**  
   là người làm việc thật.  
   xử lý nghiệp vụ create/update/delete và trả kết quả.
   
6. **callback mechanism**  
   là người báo tin về.  
   sau khi xử lý xong (success hoặc fail hết retry), gọi callback về gateway để thông báo kết quả.  
   retry 3 lần với exponential backoff nếu callback fail.
---

## tóm gọn bằng một dòng

job được **lấy ra → phân loại → điều phối → chạy quy trình chung → xử lý nghiệp vụ**.

một câu chuyện ngắn

- queueworker: mở kho, lấy đơn
- queuemessagehandler: đọc nhãn đơn
- setrefdataprocessor: phân luồng công việc
- baseactnamehandler: áp quy trình chung
- savemenuitemhandler: thợ làm việc thật
- callback: shipper báo kết quả về cho khách

---

## ghi nhớ nhanh

- queue chỉ lấy việc, không làm việc
- handler cuối mới là nơi quyết định đúng sai
- callback đảm bảo kết quả được báo về đúng chỗ
- mỗi tầng làm đúng một nhiệm vụ

hiểu lộ trình này là debug nhanh hơn rất nhiều và không bị rối hệ thống.
