## tài liệu gọt vs code về trạng thái tối giản (cli-first)

### mục tiêu

- giảm tải vs code: nhẹ, nhanh, ít nhiễu
- kiểm soát extension bằng dòng lệnh, không phụ thuộc ui
- giữ đúng những gì phục vụ công việc hiện tại, bỏ phần “để đó cho vui”

nguyên lý xuyên suốt:
**một chức năng – một extension. không dùng – tắt. không nhớ – gỡ.**

---

## 1. điều kiện cần

đảm bảo vs code cli hoạt động:

```
code --version
```

nếu không nhận lệnh `code`, cần add vs code vào path.

---

## 2. liệt kê toàn bộ extension đã cài

### liệt kê tên extension

```
code --list-extensions
```

### liệt kê kèm version (phục vụ audit)

```
code --list-extensions --show-versions
```

### xuất ra file để review

```
code --list-extensions > extensions.txt
```

file này là “bản đồ hiện trạng” của vs code.

---

## 3. phân loại extension trước khi dọn

mở `extensions.txt`, chia nhanh trong đầu thành 3 nhóm:

### nhóm a – cốt lõi (giữ)

- language support đúng stack đang làm
- git (chỉ 1 extension)
- formatter (chỉ 1)
- debugger thực sự dùng

### nhóm b – tình huống (disable workspace)

- docker, kubernetes
- cloud provider
- test tool chỉ dùng cho project đặc thù

### nhóm c – rác kỹ thuật (disable hoặc uninstall)

- theme, icon dư thừa
- extension cài thử rồi bỏ
- tool không nhớ rõ chức năng

---

## 4. tắt extension bằng dòng lệnh

### disable global

```
code --disable-extension publisher.extension
```

### disable theo workspace (khuyến nghị)

```
code --disable-extension publisher.extension --workspace
```

ví dụ:

```
code --disable-extension eamodio.gitlens --workspace
```

cách này giúp:

- vs code global vẫn sạch
- project nào cần thì bật riêng

---

## 5. gỡ extension khỏi máy (uninstall)

khi đã chắc chắn không dùng:

```
code --uninstall-extension publisher.extension
```

ví dụ:

```
code --uninstall-extension streetsidesoftware.code-spell-checker
```

cài lại khi cần:

```
code --install-extension publisher.extension
```

không có mất mát gì, chỉ là bỏ gánh nặng.

---

## 6. dọn hàng loạt bằng script (nhanh và dứt khoát)

### disable toàn bộ extension trong file

powershell:

```
Get-Content extensions.txt | ForEach-Object {
  code --disable-extension $_
}
```

sau đó enable lại từng extension cần thiết.

### uninstall hàng loạt (chỉ dùng khi reset mạnh)

```
Get-Content extensions.txt | ForEach-Object {
  code --uninstall-extension $_
}
```

---

## 7. workflow gợi ý cho dev nghiêm túc

### lần đầu setup

- list extension → `baseline.txt`
- chỉ giữ extension phục vụ stack chính

### hàng tháng

- `code --list-extensions`
- So với baseline
- Extension mới mà không nhớ lý do tồn tại → disable ngay

### nguyên tắc kỷ luật

- không cài extension vì “có thể sau này cần”
- editor là công cụ lao động, không phải chợ plugin

---

## 8. trạng thái vs code lý tưởng

- startup nhanh
- không lag khi mở file lớn
- intellisense ổn định
- không có extension chạy ngầm vô nghĩa

vs code gọn không làm bạn code giỏi hơn ngay lập tức,
nhưng nó **loại bỏ ma sát**, mà ma sát ít thì tư duy chạy xa hơn.

bước tiếp theo hợp lý là:
gọt **settings.json**, **keybindings**, và **layout** để vs code đúng nghĩa “c#-only / backend-only”.
