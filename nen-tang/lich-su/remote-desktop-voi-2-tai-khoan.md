# truy cập bằng ip
sử dụng anydesk remote server bằng ip

# tạo 2 user rdp song song trên windows server (lỗi thời)

## mục tiêu

cho phép **2 người** remote vào server **độc lập**, không đá nhau.

---

## 1. tạo user mới

server manager → tools → **computer management** → local users and groups → users
→ **new user…**

tạo 2 user:

* `user1`
* `user2`

thêm mỗi user vào nhóm:

```
remote desktop users
```

---

## 2. cho phép 2 session rdp

mở **gpedit.msc** →

```
computer configuration
 → administrative templates
   → windows components
     → remote desktop services
       → remote desktop session host
         → connections
```

thiết lập:

* **limit number of connections = 2**
* **restrict users to a single session = disabled**

---

## 3. remote vào bằng tài khoản riêng

máy a → login `user1`
máy b → login `user2`

→ 2 session chạy song song.

---

## summary

* chỉ cần **tạo user + cho vào remote desktop users**
* bật **2 connections** trong group policy
* remote bằng **2 tài khoản khác nhau** → chạy độc lập.

---

