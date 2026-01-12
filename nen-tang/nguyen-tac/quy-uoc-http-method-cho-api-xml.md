# Quy ước HTTP Method cho API XML (RK7 / POS legacy)

## 1. Bối cảnh

Hệ thống RK7 / POS legacy sử dụng **API dạng XML – command-based**, trong đó:

* HTTP **không mang ý nghĩa CRUD**
* Hành vi nghiệp vụ được quyết định bởi **`CMD` trong XML**

API này **không phải RESTful API**.

---

## 2. Nguyên tắc cốt lõi (quan trọng nhất)

> **Tất cả các thao tác (query / thêm / sửa / xoá) đều dùng HTTP `POST`.**
>
> **`CMD` trong XML mới là thứ quyết định hệ thống làm gì.**

---

## 3. Mapping nghiệp vụ thực tế

| Nghiệp vụ              | HTTP Method | CMD trong XML             |
| ---------------------- | ----------- | ------------------------- |
| Filter / Query dữ liệu | POST        | `GetRefData`              |
| Thêm dữ liệu           | POST        | `AddRefData`, `CreateXXX` |
| Sửa dữ liệu            | POST        | `UpdateRefData`           |
| Xoá dữ liệu            | POST        | `DeleteRefData`           |
| Thực thi rule / action | POST        | `ApplyXXX`, `ExecuteXXX`  |

📌 **Không dùng**: GET, PUT, DELETE trong giao tiếp trực tiếp với RK7 API.

---

## 4. Vì sao luôn là POST?

* XML payload dài, phức tạp → **không phù hợp GET**
* API thiết kế theo **RPC / Command pattern**
* Ra đời trước REST, ưu tiên:

  * Transaction
  * Logic nghiệp vụ
  * Payload lớn
* HTTP chỉ đóng vai trò **kênh truyền**

---

## 5. Ví dụ chuẩn

**HTTP**

```http
POST /rk7api
Content-Type: application/xml
```

**Body**

```xml
<RK7Query>
    <RK7CMD CMD="GetRefData" RefName="MENUITEMS">
        ...
    </RK7CMD>
</RK7Query>
```

---

## 6. Lưu ý quan trọng cho team

* Không cố “REST-hoá” RK7 API trực tiếp
* Nếu cần REST chuẩn → **bọc bằng adapter/service trung gian**
* Khi debug sai lệch dữ liệu:

  * Kiểm tra `CMD`
  * Không kiểm tra HTTP method

---

## 7. Một câu chốt để thống nhất tư duy

> **POST là phong bì.
> CMD trong XML là nội dung thư.**

---