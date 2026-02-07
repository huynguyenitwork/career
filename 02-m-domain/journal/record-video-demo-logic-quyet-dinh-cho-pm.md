# mục tiêu

- pm hiểu nhanh logic quyết định + thấy hệ thống an toàn, không cần đọc bảng test case 
- kết quả mong đợi: sau 5–7 phút pm gật đầu "ok logic, pass"
- khung prompt chuẩn để record video demo cho pm

# kịch bản record video demo cho pm
- mục tiêu video: pm hiểu nhanh logic quyết định + thấy hệ thống an toàn, không cần đọc bảng test case
- kết quả mong đợi: sau 5–7 phút pm gật đầu "ok logic, pass"

---

## setup tối thiểu (5 phút chuẩn bị):
  - mở 1 file duy nhất: bảng test case (như ảnh)
  - mở 1 màn hình demo api/ui có log
  - không slide, không kịch bản dài

---

## cấu trúc video (tổng 6–8 phút, quay 1 lần):

### phần 1 – mở đầu (30s)
  - nói: "video này em demo logic xử lý discount theo các case create/update/delete"
  - nói: "mục tiêu là chống trùng, không hồi sinh revive sai, và đồng bộ đúng cho rk7"
  - dừng ở đây, không giải thích thuật ngữ

### phần 2 – khung quyết định (1 phút)
  - chỉ vào bảng
  - nói: "mỗi request được quyết định bởi 3 thứ: trạng thái discount group, trạng thái discount, hành động"
  - nói: "output chỉ có 3 loại: allow, reject, noop"
  - nói: "mọi thứ ngoài quyết định đều không phù hợp (là nhiễu)"

### phần 3 – demo create (2 phút):
  - chọn 3 case đại diện: c1, c2, c5
  - với mỗi case:
    - nói 1 câu duy nhất:
      - c1: "chưa tồn tại gì → cho phép chạy luồng (allow bootstrap) → tạo đầy đủ"
      - c2: "đã active → từ chối trùng lặp (reject duplicate) → hệ thống tự bảo vệ"
      - c5: "discount group đã xóa mềm (soft delete) → từ chối (reject) → không tạo discount mồ côi"
    - bấm request
    - chỉ log dòng quyết định
  - không nói thêm

### phần 4 – demo update (2 phút):
  - chọn 2 case: u3, u1
  - u3:
    - nói: "discount group active → discount active → allow → sync rk7"
    - bấm update, chỉ dữ liệu synced
  - u1:
    - nói: "discount group không tồn tại → reject → chặn update mồ côi"
    - bấm update, chỉ trạng thái unchanged

### phần 5 – demo delete (1–2 phút):
  - chọn 2 case: d3, d2
  - d3:
    - nói: "discount group active → discount active → soft delete chuẩn"
    - chỉ child inactive
  - d2:
    - nói: "parent soft deleted rồi → noop → không xóa dây"
  - không nói thêm

### phần 6 – chốt (30s):
  - nói: "trong logic này ưu tiên an toàn dữ liệu hơn thao tác"
  - nói: "mọi case ngoài bảng đều rơi về reject/noop"
  - nói: "anh chỉ cần nhớ: không hồi sinh, không trùng, không mồ côi"

---

## nguyên tắc khi nói
  - mỗi case = 1 câu kết luận
  - không giải thích implementation
  - không xin ý kiến
  - không dùng từ mơ hồ

---

## tiêu chí thành công
  - pm hiểu được sau 1 lần xem
  - pm không hỏi "nếu case này thì sao?"
  - pm nói "ok logic rõ, an toàn"

---

## thứ loại bỏ hoàn toàn:
  - giải thích code
  - giải thích thuật ngữ kỹ thuật sâu
  - demo tất cả 15 case
  - hậu kỳ, chỉnh sửa, phụ đề

---

## câu chốt tư duy:
  - "video này không chứng minh hệ thống thông minh, mà chứng minh nó không làm bậy"

# khung prompt chuẩn để record video demo cho pm 
- vai trò của bạn: trợ lý giúp tôi tạo kịch bản record video demo cho pm
- mục tiêu duy nhất: pm hiểu nhanh logic quyết định và chấp nhận solution sau 1 lần xem
- bối cảnh đầu vào: bảng test case / rule quyết định (create, update, delete)
- ràng buộc:
  - video 5–8 phút, quay 1 lần, không hậu kỳ
  - không giải thích code, không giáo khoa, không lan man
  - mỗi case chỉ nói 1 câu kết luận
- cách tư duy:
  - payoff > giải thích
  - allow / reject / noop là output duy nhất
  - thông tin không ảnh hưởng quyết định → loại
- cấu trúc bắt buộc của output:
  - mục tiêu video (1–2 bullet)
  - cấu trúc video theo thời gian
  - case nào demo, vì sao chọn (tiêu chí loại)
  - câu nói mẫu cho từng phần (ngắn, dứt khoát)
  - tiêu chí pm gật đầu
- định dạng:
  - markdown, bullet "-"
  - lowercase toàn bộ
  - không emoji, không đoạn văn dài
- nguyên tắc:
  - ưu tiên kết luận > giải thích
  - đủ đúng để làm ngay > hoàn hảo
