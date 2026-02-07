# tạo public address tạm thời để test nhanh

## mục tiêu
- expose service nội bộ ra internet trong vài phút
- test end-to-end gọi được từ bên ngoài
- không cần public ip tại máy local
- chạy 1 file bin, không cài đặt, có public url ngay

## tiêu chí loại
- cần package manager → loại
- cần config dài → loại
- cần quyền root → loại

---

## khuyến nghị 1: cloudflared (bin thuần)

### mô tả
- có binary sẵn cho linux / mac / windows
- không cần cài service
- không cần public ip

### dùng ngay
- tải file bin
- `chmod +x cloudflared` (linux/mac)
- chạy:
- nhận public url → gọi test ngay

### kết luận
- nhanh nhất, ít thao tác nhất cho http/https

---

## phương án 2: localtunnel (bin node)

### mô tả
- zero config
- phù hợp test chớp nhoáng

### dùng ngay
- cần node có sẵn
- chạy:
  - `npx localtunnel --port 3000`
- nhận public url → test

### loại khi
- môi trường không có node
- cần ổn định

---

## phương án 3: frp (bin thuần, cần vps)

### mô tả
- frps + frpc đều là binary
- hỗ trợ tcp/udp, port cố định

### dùng ngay (tối thiểu)
- tải frps lên vps (public ip)
- tải frpc về máy local
- chạy frps
- chạy frpc với cấu hình reverse port
- gọi `vps_ip:port` để test

### kết luận
- bin gọn, mạnh, nhưng cần vps

---

## quyết định nhanh
- http test trong 1–2 phút → cloudflared
- test cực nhanh, chấp nhận rủi ro → localtunnel
- tcp/udp nghiêm túc → frp + vps

---

## nhận thức cần khóa
- bin ≠ public ip
- bin chỉ tạo đường đi ra ngoài
- inbound trực tiếp vẫn cần tunnel hoặc vpn

## kết luận cuối
- không có public ip thì không có inbound trực tiếp
- cloudflared bin là lựa chọn "mở file chạy liền" đúng nghĩa cho test nhanh
