## timeline (chỉ giữ mốc ảnh hưởng quyết định)

- [19-01-2026] chốt thói quen đặt tên sớm khi phát triển api
- [18-01-2026] chốt mapping object cho flow ecom → skytransfer → skycrm → refagent → rk7
- [18-01-2026] chốt chuẩn đặt tên object api dùng chung toàn hệ

---

## thói quen đặt tên sớm (giữ cái làm được việc)

- chạy trước, đẹp sau, đúng cuối
  - dùng để: ép giá trị xuất hiện sớm
- tạo bản nháp chạy end-to-end
  - dùng để: kiểm chứng hướng đi
- mỗi vòng chỉ 1 tiêu chí sống còn
  - dùng để: tránh tê liệt quyết định
- tạo và đánh giá tách thời điểm
  - dùng để: não không tự triệt tiêu
- đo bằng hành vi thực, không cảm giác
  - dùng để: loại chủ quan
- viết với giả định sẽ xóa
  - dùng để: giảm gắn bó
- dừng ngay khi đã chạy
  - dùng để: giữ nhịp triển khai

---

## nguyên tắc phát triển api (rút gọn để áp dụng)

- vòng 1: chỉ cần chạy đúng luồng
- vòng 2: đúng logic
- vòng 3: dễ đọc
- vòng 4: chuẩn hóa
- mỗi vòng chỉ làm 1 việc
- không refactor khi chưa có flow chạy thật
- hoàn thiện dồn về lúc merge
- checklist xấu: ghi lại, không sửa ngay
- kết thúc buổi làm việc bằng câu hỏi:
  - "đã chạy chưa?"

---

## kết luận dùng ngay cho đặt tên object

- mỗi boundary = object riêng
- không reuse object xuyên boundary
- nhìn suffix là biết vai trò
- object không đổi suffix khi qua tầng = sai

---

## mapping object theo flow ecom → rk7 (đủ dùng)

| đoạn | from → to               | loại object         |
|------|-------------------------|---------------------|
| 1    | ecom → skytransfer      | RequestDto          |
| 2    | skytransfer internal    | Command             |
| 3    | skycrm → refagent / rk7 | IntegrationCommand  |
| 4    | refagent / rk7 → skycrm | IntegrationResponse |
| 5    | skytransfer → ecom      | Response            |

---

## rule nhanh theo service

### ecom

- chỉ dùng RequestDto
- không reuse

### skytransfer

- inbound: RequestDto
- internal: Command
- outbound: IntegrationCommand
- callback: IntegrationResponse
- response http: Response

loại:
- trả IntegrationResponse ra ngoài
- dùng Command làm response

### skycrm

- inbound: IntegrationCommand
- internal: Command
- outbound: IntegrationCommand
- callback: IntegrationResponse
- không dùng dto

### refagent

- inbound và outbound khác tên
- chỉ adapter, không nghiệp vụ

### rk7

- inbound IntegrationCommand
- callback IntegrationResponse

---

## rule callback (hay sai)

- callback luôn là response
- callback không dùng command
- callback không reuse http response

---

## rule cây object (cắt mạnh)

### write side

- cấp 1–2: Command
- cấp ≥3:
  - chỉ value object
  - không suffix
  - không verb

loại ngay khi:
- command xuất hiện ở cấp ≥3

### read / callback side

- root: Response / IntegrationResponse
- cấp 2: Result / Summary
- cấp ≥3:
  - view / value
  - không logic

---

## rule tránh trùng tên

- không lặp suffix theo chiều sâu
- không dùng tên generic
- thêm context bằng động từ, không bằng hệ thống

đúng:
- PromotionCreateIntegrationCommand

sai:
- PromotionCommand
- PromotionDto

---

## chuẩn đặt tên api (ngôn ngữ chung)

### suffix theo tầng

| tầng                 | suffix                     |
|----------------------|----------------------------|
| http inbound         | RequestDto                 |
| application write    | Command                    |
| application read     | ReadModel / Query          |
| integration outbound | IntegrationCommand         |
| integration inbound  | IntegrationResponse        |
| http response        | Response / SummaryResponse |

---

## rule bất biến

- read ≠ write
- object name phải trả lời:
  - dùng để làm gì
  - ở đâu
- requestdto không vào application
- command không trả thẳng ra http
- response không đi ngược vào application

---

## rule reuse (nguồn lỗi lớn)

- requestdto: không reuse
- command: chỉ reuse cùng use-case
- response: chỉ reuse cùng screen
- integration*: không reuse khác boundary

---

## checklist đổi tên nhanh

- object đang nói chuyện với ai?
- nó ghi hay trả kết quả?
- nó ở boundary nào?
- bỏ suffix đi còn hiểu không?

không trả lời được → đổi tên hoặc đổi cấu trúc

---

## kết luận khóa lại

- đây là rule ngôn ngữ, không phải framework
- ít sáng tạo → ít sai
- nhất quán > thông minh
- object đúng tên → hệ dễ chạy, dễ review, dễ mở rộng
