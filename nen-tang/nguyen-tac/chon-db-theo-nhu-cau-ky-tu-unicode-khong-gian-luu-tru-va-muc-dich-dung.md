## 1. tư duy gốc (cái này quyết định đi nhanh hay đi lạc)

db **không chỉ là nơi lưu dữ liệu**.
nó là:

* cách **đóng gói ký tự**
* cách **tính byte**
* cách **đánh đổi giữa dung lượng – tốc độ – tính linh hoạt**

chọn sai db = sửa bằng mồ hôi + downtime + chửi thề.

---

## 2. bản đồ nhanh các hệ db phổ biến (20/80)

### mysql / mariadb

**dùng khi:** web/app phổ thông, startup, crud nhiều, cần dễ scale ngang.

**ký tự & lưu trữ**

* unicode qua `utf8mb4`
* 1 ký tự: 1–4 byte
* giới hạn row ~65kb
* text lưu ngoài row

**ưu**

* dễ dùng, phổ biến
* utf8mb4 xử lý tốt tiếng việt + emoji
* hiệu năng ổn cho read-heavy

**nhược**

* dễ dính bẫy charset nếu không hiểu
* index bị ảnh hưởng bởi byte

**phù hợp**

* saas, cms, pos, e-commerce
* hệ thống cần triển khai nhanh, đội dev vừa

---

### postgresql

**dùng khi:** cần chuẩn mực, dữ liệu phức tạp, lâu dài.

**ký tự & lưu trữ**

* utf-8 là mặc định
* text gần như “không giới hạn” logic
* ít bẫy charset

**ưu**

* unicode rất chuẩn
* index, query planner thông minh
* jsonb, full-text search mạnh

**nhược**

* học dốc hơn mysql
* tune không khéo là chậm

**phù hợp**

* fintech, data-heavy, hệ thống sống lâu
* dự án cần độ đúng hơn độ nhanh lúc đầu

---

### sql server

**dùng khi:** hệ sinh thái microsoft, doanh nghiệp lớn.

**ký tự & lưu trữ**

* unicode qua `nvarchar` (utf-16)
* 1 ký tự thường = 2 byte
* emoji = surrogate pair (4 byte)

**ưu**

* tách bạch unicode rõ ràng
* tooling mạnh, enterprise-grade

**nhược**

* dung lượng tốn hơn utf-8
* license

**phù hợp**

* erp, hệ thống nội bộ doanh nghiệp
* team .net thuần

---

### mongodb (nosql)

**dùng khi:** dữ liệu linh hoạt, schema thay đổi nhanh.

**ký tự & lưu trữ**

* utf-8
* document giới hạn 16mb

**ưu**

* không đau đầu schema
* lưu text đa ngôn ngữ dễ

**nhược**

* index text tốn ram
* không hợp transaction phức tạp

**phù hợp**

* log, cms, content, event data
* prototype nhanh

---

### redis

**dùng khi:** tốc độ, cache, ephemeral data.

**ký tự & lưu trữ**

* binary-safe (byte gì cũng lưu)
* tất cả nằm trong ram

**ưu**

* rất nhanh
* không quan tâm unicode hay không

**nhược**

* không phải nơi lưu text lâu dài
* ram đắt

**phù hợp**

* cache, session, rate limit
* không phải db chính

---

## 3. bảng “chọn db cho đúng việc” (đi thẳng)

| mục đích                  | db nên dùng     |
| ------------------------- | --------------- |
| web/app crud, tiếng việt  | mysql (utf8mb4) |
| dữ liệu phức tạp, lâu dài | postgresql      |
| hệ microsoft              | sql server      |
| nội dung linh hoạt        | mongodb         |
| cache, tốc độ             | redis           |

---

## 4. nguyên tắc đi nhanh – đi trước (đắt giá)

1. **chọn db theo cách nó lưu chữ**, không theo cảm tính
2. **unicode phải rõ ràng từ ngày đầu**
3. **đừng tối ưu sớm bằng loại db bạn chưa hiểu**
4. db sai → code giỏi mấy cũng chữa cháy

---

## 5. một câu chốt để nhớ lâu

> db không ngu,
> nó chỉ làm đúng thứ nó được thiết kế.
> ngu là mình khi bắt nó làm việc không phải của nó.

bạn đang hỏi đúng loại câu hỏi của người **muốn đi trước**, không phải người chỉ muốn “chạy cho xong sprint”. nếu muốn bước tiếp, có thể đào sâu theo hướng:

* chọn db cho **saas từ 0 → 1**
* hoặc **khi nào nên migrate db và khi nào đừng đụng vào**

mấy ngã rẽ này quyết định tốc độ của bạn trong vài năm, không phải vài tháng.
