# mermaid flowchart — ví dụ sync promotion cơ bản

## mục tiêu
- biến flow thử nghiệm rối → flow chuẩn dev đọc nhanh
- giữ nguyên logic, loại bỏ nhiễu hình thức
- dùng lại cho các flow sync tương tự

---

## những gì bị loại
- shape đặc thù (f-circ, fr-circ) → không ảnh hưởng quyết định
- nối nhiều node trên 1 dòng (`&`) → khó đọc / khó sửa
- class rải rác không theo nhóm logic
- note gắn trực tiếp vào decision

---

## những gì được giữ
- entry / process / decision / api / error / note
- luồng top → bottom
- error + retry đẩy sang phải
- note giải thích rule môi trường

---

## flow logic rút gọn (thứ tự quyết định)

- vào flow → sync promotion
- xác định organization theo env
- nếu không có organization → dừng
- kiểm tra discount tồn tại
- nếu tồn tại → quyết định xóa hay cập nhật
- nếu chưa tồn tại → tạo mới
- đảm bảo discount type tồn tại
- tạo discount qua api
- xác nhận sync thành công

---

## mẫu mermaid chuẩn (copy dùng lại)

```mermaid
flowchart TB

%% ===== entry =====
on(( )) --> start["muốn tạo mới promotion"]
start --> sync["kích hoạt sync promotion"]:::Aqua

%% ===== organization =====
sync --> org["lọc organization theo tên + env"]:::Pine
org --> org_ok{"organization tồn tại?"}:::Peach
org_ok -- không --> err_org["error: không có organization"]:::Rose
org_ok -- có --> dis

note_org["mỗi môi trường có organization id riêng"]:::Peach
org -.-> note_org

%% ===== discount =====
dis["lấy discount theo tên"] --> dis_ok{"discount tồn tại?"}:::Peach
dis_ok -- không --> create_dis
dis_ok -- có --> del{"discount phải xóa?"}:::Peach

del -- không --> update["cập nhật discount"]
del -- có --> create_dis["tạo mới discount"]

%% ===== discount type =====
create_dis --> dtype["lấy discount type theo tên + sapcode"]
dtype --> dtype_ok{"discount type tồn tại?"}:::Peach

dtype_ok -- có --> dtype_info["lấy thông tin discount type"]
dtype_ok -- không --> api_dtype["api: tạo discount type"]:::Sky

api_dtype --> api_dtype_ok{"api ok?"}:::Peach
api_dtype_ok -- không --> retry_type["error & retry"]:::Rose
api_dtype_ok -- có --> dtype_info

%% ===== create discount =====
dtype_info --> api_dis["api: tạo discount"]:::Sky
api_dis --> api_dis_ok{"api ok?"}:::Peach
api_dis_ok -- không --> retry_dis["error & retry"]:::Rose
api_dis_ok -- có --> done["xác nhận đồng bộ thành công"]

done --> off(( ))

%% ===== styles =====
note_org@{ shape: card}
classDef Sky fill:#e2ebff,stroke:#374d7c,color:#374d7c
classDef Aqua fill:#defff8,stroke:#46edc8,color:#378e7a
classDef Pine fill:#27654a,stroke:#254336,color:#ffffff
classDef Rose fill:#ffdfeb,stroke:#ff4d4f,color:#8e2236
classDef Peach fill:#fffbe6,stroke:#faad14,color:#8f632d
