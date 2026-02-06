## timeline di sản code rule → cách áp dụng / thực hành

### 1970s – "structured programming"

- mục tiêu: loại bỏ flow rối → giảm bug logic
- áp dụng:

  - thay "goto" → "if/for/while/function"
  - tách logic dài > 30 dòng → function riêng
- thực hành:

  - mỗi khi đọc code phải trace được luồng chạy từ trên xuống trong ≤ 10 giây
  - nếu cần nhảy nhiều tầng mới hiểu → refactor

---

### 1980s – "encapsulation"

- mục tiêu: bảo vệ state → tránh sửa sai lan hệ thống
- áp dụng:

  - không expose field mutable trực tiếp
  - mọi thay đổi state đi qua method
- thực hành:

  - nếu object có invariant → bắt buộc viết method validate trước khi set
  - phát hiện code dạng "object.property =" → xem xét khóa lại

---

### 1980s – "single responsibility principle"

- mục tiêu: giảm sửa dây chuyền
- áp dụng:

  - 1 module chỉ xử lý 1 domain concern
- thực hành:

  - nếu class/service chứa >1 động từ domain khác nhau → tách
  - nếu sửa 1 feature khiến test nhiều module fail → sai srp

---

### 1990s – "design pattern"

- mục tiêu: chuẩn hóa cách giải bài toán lặp lại
- áp dụng:

  - dùng "factory" khi khởi tạo object phụ thuộc điều kiện
  - dùng "observer/pubsub" khi nhiều module cần react data change
- thực hành:

  - nếu thấy nhiều "if type ==" → cân nhắc factory
  - nếu module gọi trực tiếp nhiều module khác → cân nhắc event/pubsub

---

### 2000s – "clean code"

- mục tiêu: tối ưu đọc hiểu → giảm cognitive load
- áp dụng:

  - function ≤ 20 dòng
  - tên biến phải chứa domain meaning
- thực hành:

  - đọc tên function phải đoán được output
  - nếu cần comment để giải thích logic → đổi tên hoặc tách function

---

### 2000s – "solid – dependency inversion"

- mục tiêu: giảm coupling → dễ thay thế implementation
- áp dụng:

  - module cấp cao không phụ thuộc module cấp thấp
  - phụ thuộc qua interface/contract
- thực hành:

  - nếu service new trực tiếp dependency → chuyển sang inject interface
  - nếu test phải mock quá nhiều concrete class → sai dependency inversion

---

### 2010s – "loose coupling / api contract"

- mục tiêu: tránh cascade failure giữa service
- áp dụng:

  - giao tiếp qua api/schema rõ ràng
  - không share database giữa service
- thực hành:

  - mỗi service version api riêng
  - thay đổi schema → phải backward compatible hoặc version mới

---

### 2010s – "idempotency"

- mục tiêu: retry an toàn → không tạo side effect lặp
- áp dụng:

  - api create/update phải support idempotency key
- thực hành:

  - mọi api liên quan tiền/giao dịch → lưu request id + trạng thái xử lý
  - test scenario retry 3 lần phải ra cùng kết quả

---

### 2010s – "12 factor app"

- mục tiêu: chuẩn hóa deploy cloud
- áp dụng:

  - config qua env
  - service stateless
- thực hành:

  - không hardcode config
  - service restart không mất state runtime

---

### 2015+ – "testing pyramid"

- mục tiêu: tối ưu chi phí phát hiện bug
- áp dụng:

  - ưu tiên unit test business logic
- thực hành:

  - viết unit test cho mọi function có branch logic
  - e2e test chỉ cover critical flow

---

### 2015+ – "observability"

- mục tiêu: debug production nhanh
- áp dụng:

  - log + metric + tracing
- thực hành:

  - mỗi request có trace id
  - log phải trả lời được: "ai gọi, khi nào, dữ liệu gì, kết quả gì"

---

### meta rule – "dry"

- mục tiêu: tránh duplication logic
- áp dụng:

  - logic domain chỉ tồn tại 1 nơi
- thực hành:

  - phát hiện copy logic ≥ 2 lần → tạo shared module

---

### meta rule – "kiss"

- mục tiêu: giảm complexity không cần thiết
- áp dụng:

  - chọn giải pháp đơn giản nhất thỏa requirement
- thực hành:

  - nếu solution cần diagram dài để giải thích → thử phương án đơn giản hơn

---

### meta rule – "yagni"

- mục tiêu: tránh over-engineer
- áp dụng:

  - chỉ build khi requirement xuất hiện
- thực hành:

  - nếu feature chưa có usecase thực → không abstract hóa trước


## dòng tiến hóa tổng thể

- structured programming → kiểm soát luồng
- oop → kiểm soát state + abstraction
- design pattern → tái sử dụng giải pháp
- clean code + solid → kiểm soát complexity
- microservice + cloud → kiểm soát scale
- devops + testing → kiểm soát reliability
- meta rule → kiểm soát ego dev
---

## thứ tự ưu tiên áp dụng thực tế (80/20)

- "clean code + srp"
- "dependency inversion"
- "testing pyramid"
- "loose coupling + api contract"
- "idempotency"
- "observability"
- "design pattern"
- "12 factor"
- "meta rule (dry/kiss/yagni)"

---

## checklist thực hành nhanh mỗi khi viết code

- "module này có >1 lý do để thay đổi không?"
- "dependency có thể thay thế bằng interface không?"
- "logic này có bị lặp ở nơi khác không?"
- "retry request có gây side effect không?"
- "log hiện tại đủ debug production chưa?"
- "có đang giải bài toán chưa tồn tại không?"