# giai đoạn dự án

## nguyên tắc
- 80% kết quả nằm ở: discovery + pre-dev
- các bước sau = thực thi và trả nợ quyết định trước

## pipeline chuẩn

### 1. kick-off
- chốt: mục tiêu dự án
- khóa: scope, vai trò, mốc thời gian
- không khóa được → dự án mù hướng

### 2. workshop
- xác định: vấn đề thật cần giải
- loại: yêu cầu phụ, nice-to-have
- bỏ sót rủi ro lớn → trả giá về sau

### 3. discovery (hiểu đúng)
- ai đau?
- đau chỗ nào?
- có đáng làm không?
- sai bước này → làm vô nghĩa

### 4. pre-dev (nghĩ kỹ)
- chốt: scope, luồng chính, api, tech stack, ước lượng
- sai bước này → dev mệt, sửa hoài

### 5. dev (làm nhanh)
- build chức năng cốt lõi trước
- code theo quyết định đã khóa
- không quyết định mới trong dev

### 6. test & release
- đảm bảo: chạy đúng, deploy an toàn
- bỏ qua → bug đập thẳng vào user

### 7. sit
- kiểm tra tích hợp module
- dữ liệu đi đúng, flow không gãy

### 8. uat
- user xác nhận use-case chính
- lỗi nhỏ chấp nhận, lỗi lõi phải fix

### 9. go-live
- hệ thống chạy thật
- backup + support sẵn
- kiểm soát sự cố nghiêm trọng

### 10. post-dev
- fix theo phản hồi thật
- tối ưu và lặp
- sản phẩm sống hay chết ở đây

## câu nhớ nhanh
- hiểu đúng → nghĩ kỹ → làm nhanh → sửa ít → sống lâu
