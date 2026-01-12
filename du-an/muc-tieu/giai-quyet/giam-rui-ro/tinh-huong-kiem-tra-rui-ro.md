# chú ý (checklist)
- thiết kế các cơ chế monitoring để đảm bảo dữ liệu luôn đầy đủ – chính xác – đúng hạn
- xây dựng các cơ chế xử lý lỗi & tự hồi phục (auto-healing) nếu xảy ra sự cố trong quá trình truyền dữ liệu giữa 2 hệ thống

# 22-12-2025
## hiểu thêm
– kiểm tra coi xem case 5,6 có bắt buộc cần có hoặc bdd/test/giải pháp thế nào
- thực hiện case timeout-cancel (thử nghiệm với mini project với python/chưa rõ khi nào cần)

## **case 5**: **có dữ liệu nhưng người dùng không thấy** [FAILED – có thể retry]

### các bài test

* bài test 1 – ghi DB thành công, UI không hiển thị
* bài test 2 – backend xử lý xong nhưng cache/index chưa cập nhật
* bài test 3 – retry cùng payload cho đến khi user nhìn thấy

### điều kiện cần

* **user-facing visibility** là điều kiện bắt buộc để kết luận SUCCESS
* ghi DB **không đủ**
* nếu chưa thấy → **FAILED có kiểm soát**
* retry chỉ áp dụng cho FAILED do **timing / eventual consistency**
* bắt buộc xử lý **idempotent** để retry an toàn

### kết quả

#### test 1

* DB ghi thành công
* user không thấy dữ liệu
  → **FAILED (not visible)**
  → cho phép retry

#### test 2

* backend xử lý xong
* cache / search chưa sync
  → **không được đánh SUCCESS**
  → FAILED
  → retry đến khi user thấy

#### test 3

* retry nhiều lần
  → xác nhận:

  * retry là đúng
  * không gây trùng dữ liệu
  * SUCCESS chỉ khi user nhìn thấy

---

## tổng kết case 5

1. **SUCCESS chỉ được kết luận khi user dùng được**
2. **retry dùng để bắc cầu giữa kỹ thuật và trải nghiệm**
3. **không đánh DONE sớm**

---

## **case 6**: **mỗi hệ thống hiểu khác nhau cùng một khái niệm (promotion)** [FAILED – không retry]

### các bài test

* bài test 1 – sender gửi promotion thiếu field hệ nhận cần
* bài test 2 – cùng payload nhưng hệ nhận diễn giải khác
* bài test 3 – retry payload sai semantic

### điều kiện cần

* **semantic contract là bắt buộc**
* sender **phải gửi theo cách hệ nhận vận hành**
* phân biệt rõ:

  * FAILED do **technical** → retry
  * FAILED do **semantic/business** → **không retry**
* không suy đoán, không “hiểu ngầm”
* mapping phải **explicit**, không default mơ hồ

### kết quả

#### test 1

* sender gửi promotion
* hệ nhận thiếu dữ liệu để áp dụng
  → **FAILED (semantic mismatch)**
  → không retry

#### test 2

* sender hiểu promotion là “giảm %”
* receiver hiểu là “mua X tặng Y”
  → xử lý sai nghiệp vụ
  → **FAILED vĩnh viễn**

#### test 3

* retry nhiều lần cùng payload
  → **không cải thiện kết quả**
  → retry bị coi là lãng phí tài nguyên

---

## tổng kết case 6

1. **retry không dùng cho lỗi hiểu sai**
2. **FAILED semantic phải dừng sớm**
3. **đúng dữ liệu quan trọng hơn đúng thời điểm**

–--

# 18-12-2025

## case 4: rủi ro "giao rồi nhưng không ai xác nhận" [FAILED – có thể retry]

### bản chất cần chốt trước (rất quan trọng)

- `PROCESSING` = **đang xử lý**
- `SUCCESS` = **đã có xác nhận từ nơi nhận**
- `FAILED` = **không thể kết luận thành công** (dù đã "giao" về mặt kỹ thuật)

=> **"Giao rồi nhưng không ai xác nhận" = xử lý xong phía gửi, nhưng không có bằng chứng business → FAILED**

