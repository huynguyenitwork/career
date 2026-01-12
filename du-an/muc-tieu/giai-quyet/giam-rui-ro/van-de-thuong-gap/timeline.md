# 22-12-2025
- ưu tiên điều phối luồng dữ liệu thế nào là phù hợp kỹ thuật/thực tế (không hoàn hảo)
- hiểu được nền tảng về mặt vận hành của **queue/retry/monitoring/autohealing** khi nào **cần/không cần timing** chạy **đồng bộ/song song/đồng thời** với **điều kiện cần/đủ** và **các bước thực hiện và kết quả đạt được** (giống giao thông/giao hàng) để tránh hỗn loạn [important]
- cơ chế retry nên **cần có thời gian cho next step retry** (cố gắng sửa lại) như shiper giao hàng, đặt lịch hẹn
- bảng so sánh và **theo dõi monitoring và auto-healing** khi nào cần/không cần dành cho dev/đại trà (ngoại đạo)
- mini project mô phỏng 6 rủi ro thường gặp để hiểu bối cảnh (context) dùng với python/c#
- giới hạn monitoring và auto healing dành cho dịch vụ đồng bộ (bắt buộc cần có) dành cho các lỗi thường gặp, phiên bản thực tế như hệ thống giao thông
- timeout và cancel hoạt động thế nào? mini project để hiểu trong quá trình runtime thì timeout (đặt thời gian hạn chế) cho tiến trình

# 18-12-2025
- efsavechanges và executesqlcommand trong các luồng **job / worker / state machine**, SaveChanges() có thể chỉ update lần đầu, các lần sau không thay đổi DB dù không có lỗi (dùng executesqlcommand)
- với nhiều yêu cầu khác nhau, khi hàng đợi làm việc không đúng chỉ quyết định 1 lần thay vì quyết định theo thứ tự (giống như bảo vệ chỉ quẹt cho xe đầu tiên vào rồi đi làm việc khác, xe 2 vào không quẹt và có người mở cổng không vào được). phương án dùng queue thay thế (queue db persist thay vì scope - dài hạn thay ngắn hạn)

# 17-12-2025
- làm sao có thể quan sát được luồng trong schedule/task thế nào, trong code ra làm sao thứ tự chạy kiểu vậy, giống như tôi quan sát giao thông chạy người a, người b đi tới đâu hoặc khoảng cách nhau ra sao, ai trước ai sau trong visual studio
=> quan sát bằng dấu chân thời điểm đi qua (log db)