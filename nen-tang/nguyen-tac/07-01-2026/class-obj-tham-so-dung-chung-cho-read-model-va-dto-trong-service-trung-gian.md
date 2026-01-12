## vấn đề thường gặp: class tham số dùng chung cho read model và dto trong service trung gian

### 1. bối cảnh

trong **service trung gian**, thường gặp tình huống:

- có `discountview` (read model)
- có `discountupdatedto` (write model)
- **một số field phức tạp** được tách ra thành class riêng để dùng chung
  ví dụ:

  * `discountrulemodel`
  * `selectlistitem`

các class này:

- không phải entity
- không thuần read hay write
- chỉ đóng vai trò **thành phần cấu thành dữ liệu**

---

### 2. vấn đề nảy sinh

khi tách các class dùng chung này ra riêng, câu hỏi xuất hiện:

> "đặt tên nhóm / file cho mấy class này là gì để không hiểu nhầm vai trò?"

đặt sai tên dễ gây hiểu nhầm rằng:

- đây là domain model
- hoặc chỉ dành cho dto
- hoặc chỉ dùng cho response

---

### 3. bản chất của các class dùng chung

các class như `discountrulemodel`, `selectlistitem` thực chất là:

- **data structure trung gian**
- dùng để compose model lớn hơn
- không chứa logic nghiệp vụ
- có thể xuất hiện ở cả request và response

vì vậy, chúng **không thuộc read hay write riêng lẻ**.

---

### 4. cách đặt tên phù hợp (khuyến nghị)

#### khuyến nghị số 1

```
discountsharedmodels.cs
```

ý nghĩa:

- **"shared"** nói rõ: dùng chung
- **"models"** giữ tính trung tính
- đúng bản chất service trung gian

bên trong:

```
discountrulemodel
selectlistitem
```

---

### 5. các lựa chọn hợp lý khác

- `discountcommonmodels.cs`
  nhấn mạnh dùng chung trong feature

- `discountcomponents.cs`
  coi các class này là thành phần cấu tạo

- `discountprimitives.cs`
  dùng khi class rất nhỏ, thiên về cấu trúc dữ liệu

---

### 6. những cách nên tránh

- `discountentity.cs` → sai bản chất
- `discountdto.cs` → hiểu nhầm chỉ dùng cho write
- `discountviewmodels.cs` → loại bỏ write

---

### 7. kết luận

đối với **class tham số dùng chung cho cả read model và dto** trong service trung gian:

- hãy xem chúng là **shared data components**
- đặt tên file **trung tính + thể hiện tính dùng chung**
- tách biệt rõ khỏi entity và model chính

**`discountsharedmodels.cs`** là lựa chọn an toàn, dễ hiểu, ít tranh cãi, sống khỏe lâu dài.

giữ được cách gọi đúng ngay từ đầu thì sau này:

- thêm api không bối rối
- team mới vào đọc là hiểu
- kiến trúc không bị "trôi khái niệm" theo thời gian
