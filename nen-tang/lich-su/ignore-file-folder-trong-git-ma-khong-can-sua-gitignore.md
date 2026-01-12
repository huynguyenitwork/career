# ignore file/folder trong git mà không cần sửa `.gitignore`

## cách làm
- đẩy vào thư mục .vs

## lỗi thời (kiểm tra không dùng được)

### 1. bỏ qua thay đổi của 1 file (assume-unchanged)

dùng khi bạn chỉ muốn git tạm thời *coi như file không thay đổi*.

**bật:**

```
git update-index --assume-unchanged path/to/file
```

**tắt:**

```
git update-index --no-assume-unchanged path/to/file
```

---

### 2. bỏ qua thay đổi của 1 folder (skip-worktree)

dùng khi bạn muốn ignore luôn cả thư mục nhưng không muốn chỉnh `.gitignore`.
kiểm tra đường dẫn thư mục track với status
```
git status
```
kiểm tra đường dẫn file/folder có xác định được hay không
```
git ls-files | find "<path/to/folder/>"
```

**bật:**

```
git ls-files path/to/folder/ | xargs git update-index --skip-worktree
```

**tắt:**

```
git ls-files path/to/folder/ | xargs git update-index --no-skip-worktree
```

---

### 3. ghi chú quan trọng

* các lệnh này chỉ áp dụng **local**, không ảnh hưởng repo chung.
* nếu folder bị skip-worktree có thay đổi từ người khác, khi `git pull` bạn cần kiểm tra lại.
* không phù hợp nếu bạn muốn ignore lâu dài → lúc đó mới dùng `.gitignore`.

---
