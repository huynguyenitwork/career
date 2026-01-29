# promotion engine ↔ pos — tài liệu chuẩn hoá nghiệp vụ & kỹ thuật (20/80)

## mục tiêu
- khoá rõ nghiệp vụ trước khi code → không đoán yêu cầu
- tách ranh giới pos / promotion engine → không tranh quyền
- giảm vòng hỏi–đáp → dev quyết định nhanh, triển khai sớm

## nguyên tắc sống còn
- chưa rõ mục tiêu nghiệp vụ → chưa có yêu cầu kỹ thuật
- promotion engine là decision service, không phải workflow
- thiếu 1 ý bắt buộc → dừng implement

## điều kiện bắt buộc để dev bắt đầu code
- mục tiêu nghiệp vụ: promotion dùng để làm gì
- thời điểm kích hoạt: pos gọi khi nào
- phạm vi áp dụng: bill / item / user / store
- rule ưu tiên & xung đột: cộng dồn hay loại trừ
- input nghiệp vụ tối thiểu: pos phải gửi gì
- output mong muốn: engine trả lại gì
- xử lý khi không đủ điều kiện hoặc lỗi

## phân vai trách nhiệm
- po: xác nhận nghiệp vụ đầy đủ, khoá quyết định
- dev: thiết kế & triển khai kỹ thuật theo nghiệp vụ đã khoá
- thiếu xác nhận → chưa đủ điều kiện code

## triết lý inbound (pos → engine)
- engine không cần biết thế giới
- engine chỉ cần snapshot tại thời điểm checkout
- snapshot càng sạch → quyết định càng đúng

## inbound bắt buộc (để engine không mù)
- định danh & truy vết: bill, store, channel, thời điểm
- danh sách item: sản phẩm, số lượng, giá gốc, nhóm rule đọc được
- tổng quan bill: subtotal, item_count, tiền tệ

## inbound tuỳ chọn (có thì dùng, không có vẫn chạy)
- thông tin khách hàng: định danh, tier, lần mua đầu
- context đặc biệt: coupon, phương thức thanh toán, giao hàng

## nguyên tắc inbound
- chỉ gửi dữ liệu rule có thể đọc
- không dump database
- không gửi thông tin không ảnh hưởng quyết định

## triết lý outbound (engine → pos)
- engine ra quyết định
- pos thi hành & hiển thị
- không tranh quyền ghi dữ liệu

## outbound engine phải trả
- trạng thái quyết định: áp dụng / không áp dụng / lỗi
- kết quả khuyến mãi: số tiền giảm, quà tặng nếu có
- metadata giải thích: promo nào áp, vì sao không áp

## nguyên tắc outbound
- không side-effect
- không sửa bill
- không ghi db nghiệp vụ
- không yêu cầu pos gọi lại

## hành vi khi engine lỗi
- engine lỗi → pos vẫn bán hàng
- fallback về giá gốc
- không block checkout
- không retry nghiệp vụ tại pos

## giao thức vận hành
- api đồng bộ, realtime
- latency thấp
- engine stateless
- pos luôn có fallback

## tách kiến trúc bắt buộc
- promotion engine: realtime, user-facing
- sync/background service: retry, stateful
- không trộn chung để tránh lan sự cố

## checklist triển khai nhanh
- inbound đủ snapshot
- outbound đủ quyết định + lý do
- timeout ngắn
- log theo bill
- không retry nghiệp vụ

## kết luận một dòng
- promotion engine chỉ cần snapshot checkout để ra quyết định khuyến mãi; nếu lỗi, pos bán giá gốc và hệ thống không được dừng
