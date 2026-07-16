# nỗi đau thực sự của shinhan ds

## 1. điểm nghẽn hệ thống (technical bottlenecks)

- **xung đột hiệu năng cơ sở dữ liệu:** (_suy luận_) truy vấn oracle sql/plsql nghẽn cổ chai, thiếu chỉ mục tối ưu → trì trệ tốc độ xử lý giao dịch thời gian thực (napas 247, core banking).
- **nợ kỹ thuật hệ thống cũ:** (_suy luận_) mã nguồn c-based monolithic thiếu tài liệu, thiếu chuẩn kiểm duyệt → lỗi phát sinh liên tục trên môi trường production, tốn thời gian khắc phục sự cố.
- **tích hợp kênh thanh toán phức tạp:** (_suy luận_) bất đồng bộ định dạng dữ liệu giữa core banking và cổng kết nối ngoại vi (iso 8583, swift, ví điện tử) → tăng tỷ lệ thất bại/treo giao dịch.

## 2. điểm nghẽn vận hành (operational pains)

- **lệch dữ liệu đối soát:** (_suy luận_) quy trình hạch toán kế toán (gl), thanh toán thẻ và đối soát thủ công/bán tự động → phát sinh sai lệch sổ sách, rủi ro phạt tuân thủ pháp lý (sbv, pci dss).
- **thiếu hụt nhân sự chủ chốt:** (_suy luận_) sự thiếu hụt kỹ sư giỏi nghiệp vụ core banking/card → quá tải công việc, chậm tiến độ triển khai sản phẩm tài chính mới.
- **chậm trễ quy trình kyc/aml:** (_suy luận_) xử lý trùng lặp dữ liệu khách hàng (cif) và rà soát rửa tiền kém hiệu quả → nghẽn luồng mở tài khoản, ảnh hưởng trải nghiệm người dùng.

## 3. ứng viên mid/senior cần tháo gỡ

- **thực tế:** tối ưu hóa truy vấn sql/plsql và tinh chỉnh hiệu năng hệ thống core/card để gánh tải giao dịch tức thời.
- **thực tế:** trực tiếp tham gia sửa lỗi cấp bách (production issue), tái cấu trúc mã nguồn cũ và chuẩn hóa tài liệu kỹ thuật.
- **thực tế:** thiết kế, lập trình luồng đối soát tự động hóa, đảm bảo chuẩn tuân thủ bảo mật và báo cáo ngân hàng nhà nước.

# kết luận

cân nhắc
