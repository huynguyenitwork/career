# bind address http trên windows

## http://127.0.0.1:<port>
- nghĩa: loopback ipv4
- truy cập: chỉ máy hiện tại
- dùng khi:
  - dev local
  - service nội bộ
- tiêu chí loại:
  - cần truy cập từ máy khác / internet

## http://localhost:<port>
- nghĩa: alias của loopback (`127.0.0.1` hoặc `::1`)
- truy cập: chỉ máy hiện tại
- dùng khi:
  - dev nhanh
- rủi ro:
  - dính ipv6 → nhiễu debug
- tiêu chí loại:
  - debug network / production

## http://0.0.0.0:<port>
- nghĩa: bind tất cả interface ipv4
- truy cập:
  - local
  - lan
  - internet (nếu firewall/nat cho phép)
- dùng khi:
  - expose service ra ngoài
  - debug kết nối nhanh
- đặc điểm:
  - socket tcp thật
  - netstat thấy rõ
- ưu tiên mặc định khi cần truy cập từ ngoài

## http://*:<port>
- nghĩa: wildcard của http.sys
- truy cập:
  - phụ thuộc http.sys + urlacl
- dùng khi:
  - iis
  - windows service dùng http.sys
- ràng buộc:
  - bắt buộc `netsh http add urlacl`
- rủi ro:
  - thiếu urlacl → service chạy nhưng không listen
- tiêu chí loại:
  - cần đơn giản / debug nhanh

## chọn nhanh
- dev local → `127.0.0.1`
- expose ra ngoài → `0.0.0.0`
- iis / http.sys → `*`
- thấy `localhost` trong production → loại

## quy tắc lọc nhiễu
- local ok ≠ external ok
- debug kết nối ngoài → tránh `localhost`, tránh `*`
- ưu tiên đi thẳng: `0.0.0.0` → xong
