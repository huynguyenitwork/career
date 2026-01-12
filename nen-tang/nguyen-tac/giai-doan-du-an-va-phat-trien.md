# giai đoạn dự án

## 1. kick-off
- mục tiêu: đồng bộ team, xác định scope, vai trò, timeline.
- 20/80 trọng tâm: ai làm gì + thời hạn quan trọng + mục tiêu dự án.
## 2. workshop
- mục tiêu: hiểu nhu cầu khách hàng & vạch giải pháp sơ bộ.
- trọng tâm: những yêu cầu chính, vấn đề cốt lõi cần giải quyết, rủi ro lớn.
## 3. phân tích & thiết kế hệ thống
- mục tiêu: chuyển yêu cầu thành blueprint kỹ thuật.
- trọng tâm: kiến trúc tổng thể, luồng dữ liệu chính, các module cốt lõi.
## 4. development (dev)
- mục tiêu: code & build hệ thống.
- trọng tâm: chức năng chính phải chạy trước, coding chuẩn, không bug nặng.

### 4.1. discovery (hiểu vấn đề)
hiểu *ai đau – đau chỗ nào – có đáng làm không*. sai chỗ này là làm vô nghĩa.

### 4.2. pre-dev (định hình lời giải)
chốt scope, luồng, api, tech stack, ước lượng. sai chỗ này là dev mệt, sửa hoài.

### 4.3. dev (xây cho chạy)
code theo kế hoạch đã chốt. đây là chỗ tốn công nhất nhưng không phải chỗ quyết định nhất.

### 4.4. test & release (cho ra đời an toàn)
đảm bảo chạy đúng, deploy không nổ. bỏ qua là ăn bug với user.

### 4.5. post-dev (sống còn)
fix, tối ưu, lặp lại theo phản hồi thật. sản phẩm sống hay chết nằm ở đây.

=> **80% kết quả nằm ở 2 bước đầu: discovery + pre-dev.**
ba bước sau chủ yếu là thực thi và trả nợ cho quyết định trước đó.

nhớ câu này cho gọn não:
*hiểu đúng → nghĩ kỹ → làm nhanh → sửa ít → sống lâu.*

## 5. sit (system integration test)
- mục tiêu: kiểm thử tích hợp các module.
- trọng tâm: các chức năng chính hoạt động trơn tru, dữ liệu luân chuyển đúng, lỗi nghiêm trọng được fix.
## 6. uat (user acceptance test)
- mục tiêu: khách hàng xác nhận hệ thống đáp ứng yêu cầu.
- trọng tâm: các use-case chính hoạt động, ux chấp nhận được, lỗi nhỏ có thể fix sau.
## 7. go-live
- mục tiêu: đưa hệ thống vào vận hành thực tế.
- trọng tâm: hệ thống chạy ổn định, backup + support sẵn sàng, các issue nghiêm trọng được kiểm soát.
