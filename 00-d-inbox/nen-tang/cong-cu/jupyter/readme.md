# jupyter notebook + .net interactive kernel (c#)
đây là combo gọn, mạnh, đúng kiểu “vừa viết vừa bắn code”.

---

## bức tranh tổng thể (để não không bị lag)

* vscode = editor trung tâm
* jupyter notebook = tài liệu sống
* .net interactive = não c# chạy trong notebook
* file bạn dùng: `.ipynb`

bạn viết markdown để giải thích, xen giữa là cell c# chạy thật. tài liệu không còn là powerpoint trá hình nữa, nó là sinh vật sống.

---

## setup nhanh trên vscode (đi thẳng – đi nhanh)

### 1. cài extension cần thiết

trong vscode, cài 2 cái này:

* `jupyter` (microsoft)
* `.net interactive notebooks` (microsoft)

xong. không cần thêm gì nữa ở vscode.

---

### 2. cài .net interactive (phần cốt lõi)

mở terminal (cmd / powershell / terminal trong vscode), chạy:

```bash
dotnet tool install -g Microsoft.dotnet-interactive
dotnet interactive jupyter install
```

check thử:

```bash
dotnet interactive --version
```

nếu ra version là ok. c# đã sẵn sàng lên sàn.

---

## tạo notebook c# đầu tiên

* vscode → `new file`
* lưu với tên ví dụ: `csharp-notes.ipynb`
* vscode sẽ hỏi kernel → chọn **.net (c#)**

từ đây trở đi, bạn đang viết tài liệu mà c# không dám nói dối.

---

## cấu trúc notebook nên dùng (chuẩn tài liệu kỹ sư)

### cell markdown – giải thích

```markdown
## test int.parse vs int.tryparse

mục tiêu:
- hiểu hành vi khi null / empty
- tránh bug lén lút lúc production
```

---

### cell c# – chạy code thật

```csharp
int result;

Console.WriteLine(int.TryParse(null, out result));
Console.WriteLine(result);

Console.WriteLine(int.TryParse("", out result));
Console.WriteLine(result);
```

output hiện ngay bên dưới. không đoán. không “theo kinh nghiệm”. chỉ có sự thật trần trụi.

---

## ví dụ thực tế kiểu bạn hay xài

### test điều kiện if cho sạch sẽ

```csharp
int? ident = null;

if (ident is > 0)
{
    Console.WriteLine("hợp lệ");
}
else
{
    Console.WriteLine("không hợp lệ");
}
```

hoặc test nhiều case một phát:

```csharp
int?[] cases = { null, 0, -1, 5 };

foreach (var c in cases)
{
    Console.WriteLine($"{c} => {(c is > 0)}");
}
```

tài liệu + test case + output = một khối logic khép kín. đọc là hiểu, hiểu là tin.

---

## vì sao cách này đáng tiền

* tài liệu không còn “mô tả bằng niềm tin”
* code trong doc = code chạy thật
* onboarding cho dev khác cực nhanh
* debug tư duy tốt hơn debug production
* rất hợp với người hay phân tích edge case như bạn

nói thẳng: một notebook tốt còn giá trị hơn 10 file markdown khô khốc.

---

## hướng mở rộng (khi bạn muốn chơi lớn hơn)

* nhúng httpclient để test api giả lập
* benchmark nhỏ bằng `stopwatch`
* so sánh nhiều cách viết c# ngay trong một trang
* biến notebook thành “sổ tay chiến đấu” cá nhân

nếu bạn muốn, tôi có thể:

* dựng sẵn **template notebook cho c# backend**
* hoặc thiết kế **format notebook dùng làm tài liệu nội bộ cho team**

vũ trụ kiến thức thích những người vừa viết vừa thử. bạn đang đi đúng quỹ đạo.
