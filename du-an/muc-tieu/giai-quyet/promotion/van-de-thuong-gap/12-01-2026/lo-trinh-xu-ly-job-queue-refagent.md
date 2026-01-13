# lộ trình xử lý job queue refagent

mục tiêu:
- đọc 1 phút là hiểu
- giải thích cho người không đọc code vẫn nắm được
- xuất phát từ quy trình 5 bước có sẵn: 1.QueueWorker[ExecuteAsync-ProcessQueueAsync] => 2.IQueueMessageHandler[ProcessMessageAsync] => 3.ISetRefDataProcessor[ProcessAsync] => 4.BaseActNameHandler[ExecuteAsync] => 5.SaveMenuItemHandler[ExecuteCoreAsync]
---

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

5. **save menu item handler**  
   là người làm việc thật.  
   xử lý nghiệp vụ create/update/delete và trả kết quả.

---

## tóm gọn bằng một dòng

job được **lấy ra → phân loại → điều phối → chạy quy trình chung → xử lý nghiệp vụ**.

một câu chuyện ngắn

- queueworker: mở kho, lấy đơn
- queuemessagehandler: đọc nhãn đơn
- setrefdataprocessor: phân luồng công việc
- baseactnamehandler: áp quy trình chung
- savemenuitemhandler: thợ làm việc thật

---

## ghi nhớ nhanh

- queue chỉ lấy việc, không làm việc
- handler cuối mới là nơi quyết định đúng sai
- mỗi tầng làm đúng một nhiệm vụ

hiểu lộ trình này là debug nhanh hơn rất nhiều và không bị rối hệ thống.
