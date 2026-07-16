nỗi đau thực sự của gs25 vietnam ẩn dưới mô tả công việc:

## 1. điểm nghẽn hệ thống (technical bottlenecks)

* **xung đột công nghệ cũ – mới:** vừa duy trì hệ thống bán hàng cũ (legacy winforms / .net framework / c++), vừa tích hợp dịch vụ mới (nodejs, react, microservices).
* **tắc nghẽn dữ liệu bán lẻ (high-traffic & concurrency):** hệ thống nghẽn ca peak (khuyến mãi, lễ tết). sql quá tải, thiếu tối ưu caching (redis) và hàng đợi (kafka/rabbitmq) dẫn đến treo giao dịch.
* **đồng bộ tồn kho – thanh toán real-time:** sai lệch dữ liệu giữa cửa hàng vật lý và ứng dụng online/api đối tác.

---

## 2. điểm nghẽn vận hành (operational pains)

* **thiếu chuẩn hóa quy trình:** hệ thống thiếu ci/cd, thiếu công cụ logging/monitoring; sự cố phát sinh phải tìm vết thủ công.
* **khoảng trống nhân lực (senior leadership):** thiếu người duyệt mã (code review), dẫn đến chất lượng mã kém, nợ kỹ thuật (technical debt) chồng chất. lập trình viên trẻ thiếu định hướng.

---

## 3. ứng viên mid/senior cần tháo gỡ

* **thực tế:** **cứu hỏa sự cố nghẽn mạng**, **đập đi xây lại module cũ**, và **xử lý bài toán nhất quán dữ liệu (data consistency)** trên toàn chuỗi bán lẻ.