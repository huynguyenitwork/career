# khóa sdk .net khi chạy project bằng task cli

## mục tiêu

- tránh chạy sai **sdk .net**
- đảm bảo **mỗi repo dùng đúng version**
- task cli chạy ổn định trên mọi máy

---

# nguyên tắc

- mỗi repo phải có `global.json`
- task phải `cd` vào repo trước khi chạy
- không ép version bằng flag cli

sdk resolver của dotnet:

```
current folder
   ↓
global.json
   ↓
sdk version
```

---

# 1. kiểm tra sdk đã cài

```bash
dotnet --list-sdks
```

ví dụ

```
6.0.428
10.0.103
```

---

# 2. tạo global.json

chạy tại **root repo**

```bash
dotnet new globaljson --sdk-version 6.0.428
```

file tạo ra

```json
{
  "sdk": {
    "version": "6.0.428",
    "rollForward": "disable"
  }
}
```

---

# 3. cấu trúc repo

```
repo
 ├─ global.json
 ├─ src
 └─ project.csproj
```

---

# 4. cấu hình task cli

```json
{
  "label": "run service",
  "command": "cmd",
  "args": ["/c", "cd /d D:/repo && dotnet run --project src/project.csproj"],
  "use_new_terminal": true
}
```

---

# 5. kiểm tra sdk đang dùng

```bash
cd D:/repo
dotnet --version
```

phải trùng với `global.json`.

---

# rule sử dụng

- mỗi repo = 1 `global.json`
- luôn chạy `dotnet` trong repo
- không dùng flag ép sdk

---

# kết luận

cách ổn định để chạy nhiều project .net sdk khác nhau:

```
global.json
   +
run command trong repo
```
