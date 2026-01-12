# hướng dẫn sử dụng d2 với cli + vs code

> mục tiêu: dùng **diagram as code** đúng chất dev, có gui để nhìn – có cli để chuẩn hoá – không lệ thuộc cloud – không tốn tiền.

---

## 1. d2 là gì (nhắc lại ngắn gọn cho đúng ngữ cảnh)

d2 là công cụ **vẽ sơ đồ bằng code** (diagram as code).

* diagram được mô tả bằng file text `.d2`
* render bằng cli thành `svg / png / pdf`
* phù hợp với git, ci/cd, tài liệu kỹ thuật

nguyên tắc cốt lõi:

> **diagram là source code, hình ảnh chỉ là artifact**

---

## 2. cài đặt d2 cli

### 2.1. cài trên macos

```bash
brew install d2
```

### 2.2. cài trên linux / windows

* tải binary từ github release của d2
* giải nén và thêm vào `path`

kiểm tra:

```bash
d2 --version
```

nếu thấy version → ok.

---

## 3. setup vs code làm gui cho d2

### 3.1. cài vs code extension

tìm và cài extension:

* **d2** (syntax highlight)

extension này giúp:

* highlight cú pháp
* đọc code dễ hơn
* ít lỗi ngớ ngẩn

---

### 3.2. cấu trúc thư mục khuyến nghị

```text
repo/
├─ diagrams/
│  ├─ system-context.d2
│  ├─ architecture.d2
│  └─ flows.d2
├─ diagrams-rendered/
│  ├─ system-context.svg
│  ├─ architecture.svg
│  └─ flows.svg
└─ readme.md
```

* `.d2` là **nguồn chân lý**
* `.svg` là output để đọc / share

---

## 4. viết diagram d2 cơ bản

ví dụ tối giản:

```d2
user -> api
api -> database
```

ví dụ có label:

```d2
user -> api: request
api -> database: query
database -> api: result
api -> user: response
```

bạn **không cần căn chỉnh**, d2 tự lo layout.

---

## 5. render diagram bằng cli

### 5.1. render thủ công

```bash
d2 architecture.d2 architecture.svg
```

hữu ích khi:

* chuẩn bị commit
* build tài liệu

---

### 5.2. live preview với `--watch`

đây là phần tạo cảm giác "có gui":

```bash
d2 --watch architecture.d2 architecture.svg
```

cơ chế:

* mỗi lần bạn lưu file `.d2`
* svg tự render lại

mở file svg bằng:

* browser
* hoặc vs code svg preview

👉 trải nghiệm gần như live preview.

---

## 6. workflow chuẩn khi làm việc hằng ngày

1. mở `.d2` trong vs code
2. mở terminal → chạy `d2 --watch`
3. vừa gõ code vừa xem svg
4. khi ổn → commit cả `.d2` và `.svg`

nguyên tắc:

* review **code diagram**, không review hình
* hình chỉ để đọc

---

## 7. tích hợp vào readme / tài liệu

ví dụ trong `readme.md`:

```md
## system architecture

![architecture](diagrams-rendered/architecture.svg)
```

diagram lúc này:

* luôn đồng bộ với code
* không bị lệch version

---

## 8. khi nào cần gui mạnh hơn?

cli + vs code là đủ cho:

* dev
* technical docs
* architecture discussion

chỉ cần gui cao cấp (d2 studio) khi:

* demo trực tiếp
* dạy người không quen code
* muốn drag-drop

không bắt buộc.

---

## 9. tư duy dùng d2 cho đúng

* đừng vẽ mọi thứ
* chỉ vẽ **quan hệ quan trọng**
* diagram để **giảm tải trí nhớ**, không để trang trí

> diagram tốt là diagram giúp bạn **nghĩ ít hơn**.

---

## 10. tổng kết nhanh

* d2 cli: engine miễn phí, ổn định
* vs code: gui đủ dùng
* `.d2` là source of truth
* svg là artifact

bạn đang dùng diagram theo cách của developer, không phải designer.