không có trạng thái "treo lơ lửng chờ hy vọng".

### các bài test

- bài test 1 – sender gửi xong, không nhận được ack
- bài test 2 – receiver xử lý xong nhưng không callback
- bài test 3 – retry cùng payload khi không có ack

### điều kiện cần

- **ack là điều kiện bắt buộc để kết luận SUCCESS**
- không có ack → **FAILED có kiểm soát**
- retry chỉ chạy trên **FAILED do thiếu xác nhận**
- phân biệt rõ:

  * FAILED do **technical**
  * FAILED do **business**
- bắt buộc có **idempotency key** phía receiver

### kết quả

#### test 1

- sender gửi thành công
- không nhận ack
  → **kết luận FAILED (missing confirmation)**
  → cho phép retry

#### test 2

- receiver xử lý xong nhưng không phản hồi
  → sender **không có quyền suy đoán thành công**
  → FAILED
  → retry có thể gây trùng nếu receiver không idempotent

#### test 3

- retry nhiều lần cùng payload
  → xác nhận:

  * retry là đúng
  * **duplicate risk nằm ở phía receiver**, không phải sender

---

## tổng kết

1. **test 1 chưa đạt khi nhận phản hồi failed chưa đạt chưa có cơ chế retry => [DONE PA dự phòng] với điều kiện (không cập nhật trạng thái xử lý của record là -1[ERROR])**


## người dùng thêm/sửa/xóa cơ bản

### bài test
- bên nhận rk7 đã xóa store, bên gửi ecom gửi lại store trùng với mã store bên rk7 đã xóa
### mong đợi
- tạo mới lại store bên nhận rk7 bên gửi ecom gửi sang, do rk7 đã xóa
### kết quả
- rk7 cập nhật lại store đã xóa

## tổng kết 
chưa đạt: bên nhận rk7 đã xóa store, bên gửi ecom gửi lại store trùng với mã store bên rk7 đã xóa [PENDING]

–--

# 17-12-2025
2 loại test trong bdd

## **case 1**: người dùng làm lại cùng một hành động tạo mới

### bài test
- tạo store cùng 1 mã và bấm 2 lần
- tạo store, xóa trên rk7 và tạo lại cùng 1 store => kết quả thế nào (đây có phải BDD người dùng? kết quả ra sao?)
### kết quả

#### test 1
- tạo store cùng 1 mã thì phía rk7 cập nhật mà không phải tạo mới (theo kết quả anh Đầy ghi nhận)
- tạo store cùng 1 mã thì phía rk7 tạo trung lặp bản ghi (theo kết quả tôi thấy được)
=> **anh Đầy đúng** vấn đề là tôi dùng 2 mã store khác nhau nên thấy trùng lặp thông tin tên/địa chỉ/...
#### test 2
- là trạng thái update. cần cập nhật trạng thái đã xóa (0) => trạng thái đẩy sang (new)

## **case 2**: rủi ro "đến nơi không đúng thứ tự"

### các bài test
- bài test 1 – update khi chưa create
- bài test 2 – disable chạy trước khi create hoàn tất
### điều kiện cần
- lắp thêm camera quan sát giao thông của các hành vi
- bằng việc tạo 1 bảng tạm và store procedure (effort – rủi ro – tốc độ nhìn ra sự thật ít ảnh hưởng business flow, transaction, model / repository)
=> đã hoàn thành

### kết quả

#### test 1
- với phép thử update, create cùng 1 store api chỉ chạy 1 lần => nguyên nhân là sự kiện đánh dấu PlantChanged chỉ 1 lần. mong đợi chạy 2 lần (lỗi)


## tổng kết 
1. test 2 chưa đạt: là trạng thái update. cần cập nhật trạng thái đã xóa (0) => trạng thái đẩy sang (new)
2. **test 1 chưa đạt 2 yêu cầu store, api chỉ chạy 1 lần (giống như bảo vệ trông giữ xe, xử lý xong xe 1 yêu cầu, xong đi đâu đó, xe 2 yêu cầu bị hủy) => [DONE PA dự phòng]**

