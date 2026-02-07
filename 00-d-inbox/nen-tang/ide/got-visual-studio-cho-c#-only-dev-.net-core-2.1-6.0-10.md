# mục tiêu

tài liệu này dùng để **chuẩn hoá visual studio cho lập trình viên chỉ làm c#/.net**, loại bỏ các thành phần không cần thiết, giảm nhiễu, giảm tải hệ thống và tránh lỗi do dùng sai sdk.

phạm vi sử dụng:

* ngôn ngữ: **c#**
* nền tảng: **.net core 2.1, .net 6.0, .net 10**
* không bao gồm: c++, python, node.js, mobile native, data science, game dev

---

# phần 1 – gọt từ gốc: workloads trong visual studio installer

## bắt buộc giữ

cài **tối thiểu** các workloads sau:

* **.net desktop development**
  dùng cho winforms, wpf, tooling c# cơ bản

* **asp.net and web development**
  dùng cho web api, mvc, minimal api, background services

> nếu không làm ui desktop thì vẫn nên giữ .net desktop development vì nhiều tool nội bộ của vs phụ thuộc.

---

## có thể loại bỏ

gỡ toàn bộ nếu không dùng:

* desktop development with c++
* python development
* node.js development
* game development (unity, unreal)
* mobile development (android/ios, xamarin)
* data science & ml
* azure development
* office / sharepoint development
* linux development

nguyên tắc: **workload nào không build ra assembly c# thì không cần tồn tại**.

---

# phần 2 – .net sdk / runtime: nên cài gì, bỏ gì

## nên giữ

chỉ giữ đúng các phiên bản bạn thực sự dùng:

* .net core **2.1 sdk + runtime** (legacy)
* .net **6.0 sdk + runtime** (lts)
* .net **10 sdk + runtime** (nếu đang thử nghiệm / chuẩn bị tương lai)

bao gồm:

* microsoft .net sdk
* microsoft .net runtime
* microsoft asp.net core runtime

---

## nên gỡ

có thể gỡ an toàn:

* .net core 1.x
* .net core 2.0
* .net core 3.0 / 3.1
* .net 5.0
* preview sdk không sử dụng
* targeting pack cho framework không build

**không gỡ:**

* .net framework 4.x (visual studio và windows còn dùng)

---

# phần 3 – cách kiểm tra sdk đang dùng (bắt buộc làm)

mở terminal:

```
dotnet --list-sdks
dotnet --list-runtimes
```

đây là danh sách **thực tế dotnet dùng**, không phải những gì visual studio hiển thị.

---

## kiểm tra project có khoá sdk không

tìm file `global.json` tại root solution:

```
{
  "sdk": {
    "version": "6.0.4xx"
  }
}
```

* có `global.json` → project **chỉ dùng đúng sdk đó**
* không có → dotnet sẽ dùng **sdk mới nhất đang cài**

khuyến nghị: **mọi solution nên có `global.json`**.

---

# phần 4 – gỡ sdk đúng cách trên windows

vào:

* settings → apps → installed apps

tìm và gỡ:

* microsoft .net sdk x.y (ngoài 2.1 / 6.0 / 10)
* microsoft asp.net core runtime x.y (ngoài các version trên)
* microsoft .net runtime x.y (ngoài các version trên)

không cần động tới visual studio installer khi gỡ sdk.

---

# phần 5 – dọn ide: tắt thứ không cần trong visual studio

## text editor

* bật:

  * line numbers
  * highlight current line

* tắt:

  * automatic outlining
  * word wrap (nếu không viết prose)
  * virtual space

---

## intellisense

* giữ:

  * completion
  * parameter information

* tắt:

  * suggest items from unimported namespaces

mục tiêu: **ít gợi ý nhưng trúng**.

---

## cửa sổ nên đóng và không dùng lại

* live visual tree
* live property explorer
* cloud explorer
* team explorer (nếu dùng git ngoài)
* object browser (f12 thay thế tốt hơn)

sau đó:

* window → reset window layout

---

# phần 6 – extensions: nguyên tắc sống còn

chỉ giữ:

* resharper **hoặc** roslynator (chọn 1)
* git extension bạn thực sự dùng
* editorconfig support

gỡ:

* extension cho js/ts nếu không viết
* azure helper
* ui designer mở rộng
* ai plugin chồng chéo

nguyên tắc: **mỗi extension = thêm độ trễ + thêm rủi ro**.

---

# phần 7 – checklist xác nhận sau khi gọt

* restart máy
* mở solution
* restore nuget
* build toàn bộ
* chạy api / test chính

nếu tất cả pass → cấu hình hợp lệ.

---

# kết luận

visual studio không chậm. nó chỉ đang bị dùng như dao đa năng để gọt táo.

với c#-only dev:

* ít workload
* ít sdk
* ít extension
* có `global.json`

khi ide im lặng, dòng code bắt đầu nói chuyện.
