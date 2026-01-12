### hỏi đáp
Hi anh @B, em nhờ anh hỗ trợ thông tin liên quan đến **Promotion & SkyOffice** ạ.

Hiện tại em đang làm **đồng bộ promotion từ eCommerce sang POS** để POS áp dụng khuyến mãi giống eCom. Để làm đúng thì **master data + rule + logic validate/tính toán promotion** đều cần lưu/lấy từ **SkyOffice**.

Vì vậy, em cần **setup SkyOffice trên môi trường local** để tìm hiểu cấu trúc dữ liệu và flow xử lý promotion trước khi tích hợp chính thức.

Nhờ anh hỗ trợ giúp em:

- Source code SkyOffice (ưu tiên phần promotion)
- Thông tin DB/schema + sample data (nếu có)
- Hướng dẫn cấu hình ban đầu để chạy SkyOffice local và test promotion

Mục tiêu là để em **hiểu đúng logic promotion gốc**, để tích hợp POS cho chuẩn, tránh sai lệch so với eCommerce.

Cảm ơn anh hỗ trợ giúp em

### yêu cầu / bối cảnh vấn đề

hiện tại, tôi cần **đồng bộ dữ liệu promotion từ hệ thống ecommerce sang máy pos** để có thể áp dụng các chương trình khuyến mãi trực tiếp tại điểm bán.

để pos có thể:

* lấy **master data** của promotion
* hiểu và áp dụng **rule / điều kiện**
* thực hiện **validate & tính toán promotion chính xác**

thì **nguồn dữ liệu và logic tính toán bắt buộc phải lấy từ skycrm**, vì skycrm đang đóng vai trò là nơi quản lý và xử lý promotion trung tâm.

---

### vấn đề cốt lõi

ở thời điểm hiện tại, tôi **chưa thể tích hợp trực tiếp** do:

* chưa nắm rõ cấu trúc promotion trong skycrm
* chưa hiểu đầy đủ flow xử lý rule / validate / calculate
* chưa có môi trường để thử nghiệm độc lập

muốn làm nhanh – đúng – không mò trong bóng tối, thì **cần một môi trường skycrm chạy local**.

---

### mục tiêu

thiết lập **skycrm local environment** nhằm:

* nghiên cứu cấu trúc promotion (data + logic)
* thử nghiệm tích hợp promotion từ skycrm → pos
* đảm bảo pos áp dụng promotion **đúng như ecommerce**

---

### yêu cầu hỗ trợ cụ thể

tôi cần được cung cấp:

* **source code skycrm** (phần liên quan đến promotion)
* **database schema / sample data** cho promotion
* **hướng dẫn cấu hình ban đầu** để:

  * chạy được skycrm trên máy local
  * sử dụng và test được chức năng promotion

---

### kết luận ngắn gọn

không setup skycrm local → không hiểu promotion tận gốc → tích hợp pos chỉ là đoán mò.
setup được → nhìn thấy logic thật → tích hợp nhanh, đúng, và tự tin triển khai.

