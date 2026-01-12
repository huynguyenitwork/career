## yêu cầu bổ sung
1. mã code từ ecom đẩy sang lưu trường "genecomcode" (bổ sung trường này trên extended rk7) vì rk7 không cần lưu code
2. bổ sung thêm thời gian áp dụng ngày bắt đầu/ngày kết thúc gởi sang skycrm (nếu có)
3. bổ sung tên loại ưu đãi mở trên skycrm => api tạo discount mở sau khi gởi tới skycrm thêm loại ưu đãi mới này
4. thêm tham số storesselection vào api tạo discount (giả lập dữ liệu đã có các store sẵn)

## mục tiêu của tài liệu

tài liệu này dùng để **demo nhanh cho po** ở giai đoạn *dựng thô* dựa trên **bdd**.
không bàn sâu kỹ thuật, không soi edge case.
chỉ tập trung một việc: **luồng create discount chạy end-to-end được**.

triết lý xuyên suốt:

> chạy được quan trọng hơn chạy đẹp.

---

## phạm vi demo

- chỉ demo **happy path**
- chỉ demo **event create discount**
- không demo rollback, retry, concurrent, validate phức tạp
- dữ liệu có thể mock / seed / fake

luồng chung:

ecom -> api -> service -> db -> skycloud -> response

---

## định nghĩa nhanh (để po dễ nắm)

- **discount**: chương trình giảm giá
- **discount group**: nhóm chứa discount
- trạng thái dữ liệu:

  * *mới*: chưa tồn tại trong db
  * *tồn tại*: có trong db, is_deleted = false
  * *đã xóa*: có trong db, is_deleted = true

---

## bảng tổng hợp các case demo
hiện trạng:
- discount đã xóa => tạo mới
- discount group đã xóa => restore (ảnh hưởng bởi discount đã tồn tại)

| case | status discount | status discount group | hành vi hệ thống                     | kỳ vọng demo        |
| ---- | --------------- | --------------------- | ------------------------------------ | ------------------- |
| 1    | mới             | mới                   | tạo mới cả 2                         | chạy full create    |
| 2    | tồn tại         | đã xóa                | restore group                        | discount giữ nguyên |
| 3    | đã xóa          | tồn tại               | **tạo mới discount**                 | group giữ nguyên    |
| 4    | tồn tại         | tồn tại               | skip create                          | trả success         |
| 5    | đã xóa          | đã xóa                | **restore group + tạo mới discount** | chạy full create    |

---

## các bước thực hiện
b1: xóa dữ liệu skycrm/ecom (discount/discountgroup/ecompromotion) đặt cache 3' thành 0 để test
b2: gọi api tạo ecompromotion (case 1)
b3: xóa discount group (trên ui crm), **đặt lại processstatus ecompromotion** | xóa ecompromotion và gọi lại api b2 (case 2)
b4: xóa discount (trên ui crm), **đặt lại processstatus ecompromotion** | xóa ecompromotion và gọi lại api b2 (case 3)
b5: giữ nguyên discount/discount group đã tạo trước đó (trên ui crm), **đặt lại processstatus ecompromotion** | xóa ecompromotion và gọi lại api b2 (case 4)
b6: xóa discount/discount group đã tạo trước đó (trên ui crm), **đặt lại processstatus ecompromotion** | xóa ecompromotion và gọi lại api b2 (case 5)

## chi tiết từng case demo

### case 1: discount [mới], discount group [mới]

**bối cảnh**

- db chưa có discount
- db chưa có discount group

**hành vi hệ thống**

- tạo discount group mới
- tạo discount mới, gán vào group vừa tạo

**demo cho po xem gì**

- api nhận request create
- db có thêm 2 record mới
- response trả success

**điểm nhấn demo**

- đây là case gốc, quan trọng nhất
- chỉ cần chạy được case này là coi như có khung

---

### case 2: discount [tồn tại], discount group [đã xóa]

**bối cảnh**

- discount đã tồn tại, đang active
- discount group tồn tại nhưng is_deleted = true

**hành vi hệ thống**

- restore discount group
- không tạo lại discount

**demo cho po xem gì**

- discount không bị duplicate
- discount group được bật lại

**điểm nhấn demo**

- hệ thống không tạo dư dữ liệu
- thể hiện có xử lý trạng thái xóa mềm

---

### case 3: discount [đã xóa], discount group [tồn tại]

**bối cảnh**

- discount tồn tại nhưng is_deleted = true
- discount group đang active

**hành vi hệ thống**

- **tạo mới discount**
- gắn discount mới vào discount group hiện có

**demo cho po xem gì**

- xuất hiện discount mới trong db
- discount cũ vẫn giữ trạng thái đã xóa (không restore)

**điểm nhấn demo**

- dữ liệu lịch sử được bảo toàn
- logic rõ ràng: đã xóa là coi như vòng đời cũ kết thúc

---

### case 4: discount [tồn tại], discount group [tồn tại]

**bối cảnh**

- cả discount và discount group đều đang active

**hành vi hệ thống**

- không tạo mới
- không restore
- trả kết quả thành công

**demo cho po xem gì**

- hệ thống idempotent (gọi lại không hỏng)
- api vẫn trả success

**điểm nhấn demo**

- gọi nhiều lần không nổ
- po rất thích case này vì nó "ổn định"

---

### case 5: discount [đã xóa], discount group [đã xóa]

**bối cảnh**

- discount tồn tại nhưng is_deleted = true
- discount group tồn tại nhưng is_deleted = true

**hành vi hệ thống**

- restore discount group
- **tạo mới discount** và gắn vào group vừa restore

**demo cho po xem gì**

- discount group được bật lại
- discount mới được tạo
- discount cũ vẫn giữ trạng thái đã xóa

**điểm nhấn demo**

- tách bạch vòng đời dữ liệu
- tránh phục hồi dữ liệu giảm giá đã hết hiệu lực trong quá khứ
