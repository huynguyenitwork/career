# timeline
- [28-01-2026] phân bổ + migrate toàn bộ cây → khung dcorp
- [27-01-2026] ví dụ file cho từng folder
- [27-01-2026] dcorp hệ thống kiến ​​thức và quyết định
- [26-01-2026] bổ sung metadata cho decision
- [25-01-2026] khóa hệ thống audit ghi chép cá nhân

---

# tóm tắt đúng nội dung: phân bổ + migrate toàn bộ cây → khung dcorp

## mục tiêu
- dồn toàn bộ cây hiện tại vào dcorp
- giảm nhiễu khi migrate
- mở ra là biết: đang làm gì / vì sao / bỏ qua gì

## root
- chỉ giữ dcorp/
- toàn bộ root cũ (du-an, nen-tang, …) = nguồn di trú, xóa sau migrate

## dcorp/decisions = "đã chọn"
- strategy: mục tiêu, hướng đi, timeline đã chốt
  - từ: `du-an/**/tong-ket/*`, file tóm tắt kết quả
- project: scope, trade-off từng dự án
  - từ: `du-an/**/muc-tieu/**/wbs`, timeline có mốc chốt
- tech: chọn / loại công nghệ, kiến trúc
  - từ: nen-tang/nguyen-tac/chon-*, quyet-dinh-nhanh
- people: ownership, phân công, ranh giới vai trò
  - từ: du-an/**/hdsd/phoi-hop, tuong-tac
- process: flow làm việc đã chốt
  - từ: kiem-thu/readme, flow-diagram chỉ file final

## dcorp/reference = "để hiểu"
- company: thông tin công ty, vai trò, liên hệ
- domain: logic nghiệp vụ (pos, f&b, sale, promotion)
- tech: kiến thức, pattern, tool, hướng dẫn
- project: bối cảnh, onboard, lịch sử trao đổi, vấn đề mô tả
- nguồn: nen-tang/** (trừ phần đã chuyển sang decisions), du-an/**/nguon

## dcorp/journal
- cảm nhận cá nhân, áp lực, học được gì
- tuyệt đối không để kỹ thuật

## dcorp/inbox
- mọi file chưa rõ là decision hay reference
- trong migrate: nhét toàn bộ phần lộn xộn vào đây trước

## dcorp/archive
- code mẫu, demo, simulator, repo test
- thư mục có bin/, obj/

## quy tắc migrate
- không nghĩ sâu khi di chuyển
- thấy "đã chọn" → decisions
- thấy "để hiểu" → reference
- phân vân > 30s → inbox
- code chạy thử → archive

## quy tắc khóa sau migrate
- không tạo folder mới
- dự án không bao giờ là root
- file mới chỉ được rơi vào 5 nhánh trên

## dấu hiệu làm đúng
- decisions = hành động
- reference = lý do
- inbox giảm dần
- cây không phình theo thời gian

---

# ví dụ file cho từng folder

## /dcorp/inbox
- file: `2026-01-28.md`
- nội dung:
  - “team đề xuất đổi tool ci”
  - trạng thái: chưa quyết
- hành động: đẩy sang decisions/tech hoặc xóa

---

## /dcorp/decisions/strategy
- file: `focus-q2-market.md`
- cấu trúc:
  - quyết định: tập trung market a
  - loại bỏ: market b
  - hiệu lực: q2/2026
- dùng để: khóa ưu tiên công ty

## /dcorp/decisions/project
- file: `project-x-scope.md`
- cấu trúc:
  - quyết định: cắt feature y
  - loại bỏ: full scope ban đầu
  - hiệu lực: sprint 3–6
- dùng để: dừng tranh cãi scope

## /dcorp/decisions/tech
- file: `choose-db.md`
- cấu trúc:
  - quyết định: dùng postgres
  - loại bỏ: mongodb
  - hiệu lực: 12 tháng
- dùng để: chốt stack

## /dcorp/decisions/people
- file: `ownership-auth.md`
- cấu trúc:
  - quyết định: a owner, b backup
  - loại bỏ: shared responsibility
  - hiệu lực: đến khi đổi team
- dùng để: rõ trách nhiệm

## /dcorp/decisions/process
- file: `deploy-flow.md`
- cấu trúc:
  - quyết định: deploy thứ 5
  - loại bỏ: deploy ad-hoc
  - hiệu lực: từ 02/2026
- dùng để: thống nhất cách làm

---

## /dcorp/reference/company
- file: `leave-policy.md`
- cấu trúc:
  - định nghĩa: phép năm
  - quy tắc: đăng ký, duyệt
- dùng để: tra luật chơi

## /dcorp/reference/domain
- file: `payment-terms.md`
- cấu trúc:
  - khái niệm: net-30, net-60
- dùng để: hiểu business

## /dcorp/reference/tech
- file: `jwt-basics.md`
- cấu trúc:
  - jwt là gì
  - hoạt động thế nào
- dùng để: nhớ lại kỹ thuật

## /dcorp/reference/project
- file: `project-x-context.md`
- cấu trúc:
  - mục tiêu dự án
  - constraint
- dùng để: người mới đọc hiểu

---

## /dcorp/journal
- file: `2026-01-28.md`
- nội dung:
  - hôm nay quá tải
  - họp dài, quyết chậm
