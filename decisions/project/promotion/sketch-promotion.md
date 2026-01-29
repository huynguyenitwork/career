```md
# sketch promotion – chuẩn hệ thống, tối giản

## mục tiêu
- mô tả **ý định xử lý promotion** từ ecom → rk7
- dùng sketch để **đóng băng logic**, không mô tả chi tiết code
- làm nền cho mermaid / plantuml / code

---

## phạm vi
- áp dụng cho luồng thêm / sửa / xóa promotion
- mô hình command-driven, async + callback
- create api **chỉ trả trạng thái**, không trả entity

---

## nguyên tắc loại
- decision tree chi tiết → loại
- mô tả cách code → loại
- lặp rule ở nhiều nơi → gom
- thông tin không ảnh hưởng quyết định xử lý → loại

---

## kiến trúc tổng quát (ý định)
- ecom phát sự kiện promotion
- skytransfer nhận, lưu, điều phối
- skycrm quyết định nghiệp vụ
- refagent / rk7 thực thi
- callback trả kết quả ngược dòng

---

## rules cốt lõi
- sync là command-driven
- organization khác nhau theo env → dùng **id**
- discount group phải tồn tại trước discount
- discount group + discount dùng **code** để đối chiếu
- promotion có 3 eventype: create / update / delete
- api gọi ra ngoài luôn có retry
- trạng thái gởi lên skycloud mặc định là "draft"

---

## trạng thái nghiệp vụ
- parent = discount group
- child = discount
- trạng thái hợp lệ: active / soft-delete / missing

---

## bảng hành vi theo event (chuẩn hóa)
| eventype | parent status | child status | hành động hệ thống              | kết quả |
|----------|---------------|--------------|---------------------------------|---------|
| create   | missing       | missing      | bootstrap create parent → child | done    |
| create   | active        | active       | reject duplicate                | reject  |
| create   | active        | soft-delete  | reject create                   | reject  |
| create   | active        | missing      | create child                    | done    |
| create   | soft-delete   | missing      | reject create child             | reject  |
| update   | missing       | any          | reject update                   | reject  |
| update   | active        | active       | update child                    | done    |
| update   | active        | missing      | reject update                   | reject  |
| update   | active        | soft-delete  | reject update                   | reject  |
| update   | soft-delete   | active       | reject update                   | reject  |
| delete   | active        | missing      | noop hoặc reject (policy)       | reject  |
| delete   | missing       | any          | noop hoặc reject (policy)       | reject  |
| delete   | active        | active       | soft-delete child               | done    |
| delete   | active        | soft-delete  | noop                            | reject  |
| delete   | soft-delete   | active       | noop                            | reject  |

---

## bootstrap rule (ngoại lệ duy nhất)
- chỉ áp dụng khi:
  - parent **chưa từng tồn tại**
  - thuộc luồng setup ban đầu / migration
- cho phép:
  - tạo parent → tạo child
- không áp dụng khi:
  - runtime thông thường
  - parent từng soft-delete

---

## sketch system (ý định – không nhánh)

### flow tổng
```

start
-> receive promotion event
-> validate organization
-> ensure discount group (theo rule)
-> ensure discount (theo eventype)
-> call external api
-> retry if fail
-> callback result
-> end

```

---

## sketch theo pha

### phase 1: intake
- nhận event promotion
- validate payload
- lưu trạng thái received

### phase 2: validate
- validate organization
- xác định eventype

### phase 3: ensure
- ensure discount group
- ensure discount (create/update/delete/skip)

### phase 4: execution
- call api rk7 (direct hoặc qua refagent)
- retry theo policy

### phase 5: finalize
- cập nhật trạng thái promotion ecom
- callback kết quả

---

## sketch dev (chuyển từ system → code)
- system sketch: nói **ý định**
- dev sketch: nói **cách làm**
- system không switch
- dev switch(eventype) để implement

---

## mapping trạng thái promotion ecom
- done  → xử lý thành công
- reject → vi phạm rule nghiệp vụ
- processing → đang xử lý
- failed → lỗi kỹ thuật sau retry

---

## checklist triển khai (tối giản)
- webhook nhận promotion từ ecom
- validate + lưu raw + callbackurl
- background xử lý promotion
- api callback inbound
- log theo requestid
- test happy path + reject path

---

## kết luận
- sketch dùng để **giữ logic thẳng**
- rule đứng riêng, flow không rẽ nhánh
- chỉ bung nhánh khi sang code
- đủ rõ để vẽ mermaid, đủ gọn để sửa nhanh
```
