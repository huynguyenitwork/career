# tài liệu: hiểu luồng code

*(dùng để onboard dev mới & giúp pm/po hình dung phạm vi xử lý)*

## 1. mục tiêu tài liệu

– giúp người mới hiểu nhanh request đi đâu, ai xử lý, tạo ra response như thế nào.
– cho thấy rõ phạm vi ảnh hưởng: controller – service – database – external service.
– đơn giản hóa giống quy trình "giao hàng – ký nhận – hoàn thành hoặc lỗi".

---

## 2. bức tranh 20% giúp hiểu 80% hệ thống

trong bất kỳ ứng dụng backend nào, request luôn đi theo 4 chặng chính:

1. **client gửi yêu cầu** (giống khách đặt hàng).
2. **controller nhận & định tuyến** (giống bộ phận nhận đơn).
3. **service xử lý logic** (giống kho trung tâm xử lý đơn).
4. **repository/database lưu & đọc dữ liệu** (giống kho hàng thật).

từ đó hệ thống trả về **response**: thành công hoặc thất bại (giống ký nhận hay báo lỗi).

---

## 3. luồng vận hành "giao hàng" của request → response

### 3.1 request xuất phát

client gửi request → controller nhận
**bạn chỉ cần nắm:** endpoint nào, payload gồm gì.
*→ đây là nhãn dán trên kiện hàng.*

---

### 3.2 controller xử lý sơ bộ

– map request → model
– gọi đúng service
*→ giống nhân viên nhập đơn vào hệ thống.*

---

### 3.3 service xử lý lõi (quan trọng nhất – 80% logic nằm ở đây)

service làm ba việc chính:

1. **validate** (đơn hợp lệ không?)
2. **business logic** (tính toán, quyết định)
3. gọi repository / external api

*→ giống kho kiểm tra đơn, phân loại, quyết định xuất kho hay trả lại.*

---

### 3.4 repository/database

– select data
– insert/update state
*→ giống việc quét mã đơn để lưu trạng thái.*

---

### 3.5 response quay về client

có 2 kết quả:

1. **thành công:** trả data, trạng thái ok
2. **lỗi:** trả code lỗi + message, log lại

*→ giống khách ký nhận hoặc shipper báo thất bại.*

---

## 4. phạm vi ảnh hưởng (impact scope) nhìn nhanh

### controller:

– ảnh hưởng routing
– ảnh hưởng validate đơn giản
– không nên chứa logic nặng

### service:

– ảnh hưởng toàn bộ logic nghiệp vụ
– là nơi thay đổi -> chức năng thay đổi
– chiếm 80% suy nghĩ khi debug

### repository/db:

– ảnh hưởng dữ liệu thực tế
– cần đúng query, tránh deadlock, tránh update sai

### external services:

– ảnh hưởng phụ thuộc hệ thống khác
– cần timeout, retry, fallback

*→ chỉ cần nhìn 4 vùng này là hiểu một tính năng "đụng vào đâu".*

---

## 5. sơ đồ 20/80 cho dev/pm dễ nhìn

```
client
  ↓
controller
  - nhận request
  - map model
  ↓
service
  - validate
  - business logic
  - gọi repository/external
      ↓
      repository → database
      - select
      - insert/update
      ↑
  - build response
  ↓
response → client (success/error)
```

---

## 6. tiêu chuẩn vẽ nhanh một luồng code 20/80

dù dùng activity diagram hay sequence diagram, chỉ cần bảo đảm 4 điểm:

1. request → controller
2. controller → service (logic chính nằm đây)
3. service → db/external
4. service → response

không vẽ chi tiết hàm, không vẽ vòng lặp, không vẽ mọi field.
chỉ vẽ cái giúp nhìn là hiểu.

---

## 7. kết luận 20/80

chỉ cần nắm 4 điểm: **controller – service – repository – response** là bạn hiểu 80% luồng của bất kỳ hệ thống backend nào.

dev mới nhìn vào thấy được flow.
dev senior xem vào biết điểm nóng.
pm/po đọc vào nắm được phạm vi ảnh hưởng để estimate.

luồng code lúc này như một phiếu giao hàng điện tử: rõ ràng đường đi, nơi chịu trách nhiệm, và điều gì xảy ra khi lỗi.

---

nếu bạn muốn, mình có thể tạo thêm **một phiên bản chuyên cho dev senior** hoặc **một phiên bản chuyên cho pm/po** — mỗi bên có cách ghi chú khác nhau để đọc nhanh mà không nhầm phạm vi.
