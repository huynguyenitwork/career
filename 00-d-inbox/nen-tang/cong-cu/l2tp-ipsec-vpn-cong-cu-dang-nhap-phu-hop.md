# l2tp/ipsec vpn – công cụ đăng nhập phù hợp

## thông tin cấu hình
- server: vpn.dcorp.com.vn  
- vpn type: l2tp/ipsec with pre-shared key  
- shared secret (psk): Dc0rp  
- auth: username & password
- username: d.developer@dcorp.com.vn
- password: Sb1q7MJF0cwVWL

=> đây là mô hình vpn enterprise cổ điển (l2tp + ipsec + user/pass)

---

## công cụ nên dùng (đúng & gọn)

### windows 10/11
- **windows vpn built-in**
- system → network & internet → vpn
- ổn định nhất, không cần cài thêm

### macos / ios
- **vpn native của hệ điều hành**
- loại: l2tp over ipsec
- apple hỗ trợ chuẩn

### android
- **android vpn built-in**
- loại: l2tp/ipsec psk

### linux
- **strongswan + xl2tpd**
- strongswan: xử lý ipsec (psk)
- xl2tpd: xử lý l2tp + user/pass

---

## không nên dùng
- openvpn / wireguard client
- nordvpn / expressvpn
- v2ray / clash

(lý do: khác giao thức)

---
## vấn đề thường gặp

### khắc phục lỗi the connection was terminated by the remote computer before it could be completed
- tại advanced options > more vpn properties > tab security (allow these protocols) tích chọn 3 loại
- tham khảo: https://vanishedvpn.freshdesk.com/support/solutions/articles/17000062078-how-to-fix-the-connection-was-terminated-by-the-remote-computer-before-it-could-be-completed-
### không kết nối được vpn server
kiểm tra lỗi bằng: mở event viewer
- win + r → gõ eventvwr.msc → enter
- win + s → gõ event viewer → enter
xem lỗi ở tab
- windows logs/application/error [rasclient]



## lưu ý nhanh cho dev
- lỗi 789 / 809 trên windows → thường do firewall chặn udp 500/4500
- l2tp/ipsec là công nghệ cũ, đủ dùng cho intranet
- nếu mở rộng lâu dài → nên migrate ikev2 hoặc wireguard

---

## kết luận
- dùng **vpn built-in của hệ điều hành** là lựa chọn tối ưu
- client đã đúng, nếu lỗi thường nằm ở network hoặc server
