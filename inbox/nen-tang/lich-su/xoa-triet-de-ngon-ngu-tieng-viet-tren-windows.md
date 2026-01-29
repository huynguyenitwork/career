# tài liệu 20/80 – xoá triệt để ngôn ngữ tiếng việt trên windows (dùng powershell 7)

## 1. mục tiêu

hướng dẫn xoá hoàn toàn tiếng việt khỏi windows khi làm việc bằng powershell 7 (ps7).
xử lý ba thành phần:
– language list (ui + bàn phím)
– capability (tính năng ngôn ngữ)
– package (gói cài đặt – mức hệ thống)

tài liệu tập trung vào 20% thao tác tạo ra 80% hiệu quả, đảm bảo sạch sẽ và không tái xuất hiện.

---

## 2. nguyên lý xử lý

powershell 7 không hỗ trợ trực tiếp cmdlet `get-winpackage`, vì module dism được thiết kế cho windows powershell 5.1.
vì vậy, chiến lược 20/80 là:

1. **dùng dism.exe trực tiếp** để thao tác với package (ổn định, chắc chắn hoạt động).
2. **dùng get-windowscapability** trong ps7 để xoá capability tiếng việt.
3. **reset language list** bằng cmdlet vẫn hỗ trợ trong ps7.

ba bước này xử lý trên cả ui lẫn hệ thống.

---

## 3. quy trình 20/80 xử lý hoàn chỉnh (powershell 7)

### bước 1 – reset language list về english

xoá sạch tất cả input method, bàn phím và thiết lập ngôn ngữ hiện tại:

```powershell
$LangList = New-WinUserLanguageList "en-US"
Set-WinUserLanguageList $LangList -Force
```

---

### bước 2 – xóa toàn bộ capability tiếng việt

powershell 7 hỗ trợ đầy đủ lệnh này:

```powershell
Get-WindowsCapability -Online | Where-Object {$_.Name -like "*Vietnamese*"} | Remove-WindowsCapability -Online
```

capability bao gồm:
– typography
– handwriting
– optical character recognition
– supplemental fonts
tất cả đều sẽ được xoá.

---

### bước 3 – tìm và xoá gói ngôn ngữ vietnamese bằng dism

ps7 không có `get-winpackage`, vì vậy dùng dism trực tiếp.

kiểm tra các package tiếng việt:

```powershell
dism.exe /online /get-packages | Select-String "vi-VN"
```

nếu có package xuất hiện, sử dụng lệnh sau để xoá:

```powershell
dism.exe /online /remove-package /packagename:<Tên-package>
```

ví dụ:

```powershell
dism.exe /online /remove-package /packagename:Microsoft-Windows-LanguageFeatures-Basic-vi-VN-Package~31bf3856ad364e35~amd64~~10.0.22621.1
```

lệnh dism luôn hoạt động trong ps7 và không phụ thuộc module.

---

### bước 4 – khởi động lại hệ thống

sau khi restart, windows sẽ tái tạo cấu hình input và loại bỏ các entry tiếng việt còn sót.

---

## 4. tuỳ chọn: sử dụng module windows powershell trong ps7

nếu muốn dùng `get-winpackage` ngay trong ps7 (không khuyến nghị bằng dism nhưng vẫn khả thi):

```powershell
Import-Module Dism -UseWindowsPowerShell
```

sau đó:

```powershell
Get-WinPackage -Online
```

tuy nhiên, cách này chỉ hữu ích khi bạn buộc phải dùng winpackage; dùng dism vẫn hiệu quả hơn.

---

## 5. lưu ý bổ sung

windows có thể tự sync lại tiếng việt thông qua microsoft account.
nếu gặp hiện tượng ngôn ngữ tự quay trở lại:

tắt tính năng sync language:

**settings → accounts → windows backup → turn off “remember my preferences → language preferences”**

---

## 6. kết luận 20/80

– ps7 không xoá winpackage bằng cmdlet, nhưng xoá được bằng dism (chiếm 80% hiệu quả).
– capability và language list vẫn xoá bình thường trong ps7.
– kết hợp cả ba bước sẽ xoá hoàn toàn tiếng việt khỏi windows mà không cần chuyển sang powershell 5.1.

---
