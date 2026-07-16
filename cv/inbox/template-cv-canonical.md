question:
tồn tại một mẫu cv "bất biến" nào mà ít thay đổi theo thời gian, tối ưu cho recruiter, ats và tech lead, đồng thời có thể tái sử dụng chỉ bằng cách thay nội dung?
outcome:
* xây dựng được **template cv canonical** chỉ gồm các primitive cốt lõi.
* mỗi primitive có mục đích rõ ràng.
* chỉ thay nội dung theo từng job, không phải thiết kế lại.
* recruiter mất 10–20 giây vẫn tìm được thông tin cần.
* ats đọc được 100%.
* tech lead đọc được chiều sâu kỹ thuật.
mechanisms:

| mechanism             | use when                  | +                | -                   | signals                                                      |
| --------------------- | ------------------------- | ---------------- | ------------------- | ------------------------------------------------------------ |
| canonical structure   | muốn có mẫu dùng 10+ năm  | gần như bất biến | ít màu mè           | mọi cv lớn đều giống nhau                                    |
| information hierarchy | muốn người đọc scan nhanh | tăng tốc đọc     | phải cắt chữ thừa   | mắt luôn đi từ trên xuống                                    |
| keyword-first         | ứng tuyển ATS hoặc HR     | tăng tỉ lệ match | dễ thành liệt kê    | JD có nhiều keyword                                          |
| evidence-first        | phỏng vấn kỹ thuật        | tăng độ tin cậy  | viết khó hơn        | mọi claim đều có bằng chứng                                  |
| impact-first          | senior trở lên            | nổi bật giá trị  | cần đo được kết quả | có số liệu hoặc business value                               |
| one-page scan         | recruiter vòng đầu        | đọc rất nhanh    | phải chọn lọc       | toàn bộ CV nhìn hết trong một màn hình hoặc hai trang tối đa |

links:
* chưa có
---
# ví dụ
## canonical cv (ít thay đổi nhất)
```text
NAME
Target Position
Phone
Email
Github
LinkedIn
Location
==================================================
SUMMARY
CORE SKILLS
EXPERIENCE
PROJECTS
EDUCATION
CERTIFICATIONS
LANGUAGE
```
đây là phần gần như **không đổi suốt nhiều năm**.
---
## mapping theo mục đích
| section     | recruiter | tech lead | ats |
| ----------- | --------- | --------- | --- |
| header      | ✓         |           | ✓   |
| summary     | ✓         | ✓         | ✓  |
| skills      | ✓         | ✓         | ✓  |
| experience  | ✓         | ✓         | ✓  |
| projects    |           | ✓         | ✓   |
| education   | ✓         |           | ✓   |
| certificate | ✓         | ✓         | ✓   |
---
## ví dụ dựa trên cv của bạn
### 1. header
```text
NGUYỄN PHÚ HUY
Senior .NET Backend Developer
Ho Chi Minh City
(+84) 353 xxx xxx
huy.nguyen.it.work@gmail.com
Github
LinkedIn
```
không cần:
* ngày sinh
* giới tính
* ảnh
* tình trạng hôn nhân
trừ khi công ty yêu cầu.
---
### 2. summary
không nên
```text
Ham học hỏi.
Có trách nhiệm.
Có khả năng teamwork.
```
nên
```text
Senior .NET Developer với hơn 6 năm kinh nghiệm phát triển hệ thống ERP,
POS và Enterprise Software.
Có kinh nghiệm Backend, Database, Integration và System Design.
Đã phát triển sản phẩm cho Manufacturing, Government,
Hospitality và Retail.
```
Người đọc biết ngay
* senior
* số năm
* domain
* loại hệ thống
---
### 3. core skills
thay vì
```text
Python
C#
Angular
Vue
Bootstrap
...
```
gom nhóm
```text
Backend
.NET
ASP.NET MVC
WebAPI
Python (Odoo)
Database
SQL Server
PostgreSQL
MySQL
Oracle
Frontend
Angular
Vue
JavaScript
TypeScript
Architecture
REST API
Entity Framework
Docker
Git
Testing
xUnit
NUnit
UAT
```
scan cực nhanh.
---
### 4. experience
thay vì
```text
Mô tả dự án
...
Trách nhiệm
...
...
```
nên
```text
Nagakawa
ERP Developer
08/2023 – Present
Domain
Manufacturing ERP
Tech
Python
Odoo
PostgreSQL
Docker
Achievements
• Phát triển nhiều module ERP
• Migration Base → Odoo
• Thiết kế Technical Specification
• Unit Test
• UAT
```
mắt đọc chỉ mất vài giây.
---
### 5. project
đây là phần Tech Lead thích nhất.
Ví dụ
```text
ERP Internal Platform
Role
ERP Developer
Business
ERP cho doanh nghiệp sản xuất.
Tech
Python
Odoo
PostgreSQL
Docker
Responsibilities
• Phát triển module HR
• Workflow
• Notification
• Dashboard
Impact
• Migration Base → Odoo
• Tiết kiệm chi phí license
• Chuẩn hóa quy trình doanh nghiệp
```
thay vì mô tả dài.
---
### 6. achievement
đây là phần thường bị thiếu.
Ví dụ
```text
Achievements
• Migration thành công Base → Odoo
• Tham gia phát triển ERP cho nhiều doanh nghiệp
• Thiết kế Technical Specification
• Fullstack Development
• Unit Test và UAT
```
---
### 7. education
```text
University of Civil Engineering
Software Engineering
2013–2018
```
không cần nhiều hơn.
---
## nguyên tắc bất biến
```text
Header
↓
Summary
↓
Skills
↓
Experience
↓
Project
↓
Impact
↓
Education
```
không đổi.
---
## chỉ thay nội dung
ví dụ apply
Senior Backend
↓
Summary
```text
Backend
Distributed Systems
API
Performance
```
---
apply
ERP
↓
Summary
```text
ERP
Workflow
Manufacturing
Odoo
```
---
apply
Solution Architect
↓
Summary
```text
Architecture
Integration
Business Analysis
System Design
```
Template không đổi.
---
## điều thay đổi duy nhất
```text
Canonical CV
↓
Summary
↓
Keyword
↓
Project Order
↓
Achievement Order
```
chỉ 4 phần này thay đổi.
---
## mô hình tổng quát
```text
CV
├── Identity
│
├── Capability
│
├── Evidence
│
├── Business Impact
│
└── Contact
```
