# các loại sketch nên dùng

## mục tiêu
- chọn đúng kiểu sketch trước khi vẽ
- giảm nhánh, giảm suy nghĩ, quyết định nhanh
- tách rõ flow / rule / decision

---

## nguyên tắc lọc
- cần vẽ nhánh để hiểu → loại
- trộn rule vào flow → loại
- sketch không dùng lại được → loại
- thông tin không ảnh hưởng thiết kế 7–30 ngày → loại

---

## loại sketch nên dùng

### 1. linear flow + checkpoint (mặc định, 80/20)
- flow luôn thẳng
- decision bị nén tại checkpoint
- thêm/bớt bước không phá cấu trúc

- dùng khi:
  - backend flow chuẩn
  - hay thay đổi thứ tự bước
  - cần xương sống ổn định

---

### 2. ensure-based sketch (ưu tiên hệ thống sync)
- tư duy theo trạng thái cần đảm bảo
- mỗi dòng là 1 ý định, không phải nhánh

- đặc điểm:
  - decision ẩn trong ensure
  - error chỉ xuất hiện khi ensure fail
  - logic đọc như code

- dùng khi:
  - sync dữ liệu
  - reconcile state
  - backend idempotent

---

### 3. phase-based sketch (theo giai đoạn)
- chia flow theo pha, không theo nhánh
- mỗi pha gom các bước cùng bản chất

- dùng khi:
  - flow dài
  - nhiều bước validate / dependency
  - cần map sang subgraph

---

### 4. rule-first sketch (tách rule khỏi flow)
- rule đứng riêng
- flow giữ thẳng, không decision

- đặc điểm:
  - rule = constraint
  - flow = thứ tự thực thi

- dùng khi:
  - rule nhiều
  - flow đơn giản
  - cần giữ hình vẽ gọn

---

## combo khuyến nghị
- xương sống: linear flow
- logic chi tiết: ensure-based
- ràng buộc: rule-first

- mục tiêu:
  - sketch nhanh
  - sửa nhanh
  - không cần decision tree

---

# ví dụ minh họa

## ví dụ 1: linear flow + checkpoint
```

start
-> sync
-> checkpoint: organization
-> checkpoint: discount
-> checkpoint: discount group
-> create discount
-> confirm
-> end

```

---

## ví dụ 2: ensure-based
```

ensure organization exists
ensure discount exists or recreated
ensure discount group exists
call create discount api
retry on failure
done

```

---

## ví dụ 3: phase-based
```

phase prepare

* input
* sync trigger

phase validate

* organization
* discount

phase execution

* create discount
* retry

phase finalize

* confirm

```

---

## ví dụ 4: rule-first
```

rules

* organization theo env
* discount group phải có trước discount
* api có retry

flow
start
-> sync
-> organization
-> discount
-> discount group
-> api
-> done

```

---

## kết luận
- sketch để đi nhanh, không để suy nghĩ lâu
- cần decision tree để hiểu → sketch sai
- flow thẳng + rule tách riêng = đủ dùng
