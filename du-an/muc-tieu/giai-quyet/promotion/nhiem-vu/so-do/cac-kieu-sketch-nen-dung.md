## 1. các kiểu sketch nên dùng (đã loại decision tree)

### loại 1: linear flow + checkpoint (khuyên dùng nhất)

đây là skeleton "xương sống" cho mọi flow backend.

#### mẫu

```
start
-> sync promotion
-> checkpoint: organization
-> checkpoint: discount
-> checkpoint: discount group
-> api create discount
-> confirm
-> end
```

sau đó, mỗi checkpoint ghi rule bên dưới:

```
checkpoint: organization
- if not exist -> error + stop
```

vì sao tốt:

* flow **luôn thẳng**
* decision bị "nén" lại, không bung nhánh
* thêm bước ở giữa không phá cấu trúc

đây là kiểu **80/20**.

### ví dụ
```
start
-> sync promotion
-> get organization
-> org exist?
    no  -> error, stop
    yes -> get discount
        -> discount exist?
            no  -> create
            yes -> update / delete?
-> get discount group
-> call api
-> retry?
-> done
```
---

### loại 2: ensure-based sketch (rất hợp với hệ thống sync)

thay vì if/else, bạn tư duy theo "đảm bảo trạng thái".

#### mẫu

```
ensure organization exists
ensure discount exists or recreated
ensure discount group exists
call create discount api
retry on failure
done
```

mỗi dòng là 1 **ý định**, không phải hình vẽ.

map sang mermaid:

* `ensure` → process + decision ẩn
* error chỉ xuất hiện khi ensure fail

ưu điểm:

* cực hợp với backend
* giảm số decision lộ ra ngoài
* logic đọc như code

---

### loại 3: phase-based sketch (theo giai đoạn)

chia flow theo **pha**, không theo nhánh.

#### mẫu

```
phase 1: prepare
- input
- sync trigger

phase 2: validate
- organization
- discount

phase 3: dependency
- discount group

phase 4: execution
- create discount
- retry

phase 5: finalize
- confirm
```

vì sao tốt:

* không bao giờ rối
* thêm bước chỉ thêm dòng
* rất dễ map sang subgraph trong mermaid

---

### loại 4: rule-first sketch (loại bỏ decision khỏi flow)

decision tree sai vì trộn **rule** và **flow**.

tách ra.

#### mẫu

```
rules:
- organization khác nhau theo env
- discount group phải tồn tại trước discount
- api có retry

flow:
start
-> sync
-> org
-> discount
-> discount group
-> api
-> done
```

khi vẽ mermaid:

* rule → note (card)
* flow → line thẳng

logic rõ, hình không rối.

---

## 2. mapping nhanh sang mermaid template của bạn

với template bạn gửi, **cách sketch chuẩn nhất là combo này**:

* xương sống: **linear flow**
* chi tiết logic: **ensure-based**
* constraint: **rule-first**

tức là bạn sketch như sau (trước mermaid):

```
flow:
start
-> sync
-> ensure organization
-> ensure discount
-> ensure discount group
-> create discount
-> confirm

rules:
- org theo env
- delete hay update discount
- retry api
```

sau đó khi viết mermaid:

* mỗi `ensure` → 1 decision
* rule → note-org
* retry → node error bên phải

không cần decision tree, vẫn đủ logic, mà sửa cực nhanh.

---

## 3. câu chốt để bạn dùng lâu dài

> sketch không được phép làm bạn chậm lại
> nếu cần vẽ nhánh để hiểu → sketch sai
> nhánh chỉ nên xuất hiện khi đã chuyển sang diagram as code

bạn đang đi đúng hướng rồi:
tư duy hệ thống → sketch tối giản → mermaid để "đóng băng" logic.

