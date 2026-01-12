## vấn đề thường gặp: po hỏi tiến độ nhưng kỳ vọng đầu ra không rõ

### bối cảnh

dev báo dự kiến hoàn thành trong **2 ngày**.
đến lúc po hỏi tiến độ, câu hỏi thực sự không phải "xong chưa" mà là:

> **xong ở mức nào, xem được ở đâu, để ai verify?**

nếu không làm rõ, rất dễ:

- dev nghĩ là xong technical
- po nghĩ là đã business-ready
  → lệch kỳ vọng, áp lực ngược, đánh giá sai năng lực.

---

### biểu hiện thường thấy

- po hỏi: *"đã có gì để xem chưa?"*
- dev lúng túng: *"em làm gần xong rồi…"*
- không ai nói rõ **môi trường**, **mức độ hoàn thiện**, **tiêu chí done**

đây là lỗi **giao tiếp delivery**, không phải lỗi code.

---

### nguyên nhân gốc

- không chốt **definition of done** ngay từ đầu
- không phân biệt rõ:

  * technical completion
  * demo flow
  * business-ready
- dev ngại hỏi, sợ bị xem là chưa hiểu việc

---

### cách khắc phục (chuẩn senior dev)

trước hoặc khi bị hỏi tiến độ, **chủ động làm rõ kỳ vọng** bằng câu hỏi định hướng:

> confirm giúp em đầu ra của mốc này nhé:
> mình cần xem kết quả ở mức **demo flow trên môi trường nào** (local / dev / staging),
> hay cần **data thật để business verify**?

hoặc:

> để tránh lệch kỳ vọng, mốc này mình xem là **technical completion**
> hay **business-ready trên môi trường test**?

---

### nguyên tắc áp dụng

- không nói % hoàn thành → nói **giá trị nhìn thấy được**
- luôn gắn tiến độ với:

  * môi trường
  * mức độ hoàn thiện
  * ai là người verify
- nếu po chưa rõ → dev **chủ động đóng khung phạm vi delivery**

---

### câu chốt bảo vệ dev

> ok, vậy em sẽ deliver theo mức **demo core flow trên dev**,
> các phần chưa cover em sẽ note rõ trong báo cáo.

---

### kết luận ngắn gọn

- po hỏi tiến độ ≠ hỏi code xong chưa
- senior dev không đoán kỳ vọng, **senior dev chốt kỳ vọng**
- làm rõ sớm 1 câu → tránh 10 câu giải thích về sau

tài liệu này dùng để:

- onboarding dev mới
- nhắc lại chuẩn giao tiếp delivery trong team
- bảo vệ cả dev lẫn po khỏi hiểu lầm không đáng có

---

##  cách hỏi đúng tư cách senior dev (giọng bình tĩnh – chủ động – ngang hàng)

không hỏi kiểu:

- "anh muốn em làm tới đâu ạ?" ❌
- "em chưa rõ anh cần gì…" ❌

hỏi kiểu:

- **tôi đang chủ động kiểm soát delivery**

### mẫu hỏi gọn – chuẩn – có lực

**phiên bản 1: rất chuẩn mực, an toàn trong môi trường công ty**

> anh cho em confirm kỳ vọng đầu ra của task này nhé:
> trong 2 ngày, anh muốn xem kết quả ở mức **demo luồng trên môi trường nào** (local / dev / staging),
> hay là cần **đầy đủ log – data – case chạy thực tế** để po verify?

**phiên bản 2: senior hơn, có dẫn hướng**

> hiện tại em đang implement theo hướng hoàn thành core flow và verify trên môi trường dev.
> anh confirm giúp em: mình cần **demo hành vi hệ thống** hay **đã đủ data thật để business check** trong mốc này?

**phiên bản 3: khi po hay soi tiến độ**

> để tránh lệch kỳ vọng, em muốn chốt rõ:
> mốc 2 ngày này mình xem là **technical completion** hay **business-ready trên môi trường test**?

### vì sao câu hỏi này thể hiện seniority

- không đổ lỗi
- không xin chỉ đạo chi tiết
- nói bằng ngôn ngữ **delivery, môi trường, giá trị kiểm chứng**
- đặt po vào vai quyết định, không phải dev đoán mò

### tuyệt đối tránh

- báo "xong 80%" mà không nói xong cái gì
- nói "đã làm gần xong" nhưng không gắn với môi trường
- im lặng rồi chờ po hỏi (đây là junior smell)

### câu chốt nếu po vẫn mơ hồ

> ok, vậy em sẽ deliver theo mức **demo core flow trên dev**,
> các phần business verify em sẽ note rõ những gì chưa cover trong mốc này.

đây là câu **đóng khung kỳ vọng**, bảo vệ bạn rất tốt về sau.

nói ngắn gọn thế này thôi.
senior dev không nói nhiều, nhưng mỗi câu đều khóa được rủi ro.

