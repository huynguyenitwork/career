# mermaid flowchart — ví dụ sync promotion bố cục 3 tầng

## mục tiêu sử dụng
- chia flow thành 3 tầng độc lập để sửa nhanh
- decision ngắn, không kéo dây
- retry / error tách khỏi flow chính
- đọc theo 1 chiều, không zigzag

---

## phạm vi giữ lại (20/80)
- chia tầng logic
- flow top → bottom
- decision 1 câu / 2 nhánh
- api + retry gom cột phải
- style nhất quán

ngoài phạm vi này: **loại**

---

## bố cục chuẩn 3 tầng (cố định)

### tầng 1 — entry & validation
- start
- sync
- organization check
→ ổn định, ít thay đổi

### tầng 2 — domain handling
- discount tồn tại?
- update / delete / create
→ hay đổi, cần phẳng và gọn

### tầng 3 — external api & result
- discount type
- api calls
- retry / success
→ dễ fail, gom riêng

---

## quy ước bất di bất dịch
- luồng chính: trên → dưới
- decision: hỏi đúng 1 điều kiện
- error / retry: đẩy sang phải
- note: chỉ giải thích rule
- api: prefix `api:`

---

## template mermaid chuẩn (copy dùng luôn)

```mermaid
flowchart TB

%% ===== tầng 1: entry & validation =====
on(( )) --> start["muốn tạo mới promotion"]
start --> sync["kích hoạt sync promotion"]:::Aqua

sync --> org["lọc organization theo tên + env"]:::Pine
org --> org_ok{"organization tồn tại?"}:::Peach
org_ok -- không --> err_org["error: không có organization"]:::Rose
org_ok -- có --> dis

note_org["mỗi môi trường có organization id riêng"]:::Peach
org -.-> note_org

%% ===== tầng 2: discount handling =====
dis["lấy discount theo tên"] --> dis_ok{"discount tồn tại?"}:::Peach

dis_ok -- không --> create_dis
dis_ok -- có --> del{"discount phải xóa?"}:::Peach

del -- không --> update["cập nhật discount"]
del -- có --> create_dis["tạo mới discount"]

%% ===== tầng 3: external api & result =====
create_dis --> dtype["lấy discount type theo tên + sapcode"]
dtype --> dtype_ok{"discount type tồn tại?"}:::Peach

dtype_ok -- có --> dtype_info["lấy thông tin discount type"]
dtype_ok -- không --> api_dtype["api: tạo discount type"]:::Sky

api_dtype --> api_dtype_ok{"api ok?"}:::Peach
api_dtype_ok -- không --> retry_type["error & retry"]:::Rose
api_dtype_ok -- có --> dtype_info

dtype_info --> api_dis["api: tạo discount"]:::Sky
api_dis --> api_dis_ok{"api ok?"}:::Peach
api_dis_ok -- không --> retry_dis["error & retry"]:::Rose
api_dis_ok -- có --> done["xác nhận đồng bộ thành công"]

done --> off(( ))

%% ===== styles =====
classDef Sky fill:#e2ebff,stroke:#374d7c,color:#374d7c
classDef Aqua fill:#defff8,stroke:#46edc8,color:#378e7a
classDef Pine fill:#27654a,stroke:#254336,color:#ffffff
classDef Rose fill:#ffdfeb,stroke:#ff4d4f,color:#8e2236
classDef Peach fill:#fffbe6,stroke:#faad14,color:#8f632d
