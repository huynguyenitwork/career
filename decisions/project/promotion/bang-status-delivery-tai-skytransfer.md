## timeline (chỉ giữ mốc ảnh hưởng triển khai)

- [18-01-2026] chốt bảng status delivery tại skytransfer
- [18-01-2026] chốt contract request/response giữa service
- [18-01-2026] chốt phân định upstream – core – downstream cho discount group

---

## bảng status delivery tại skytransfer

### nguyên tắc dùng status

- status = tiến độ delivery, không phải nghiệp vụ
- 1 nguồn set status duy nhất: skytransfer
- status dùng cho: tracking, retry, vận hành
- status không dùng cho: quyết định discount

### status giữ lại (đủ dùng)

| status_code | dùng để làm gì              | loại bỏ ngay       |
|-------------|-----------------------------|--------------------|
| received    | xác nhận đã nhận request    | chi tiết nghiệp vụ |
| validated   | chặn lỗi format sớm         | validate business  |
| rejected    | trả lỗi sớm cho ecom        | retry tự động      |
| grouped     | đảm bảo contract group_code | lookup group       |
| queued      | kiểm soát lưu lượng         | xử lý logic        |
| sent        | biết đã forward core        | biết kết quả       |
| processing  | theo dõi đang xử lý         | suy diễn           |
| success     | kết thúc luồng              | chi tiết nội bộ    |
| failed      | trigger retry/alert         | sửa nghiệp vụ      |
| retrying    | ổn định hệ                  | retry vô hạn       |
| timeout     | cảnh báo sla                | đoán kết quả       |
| canceled    | dừng thủ công               | tự động hủy        |

### quy tắc chuyển (rút gọn đủ chạy)

- received → validated | format ok
- received → rejected | format fail
- validated → grouped | gắn group_code xong
- grouped → queued | enqueue ok
- queued → sent | call skycrm ok
- sent → processing | chưa có kết quả
- processing → success | core ok
- processing → failed | core fail
- failed → retrying | còn retry
- retrying → sent | retry ok
- processing → timeout | quá sla
- any → canceled | manual

### việc cần làm ngay

- chốt enum status_code
- gắn sla cho processing

---

## request / response giữa service (chỉ giữ contract)

### vai trò theo service

| service     | bắt buộc nhận         | bắt buộc gửi           | không được làm |
|-------------|-----------------------|------------------------|----------------|
| ecom        | discount thuần        | discount → skytransfer | biết group     |
| skytransfer | discount thuần        | discount + group_code  | business logic |
| skycrm      | discount + group_code | payload chuẩn          | lan logic      |
| refagent    | payload chuẩn         | payload rk7            | nghiệp vụ      |
| rk7         | payload rk7           | kết quả                | suy diễn group |

### contract cần khóa

- ecom → skytransfer:
  - có: discount data
  - không: group_id, group_code
- skytransfer → skycrm:
  - có: discount + group_code
  - không: business decision
- skycrm → refagent:
  - có: payload chuẩn
  - không: group_code
- refagent → rk7:
  - có: payload rk7
  - không: khái niệm group

### kết luận nhanh

- chỉ cần ổn định 1 schema:
  - skytransfer → skycrm
- nghiệp vụ đổi:
  - chỉ sửa skycrm

---

## phân định upstream – core – downstream

### mục tiêu thiết kế

- khóa toàn bộ discount/group tại skycrm
- upstream chỉ điều phối
- downstream thuần adapter / hệ đích
- đổi ít, ổn định lâu

### trách nhiệm rõ ràng

#### ecom

- gửi discount thuần
- không biết group

#### skytransfer (upstream)

- entry point
- gắn group_code kỹ thuật
- validate format
- quản lý checklist + status
- không lookup group
- không xử lý nghiệp vụ

#### skycrm (core)

- nguồn sự thật duy nhất
- lookup group_code → group
- xử lý create/update/delete:
  - discount
  - discount group
- giữ toàn bộ business logic

#### refagent

- adapter chuyển đổi
- không có logic group

#### rk7 (downstream)

- hệ đích
- nhận dữ liệu đã chuẩn hóa

---

## group_code (chốt để khỏi lan nhiễu)

- group_code = khóa kỹ thuật
- không mang ý nghĩa nghiệp vụ
- gắn tại skytransfer
- lookup chỉ ở skycrm
- contract bất biến skytransfer → skycrm

---

## xử lý c/u/d

- tất cả create/update/delete:
  - discount
  - discount group
- chỉ ở skycrm
- skytransfer không phân biệt hành động
- skytransfer chỉ theo dõi tiến độ

---

## sketch luồng tối giản

- ecom → skytransfer → skycrm → refagent → rk7

---

## kết luận cuối

- skytransfer = điều phối + giám sát
- skycrm = core nghiệp vụ duy nhất
- group_code = chìa khóa kỹ thuật
- thiết kế này: ít sửa, ít lan, dễ giữ ổn định
