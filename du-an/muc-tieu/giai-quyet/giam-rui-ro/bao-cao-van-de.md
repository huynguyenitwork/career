## vấn đề về queue

### 23-12-2025
TODO

### 18-12-2025
**Anh Tính ơi,**
em có test luồng đồng bộ từ **ecom → skytransfer** thì thấy có một điểm cần **ghi nhận lại** để theo dõi thêm.

Cụ thể:

* Với **1 request** của **cùng một loại đồng bộ** (ví dụ store) thì hệ thống xử lý ổn.
* Khi có **nhiều request cùng loại đồng bộ gửi gần nhau**, phần **skytransfer tiếp nhận và xếp lịch xử lý** hiện tại có dấu hiệu **xử lý hàng đợi chưa đúng kỳ vọng** (tức là khi hoàn thành 1 request thì các request sau không chạy).

Hiện tại:

* **Dữ liệu test vẫn cho kết quả đúng**, chưa gây lỗi dữ liệu hay ảnh hưởng business.
* Em đề xuất **log lại vấn đề này**, chưa cần can thiệp xử lý ngay, để ưu tiên các đầu việc khác trước.

Sau khi xong phase hiện tại, mình có thể **review lại cơ chế queue / scheduling** của skytransfer cho các case nhiều request cùng loại.
