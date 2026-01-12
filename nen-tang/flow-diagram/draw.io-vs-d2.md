# draw.io vs d2

> tài liệu này giúp phân biệt **diagram truyền thống*- và **diagram hiện đại (diagram as code)*- thông qua hai đại diện tiêu biểu: **draw.io*- và **d2**.
> mục tiêu: hiểu *vì sao chúng sinh ra*, *giải quyết vấn đề gì*, *dùng cho ai*, và *cần gì để thực hành được ngay*.

---

## 1. timeline hình thành

### 1.1. thời đại draw.io (≈ 2010)

#### bối cảnh

- doanh nghiệp bắt đầu số hoá mạnh
- team đông, trình độ không đồng đều
- nhu cầu vẽ sơ đồ để **giải thích – trình bày – thống nhất nhận thức**
- công cụ phổ biến lúc đó: visio (nặng, đắt), powerpoint (thủ công)

#### vấn đề tồn tại

- vẽ sơ đồ tốn thời gian
- khó chia sẻ
- phụ thuộc phần mềm cài đặt
- không phải ai cũng dùng được

#### draw.io ra đời để giải quyết

- vẽ sơ đồ **kéo – thả – trực quan**
- chạy trên web, không cần cài đặt
- miễn phí, mã nguồn mở
- file-based, dễ lưu trữ và chia sẻ

**câu hỏi mà draw.io trả lời:**

> “làm sao để mọi người *nhìn thấy cùng một bức tranh*?”

---

### 1.2. thời đại d2 (≈ 2022)

#### bối cảnh

- hệ thống phần mềm phức tạp: microservices, event-driven, async
- diagram vẽ xong là lỗi thời rất nhanh
- diagram thường nằm ngoài git, không ai maintain
- team kỹ thuật cần sơ đồ để **suy nghĩ và kiểm soát hệ thống**, không chỉ để trình bày

#### vấn đề tồn tại

- diagram đẹp nhưng sai thực tế
- không diff được, không review được
- không gắn với vòng đời code
- diagram chết sau vài sprint

#### d2 ra đời để giải quyết

- diagram được **viết bằng text (diagram as code)**
- có thể version control, review, diff như code
- tạo sơ đồ nhanh, sửa nhanh
- diagram trở thành một artifact kỹ thuật

**câu hỏi mà d2 trả lời:**

> “hệ thống này có thực sự vận hành đúng như ta nghĩ không?”

---

## 2. triết lý cốt lõi

### draw.io

- diagram là **hình ảnh**
- con người là trung tâm
- trực giác > logic hình thức
- phù hợp để **giải thích và trình bày**

### d2

- diagram là **mô hình logic**
- logic là trung tâm
- văn bản > thao tác tay
- phù hợp để **suy nghĩ, thiết kế và duy trì hệ thống**

---

## 3. so sánh nhanh theo tư duy

| khía cạnh             | draw.io       | d2                  |
| --------------------- | ------------- | ------------------- |
| cách tạo              | kéo – thả     | viết text           |
| đối tượng chính       | mọi vai trò   | dev, architect      |
| version control       | không phù hợp | rất phù hợp         |
| độ bền theo thời gian | trung bình    | cao                 |
| tốc độ sửa logic      | chậm          | nhanh               |
| mục đích chính        | giải thích    | suy nghĩ & thiết kế |

---

## 4. dùng cho ai, mục đích gì?

### khi nên dùng draw.io

- thuyết trình, training
- onboarding người mới
- brainstorm nhóm đông
- làm việc với non-tech stakeholder
- khi cần **nhìn là hiểu ngay**

### khi nên dùng d2

- thiết kế hệ thống
- phân tích luồng xử lý
- viết tài liệu kỹ thuật sống cùng code
- review kiến trúc
- khi cần **nghĩ cho đúng và sửa cho nhanh**

---

## 5. điều kiện tối thiểu để thực hành

### thực hành draw.io

- biết các loại sơ đồ cơ bản (flow, box, arrow)
- không cần kiến thức kỹ thuật sâu
- không cần git
- phù hợp cho người mới

### thực hành d2

- text editor
- hiểu cấu trúc hệ thống đang mô tả
- tư duy entity – relationship – flow
- có git là lợi thế lớn

---

## 6. chiến lược sử dụng hiệu quả (20/80)

cách tiếp cận thực tế và bền vững:

- dùng **d2*- để:

  - thiết kế
  - suy nghĩ
  - maintain
  - review

- dùng **draw.io*- để:

  - giải thích
  - thống nhất nhận thức
  - trình bày với người ngoài team kỹ thuật

diagram không phải tôn giáo.
diagram là công cụ.

---

## 7. kết luận

- draw.io đại diện cho **diagram truyền thống – human-first**
- d2 đại diện cho **diagram hiện đại – logic-first**

người làm hệ thống trưởng thành là người:

> **vẽ bằng draw.io khi cần giao tiếp, nhưng suy nghĩ bằng d2 khi cần quyết định.**
