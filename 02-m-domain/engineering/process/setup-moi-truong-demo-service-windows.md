# setup môi trường demo service windows

## chọn port
- scan port đang listen → `netstat -ano | findstr LISTENING`
- kiểm tra port dự kiến → `netstat -ano | findstr :<port>`
- kiểm tra port bị reserve → `netsh int ipv4 show excludedportrange protocol=tcp`
- port hợp lệ khi >1024 + không xuất hiện + không nằm trong reserve
- ưu tiên chọn port 5000–5999 hoặc 7000–7999

---

## quản lý vòng đời service bằng .bat
- tách mỗi hành động thành 1 file script
- đặt exe tại `service/myservice.exe`
- đặt script tại `service/scripts/`
- dùng đường dẫn tương đối qua `%~dp0`
- flow chuẩn: **install → start → status → stop → uninstall**

### install
```bat
@echo off
set service_name=myservice
set service_bin=%~dp0..\myservice.exe

sc create %service_name% binpath= "%service_bin%" start= auto
```

### start

```bat
@echo off
set service_name=myservice

sc start %service_name%
```

### status

```bat
@echo off
set service_name=myservice

sc query %service_name%
```

### stop

```bat
@echo off
set service_name=myservice

sc stop %service_name%
```

### uninstall

```bat
@echo off
set service_name=myservice

sc stop %service_name% >nul 2>&1
sc delete %service_name%
```

---

## tiêu chí loại

* service không cần auto start → bỏ `start= auto`
* service không hỗ trợ pause → không tạo pause/continue
* service lỗi start → test exe chạy độc lập
* service không nhận path → debug bằng `echo %service_bin%`

---

## prompt tạo wbs demo

```
hãy viết wbs cho task sau với góc nhìn senior dev:
- chỉ giữ đúng các hạng mục tôi nêu, không mở rộng
- mỗi task gồm:
  - 1 gạch tổng quan
  - 1 gạch mô tả việc cần làm
  - 1 gạch effort thuận / nghịch
- ước lượng effort cho demo happy path
- định dạng markdown
- bullet "-"
- lowercase
- nội dung ngắn
- không giải thích thêm
```