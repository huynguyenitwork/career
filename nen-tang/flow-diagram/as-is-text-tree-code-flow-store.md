# as-is text tree flow code store

```
[START]
└─ Kích hoạt tiến trình
    ├─ Nhận request (job / event / trigger)
    ├─ Kiểm tra quyền chạy ngay (immediate)
    │    ├─ Nếu không → ghi log → [END]
    │    └─ Nếu có → tiếp tục
    └─ Kiểm tra hành động (ImportMasterData)
         ├─ Nếu hành động khác → bỏ qua → [END]
         └─ Nếu đúng → sang bước kiểm tra thay đổi dữ liệu

---------------------------------------------------------
(1) KIỂM TRA STORE CÓ THAY ĐỔI KHÔNG
---------------------------------------------------------
└─ Kiểm tra sự kiện thay đổi dữ liệu store
    ├─ Không thay đổi
    │    └─ Lấy danh sách store từ DB/cache → [END]
    └─ Có thay đổi
         └─ Chuyển sang bước xử lý danh sách store

---------------------------------------------------------
(2) LẤY DANH SÁCH STORE
---------------------------------------------------------
└─ Kiểm tra dữ liệu trong cache ("RestaurantsList")
    ├─ Cache tồn tại
    │    ├─ Lấy danh sách store từ cache
    │    ├─ Lọc & chuẩn hóa dữ liệu
    │    └─ Chuyển sang đồng bộ store vào DB
    └─ Không có cache
         └─ Gọi RK7 API để lấy danh sách store
              ├─ Nhận XML từ RK7
              ├─ Deserialize XML → đối tượng dữ liệu
              ├─ Lọc dữ liệu (loại bỏ field thừa)
              ├─ Cập nhật cache:
              │      ├─ Key: RestaurantsList
              │      └─ TTL: 60 phút
              └─ Chuyển sang đồng bộ store vào DB

---------------------------------------------------------
(3) ĐỒNG BỘ STORE VÀO DATABASE
---------------------------------------------------------
└─ Lặp qua từng store trong danh sách
    ├─ Kiểm tra store tồn tại trong DB
    │
    │  (A) STORE CHƯA TỒN TẠI
    │    ├─ Tạo mới store trong DB
    │    ├─ Áp logic chuyển đổi mã store (generate/convert code)
    │    ├─ Thực hiện insert store
    │    ├─ Cập nhật ProcessStatus = 1 (successful)
    │    └─ Nếu lỗi → ProcessStatus = -1 + ghi log
    │
    │  (B) STORE ĐÃ TỒN TẠI
    │    ├─ Kiểm tra mã store giữa Ecom và RK7
    │    │     ├─ Khác nhau → cập nhật lại
    │    │     └─ Giống nhau → giữ nguyên
    │    ├─ Áp logic update thông tin thay đổi nếu có
    │    ├─ Cập nhật store trong DB
    │    ├─ Cập nhật ProcessStatus = 1
    │    └─ Nếu lỗi → ProcessStatus = -1 + ghi log
    │
    └─ Lặp sang store tiếp theo

---------------------------------------------------------
(4) SAU KHI XỬ LÝ TẤT CẢ STORE
---------------------------------------------------------
└─ Cập nhật cache danh sách store RK7 (nếu được phép)
    ├─ Ghi cache key "RestaurantsList"
    ├─ TTL: 60 phút
    └─ Hoàn tất

└─ Ghi ProcessStatus cuối cùng vào bảng EcomStore
└─ Ghi log tổng hợp

[END]
```

---

# bạn đọc vào sẽ hiểu ngay 3 tầng lớn

- **tầng 1: trigger → xem có thay đổi không**
- **tầng 2: lấy danh sách store (cache hoặc rk7)**
- **tầng 3: đồng bộ vào db (insert/update + processstatus)**

cuối cùng là cleanup + cache.

mọi thứ trong sơ đồ gốc đều có mặt đầy đủ ở đây, nhưng theo kiểu **ngăn nắp – dễ theo dõi – không bị chìm trong những box nhỏ**.

