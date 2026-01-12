## mục tiêu

* chia sơ đồ thành **3 tầng rõ ràng**
* mỗi tầng là **1 cụm logic độc lập**
* decision chỉ rẽ nhánh *ngắn*, không kéo dây lòng thòng
* retry / error gom về cạnh phải, không chọc vào flow chính

---

## 1. bố cục đề xuất (rất quan trọng)

### tầng 1 – entry & validation (ít thay đổi)

* start
* sync
* organization check

→ tầng này gần như **ổn định lâu dài**

### tầng 2 – discount handling (hay đổi)

* discount tồn tại?
* update / delete / create

→ đây là nơi bạn sửa nhiều nhất → cần gọn, phẳng

### tầng 3 – external api & sync result (hay fail)

* discount type
* api calls
* retry / success

→ gom api sang **1 cột riêng**

---

## 2. code mermaid bố cục “sống khỏe” (khuyến nghị dùng)

bạn có thể copy nguyên khối này làm **template chuẩn**.

```mermaid
---
config:
  layout: dagre
---
flowchart TB

%% ========== entry ==========
on(( )) --> start["muốn tạo mới promotion"]
start --> sync["kích hoạt sync promotion"]:::Aqua

%% ========== organization ==========
sync --> org["lọc organization theo tên + env"]:::Pine
org --> org_ok{"organization tồn tại?"}:::Peach
org_ok -- không --> err_org["báo error & kết thúc"]:::Rose
org_ok -- có --> dis

note_org["mỗi môi trường có organization id riêng<br/>(dev / stag / prod)"]:::Peach
org -.-> note_org

%% ========== discount ==========
dis["lấy discount theo tên"] --> dis_ok{"discount tồn tại?"}:::Peach

dis_ok -- không --> create_dis
dis_ok -- có --> del{"discount phải xóa?"}:::Peach

del -- không --> update["cập nhật discount"]
del -- có --> create_dis["tạo mới discount"]

%% ========== discount type ==========
create_dis --> dtype["lấy discount type theo tên + sapcode"]
dtype --> dtype_ok{"discount type tồn tại?"}:::Peach

dtype_ok -- có --> dtype_info["lấy thông tin discount type"]
dtype_ok -- không --> api_dtype["api: tạo discount type"]:::Sky

api_dtype --> api_dtype_ok{"api tạo discount type ok?"}:::Peach
api_dtype_ok -- không --> retry_type["error & retry"]:::Rose
api_dtype_ok -- có --> dtype_info

%% ========== create discount ==========
dtype_info --> api_dis["api: tạo discount"]:::Sky
api_dis --> api_dis_ok{"api tạo discount ok?"}:::Peach
api_dis_ok -- không --> retry_dis["error & retry"]:::Rose
api_dis_ok -- có --> done["xác nhận đồng bộ thành công"]

done --> off(( ))

%% ========== styles ==========
classDef Sky stroke:#374D7C, fill:#E2EBFF, color:#374D7C
classDef Aqua stroke:#46EDC8, fill:#DEFFF8, color:#378E7A
classDef Pine stroke:#254336, fill:#27654A, color:#FFFFFF
classDef Rose stroke:#FF5978, fill:#FFDFE5, color:#8E2236
classDef Peach stroke:#FBB35A, fill:#FFEFDB, color:#8F632D
```

---

## 3. vì sao bố cục này sửa rất nhanh

* thêm rule mới cho discount
  → chỉ đụng **tầng 2**, không ảnh hưởng api
* đổi logic discount type
  → chỉ đụng **tầng 3**
* thêm env / org logic
  → chỉ đụng **tầng 1**
* retry / error
  → luôn nằm **bên phải**, không phá flow chính

não dev đọc theo chiều:

> vào → kiểm tra → xử lý → gọi api → kết quả

không zigzag, không xoắn dây.

---

## 4. nguyên tắc dùng lâu (rất đáng nhớ)

* mỗi decision **chỉ hỏi 1 câu**
* mỗi block **chỉ làm 1 việc**
* api luôn có prefix `api:`
* error luôn màu đỏ, nằm ngoài luồng chính

làm đúng 4 điều này, sơ đồ của bạn sẽ **không bao giờ nát**, kể cả sau 20 lần sửa.

---

nếu bạn muốn bước tiếp:

* tôi có thể **tách sơ đồ này thành 3 file** (entry / domain / integration)
* hoặc viết **version “async + retry queue”** cho skytransfer

đây đã là level “diagram dùng như code”, không phải vẽ cho có.
