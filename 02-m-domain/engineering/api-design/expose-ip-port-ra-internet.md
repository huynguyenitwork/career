# expose ip + port ra internet

## tầng 1: internet / isp
- câu hỏi: gói tcp từ internet có được phép đi tới ip này không?
- lỗi thường gặp:
  - isp chặn port (6000–7000 hay bị)
  - ip public không route trực tiếp
- hành động:
  - test port phổ biến (80 / 443 / 8080)
- tiêu chí loại:
  - đổi port mà vẫn fail → chưa tới được server

## tầng 2: cloud / datacenter firewall (upstream)
- câu hỏi: hạ tầng trước server có cho phép port này không?
- ví dụ:
  - aws security group
  - azure nsg
  - firewall nhà cung cấp dc
- hành động:
  - check inbound rule tại cloud/dc
- tiêu chí loại:
  - windows firewall mở nhưng cloud block → **fail**

## tầng 3: nat / port forwarding
- câu hỏi: ip public có map trực tiếp vào máy này không?
- lỗi thường gặp:
  - server nằm sau nat
  - port chưa forward
  - public ip không phải ip của nic server
- hành động:
  - kiểm tra ip public có gắn thẳng nic server
- tiêu chí loại:
  - local test public ip fail → nat

## tầng 4: network interface trên server
- câu hỏi: service bind đúng interface chưa?
- lỗi thường gặp:
  - server có nhiều nic
  - service bind nic nội bộ
- hành động:
  - `ipconfig`
  - đối chiếu ip bind với ip public
- tiêu chí loại:
  - bind sai nic → ngoài không vào

## tầng 5: firewall trên os (windows firewall)
- câu hỏi: os có cho phép inbound tcp port này không?
- hành động:
  - inbound rule allow tcp <port>
- tiêu chí loại:
  - rule sai profile (domain/private/public)

## tầng 6: process / service listen
- câu hỏi: process có thật sự listen port không?
- hành động:
  - `netstat -ano | findstr <port>`
- tiêu chí đạt:
  - thấy `0.0.0.0:<port>` hoặc `:::<port>`
- tiêu chí loại:
  - không thấy → service chưa listen

## tầng 7: bind address / protocol
- câu hỏi: bind đúng kiểu cho external chưa?
- hành động:
  - ưu tiên `0.0.0.0`
- tiêu chí loại:
  - `127.0.0.1`
  - `localhost`
  - `*` thiếu urlacl

## tầng 8: protocol mismatch
- câu hỏi: client test đúng protocol chưa?
- ví dụ:
  - tcp test ≠ http test
- hành động:
  - tcp → `test-netconnection`
  - http → `invoke-webrequest`
- tiêu chí loại:
  - tcp chưa thông mà test http

## tầng 9: ứng dụng logic
- câu hỏi: app có trả response không?
- chỉ xét khi:
  - tcp đã thông
- tiêu chí loại:
  - debug code khi tcp fail

## thứ tự bắt buộc (không đảo)
- internet/isp
- cloud/dc firewall
- nat
- nic
- os firewall
- process listen
- bind address
- protocol
- logic

## kết luận root cause
- local ok + external fail
- bind đã đúng
- firewall os đã mở
→ nguyên nhân luôn nằm ở:
- isp
- cloud/dc firewall
- nat / ip public không direct

## quy tắc vàng
- ip+port ra ngoài = bài toán hạ tầng
- code chỉ là tầng cuối
- tcp chưa thông → mọi thứ phía trên đều nhiễu
