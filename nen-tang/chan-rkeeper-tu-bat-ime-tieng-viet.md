# Khắc phục lỗi bàn phím tự chuyển sang tiếng Việt trong ứng dụng (R-Keeper)

## 1. Hiện tượng

Khi nhập liệu trong một số ứng dụng (đặc biệt là R-Keeper), bàn phím tự chuyển từ tiếng Anh sang tiếng Việt, dù đã xoá gói ngôn ngữ và bàn phím tiếng Việt trong Windows.

## 2. Nguyên nhân chính (80%)

1. Ứng dụng sử dụng input engine/IME legacy, tự ép Windows đổi layout.
2. Windows còn giữ *Input Method Profile* ẩn trong registry dù đã gỡ trong Settings.

## 3. Cách khắc phục 20% thao tác – cho hiệu quả cao nhất

### Bước 1 – Xoá hoàn toàn language profile bằng PowerShell

Chạy PowerShell với quyền **Admin**:

```powershell
$LangList = Get-WinUserLanguageList
$LangList.RemoveAll({ $_.LanguageTag -eq "vi-VN" })
Set-WinUserLanguageList $LangList -Force
```

Khởi động lại máy.

---

### Bước 2 – Xoá IME tiếng Việt còn sót trong registry

Mở **regedit** và kiểm tra ba vị trí:

* `HKEY_CURRENT_USER\Keyboard Layout\Preload`
* `HKEY_CURRENT_USER\Keyboard Layout\Substitutes`
* `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts`

Nếu thấy mã tiếng Việt `0000042A` hoặc `042A` → xoá.

---

### Bước 3 – Ép Windows chỉ còn một layout (EN-US)

- Việc này giúp ứng dụng không thể tự đổi IME được nữa.

- Không cài thêm ngôn ngữ nào khác ngoài **English (US)**.

- Tạo file .reg (nếu muốn nhanh) để ép Windows luôn dùng một kiểu layout:

```
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Microsoft\CTF\LangBar]
"ShowStatus"=dword:00000003

[HKEY_CURRENT_USER\Software\Microsoft\CTF\LangBar]
"Label"=dword:00000000
```

Điều này ép IME chỉ còn một lựa chọn có thể dùng → app không đổi được nữa.
---

### Bước 4 – Chặn R-Keeper tự bật IME** (nếu phiên bản hỗ trợ)

Chỉnh shortcut của R-Keeper:

```
/DisableTextService
```

Hoặc bật chế độ “Legacy input” trong file config của RK7 nếu có.

---

## 4. Khi nào chắc chắn lỗi đến từ ứng dụng?

Nếu Notepad/Chrome/Word không bị tự đổi layout nhưng chỉ R-Keeper bị → nguyên nhân là do input engine của app, không phải Windows.

---

## 5. Kết luận

Chỉ cần làm 3 bước chính:
**Xoá language profile → xoá IME ẩn → ép dùng một layout.**
Hầu hết lỗi bàn phím tự đổi trong các app legacy như R-Keeper sẽ biến mất.

---