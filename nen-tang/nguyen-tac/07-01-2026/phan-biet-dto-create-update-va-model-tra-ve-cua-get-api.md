## phân biệt dto (create/update) và model trả về của get api

### 1. bối cảnh

trong thiết kế restful api, **create / update** và **get** phục vụ **hai mục đích khác nhau**:

- create / update → ghi dữ liệu
- get → đọc và hiển thị dữ liệu

vì khác mục đích, **không nên dùng chung một model** cho cả hai chiều.

---

### 2. dto là gì? (write model)

**dto (data transfer object)** dùng cho **đầu vào** của api ghi dữ liệu.

đặc điểm:

- phục vụ validate dữ liệu
- phản ánh rule nghiệp vụ
- không nhất thiết chứa đầy đủ field của entity
- có thể thay đổi theo từng hành động (create / update)

ví dụ:

```
creatediscountdto
updatediscountdto
```

=> dto = để ghi, không phải để đọc.

---

### 3. get api trả về cái gì? (read model)

get api trả về **representation của dữ liệu để client đọc**, không phải dto.

đặc điểm:

- tập trung vào dữ liệu hiển thị
- có thể bao gồm field tổng hợp, join, computed
- không bị ràng buộc bởi rule ghi dữ liệu

về bản chất:
**đây là read model / response model / view model**.

---

### 4. cách đặt tên (suffix khuyến nghị)

tùy mức độ hệ thống, chọn một trong các cách sau:

#### phổ biến, dễ hiểu

```
xxxresponse
```

ví dụ:

```
discountresponse
userresponse
```

#### hướng hiển thị, phù hợp ui phức tạp

```
xxxview
xxxviewmodel
```

#### hệ thống lớn, tách read / write rõ ràng

```
xxxreadmodel
```

không nên dùng chung suffix `dto` cho get api.

---

### 5. những sai lầm cần tránh

- dùng `createdto` / `updatedto` làm response
- trả thẳng `entity` ra ngoài api
- dùng một class `xxxdt o` cho cả get/post/put

những cách này khiến:

- api khó mở rộng
- logic rối
- thay đổi một phía ảnh hưởng phía còn lại

---

### 6. kết luận

- **dto**: chỉ dùng cho **create / update** (ghi)
- **get api**: dùng **response / view / read model** (đọc)
- đọc và ghi là hai chiều khác nhau → **tách model là đúng bản chất**

giữ nguyên tắc này từ sớm sẽ giúp api:

- rõ ràng
- dễ maintain
- ít hiểu sai giữa backend – frontend – po