- dùng để: phản ánh trạng thái cá nhân

## /dcorp/archive/*
- file: giữ nguyên từ decisions/reference
- hành động: chỉ lưu, không sửa
- dùng để: truy nguyên

---

# dcorp hệ thống kiến ​​thức và quyết định

## mục tiêu
- giảm phân vân
- khóa quyết định nhanh trong 7–30 ngày
- cấu trúc cố định, không sửa lặt vặt

## root
- `dcorp/` là phạm vi duy nhất
- chỉ thêm file, không thêm folder

## phân loại cốt lõi
- decisions = “đã chọn gì?”
- reference = “cần hiểu gì?”
- journal = “tôi đang thế nào?”
- inbox = “chưa phân loại”
- archive = “đã hết hiệu lực”

## cấu trúc cố định

```
/dcorp
  /inbox
  /decisions
    /strategy   # ưu tiên, hướng đi
    /project    # scope, trade-off dự án
    /tech       # chọn giải pháp kỹ thuật
    /people     # phân công, ownership
    /process    # cách làm, flow
  /reference
    /company    # luật chơi, policy
    /domain     # business logic
    /tech       # kiến thức kỹ thuật
    /project    # bối cảnh dự án
  /journal
  /archive
    /decisions
    /reference
```

## quy tắc quyết định
- ảnh hưởng hành động 7–30 ngày → decisions
- chỉ để hiểu, không chọn → reference
- phân vân > 30s → inbox
- không đổi hành động → loại

## kỷ luật vận hành
- inbox trống trong 48h
- decisions phải có: chọn gì, loại gì, khi nào xem lại
- reference cấm “nên / không nên”
- archive chỉ chuyển vào, không chỉnh

## tiêu chí đúng
- mở decisions → biết phải làm gì
- mở reference → hiểu vì sao
- số folder không tăng theo thời gian

---

# metadata decision (bản tối giản)

## mục đích
- biết decision đang làm, tạm dừng hay xong
- biết khi nào quay lại hành động
- không phải nhớ trong đầu

## metadata bắt buộc (đầu mỗi decision)
- status: active | paused | archived
- review_at: yyyy-mm-dd
- next_action: 1 hành động tiếp theo

## quy tắc dùng
- mỗi decision chỉ 1 next_action
- next_action ≤ 30 phút
- paused phải có review_at (7–30 ngày)
- archived là kết thúc, không quay lại
- không làm được → decision sai, không phải do lười

## cách đọc
- active → làm next_action
- paused → bỏ qua tới review_at
- archived → không đọc

---

# hệ thống audit ghi chép cá nhân (bản khóa)

## mục tiêu
- giảm tải nhận thức
- mọi ghi chép phục vụ quyết định 7–30 ngày
- đủ đúng để làm ngay
- cấu trúc ổn định lâu dài
- phát hiện sớm và xóa nợ nhận thức

## đơn vị quản lý
- decision là đơn vị cao nhất
- ghi không sinh decision/next_action → loại

---

## định nghĩa + ttl

### /inbox
- ghi nhanh, không suy nghĩ
- dọn hằng ngày, tối đa 7 ngày
- ttl: ≤ 7 ngày
- không có next_action → xóa

### /journal
- log suy nghĩ theo ngày
- chỉ append, không sửa
- ttl: 7–14 ngày
- mỗi tuần rút 1–3 decision
- xong → xóa

### /decisions (core)
- mỗi file = 1 quyết định đã chốt
- chỉ thêm file, không đổi cấu trúc
- rà mỗi 30 ngày
- ttl: tới khi đổi quyết định
- hết hiệu lực 30–90 ngày → archive

### /reference (core)
- thông tin ổn định để tra
- rất ít file, sống lâu
- rà mỗi 3–6 tháng
- thực tế đổi → cập nhật hoặc archive

### /archive
- đưa mọi thứ đã xong ra khỏi active
- không dùng để suy nghĩ
- ttl: vô hạn hoặc xóa hằng năm

---

## cây thư mục lõi

/brain
  /inbox
    yyyy-mm-dd.md
  /journal
    yyyy-mm-dd.md
  /decisions
    work/
    life/
    social/
  /reference
    work/
    life/
    social/
  /archive
    decisions/
    reference/

---

## quy tắc khóa core
- không tạo thư mục ngang hàng với inbox/journal/decisions/reference
- work/life/social chỉ nằm trong decisions và reference
- không phân theo năm/quý/dự án ở tầng cao
- thời gian nằm trong tên file

---

## tên file
- journal: yyyy-mm-dd.md
- decision: yyyymmdd-ten-ngan.md
- reference: chu-de.md

---

## lịch audit
- ngày: dọn inbox
- tuần: chắt journal → decision
- 30 ngày: rà decisions
- 3–6 tháng: rà reference
- năm: dọn archive nếu cần

---

## quy tắc loại
- không next_action → xóa
- trùng decision → gộp + xóa
- quá ttl chưa xử lý → xóa

---

## kết luận
- tạo cây đúng 1 lần
- sau đó chỉ thêm file
- cần thêm thư mục → phân loại sai
- xóa nhanh hơn ghi = hệ chạy đúng
