# chọn port trống, không xung đột
- xem toàn bộ port đang dùng
  - `netstat -ano | findstr LISTENING`
  - `netstat -ano | findstr LISTENING | sort`
  - port xuất hiện → loại

- kiểm tra port cụ thể
  - `netstat -ano | findstr :<port>`
  - có output → loại

- kiểm tra port bị windows reserve
  - `netsh int ipv4 show excludedportrange protocol=tcp`
  - nằm trong range → loại

- quyết định dùng port
  - >1024
  - không xuất hiện ở 3 bước trên
  - dùng ngay

- gợi ý
  - ưu tiên 5000–5999 hoặc 7000–7999
