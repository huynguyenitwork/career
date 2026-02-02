# mẫu thiết kế payload callback skytool ⇔ refagent

## 1. payload chiều a → b (skytool → refagent)

### mục tiêu

* gửi yêu cầu xử lý async
* **khai báo rõ callback contract**
* refagent không cần config gì thêm

---

### payload đề xuất

```json
{
    "ActName": "SaveDiscount",
    "Payload": {
        "SyncTaskId": 666,
        "Discount": {
            "Action": 4,
            "DiscountItem": {
                "Item": {
                    "Name": "[test] discount 14-01-2026 15:01",
                    "genSAPCODE": "[TEST]-sapcode-1401261444",
                    "Status": 1,
                    "Parent": 1108039
                }
            },
            "DiscountTypeItem": {
                "Item": {
                    "Code": 1393,
                    "Status": 1
                }
            }
        }
    },
    "Callback": {
        "Url": "https://skytool/api/refagent/callback",
        "Method": "POST",
        "TimeoutSeconds": 10,
        "Retry": {
            "MaxAttempts": 3,
            "IntervalSeconds": 30
        },
        "Secret": "skytool-refagent-shared-secret"
    }
}
```

---

### giải thích nhanh

* `ActName`

  * định danh nghiệp vụ, giúp callback không cần đoán ngữ cảnh
* `SyncTaskId`

  * id nội bộ của skytool, dùng map trạng thái
* `Callback.Url`

  * **hợp đồng callback**, không suy luận
* `Secret`

  * dùng ký callback (hmac / hash), tránh fake request
* `Retry`

  * refagent retry có kiểm soát, tránh spam

---

## 2. response ngay sau khi nhận request (b → a, synchronous)

```json
{
    "success": true,
    "message": "request queued successfully. processing will happen asynchronously.",
    "data": {
        "requestId": "2fed7812-83a3-40c7-b764-6cb82eb640aa"
    }
}
```

* `requestId`

  * id xử lý phía refagent
  * dùng để trace log + correlate callback

---

## 3. payload callback chiều b → a (refagent → skytool)

### mục tiêu

* báo kết quả xử lý cuối cùng
* **idempotent**
* đủ thông tin để skytool cập nhật trạng thái

---

### callback payload (success)

```json
{
    "requestId": "2fed7812-83a3-40c7-b764-6cb82eb640aa",
    "SyncTaskId": 666,
    "ActName": "SaveDiscount",
    "Status": "success",
    "Result": {
        "RefId": 998812,
        "Message": "discount saved successfully"
    },
    "Error": null,
    "ProcessedAt": "2026-01-14T08:15:42Z",
    "Signature": "hmac-sha256-signature"
}
```

---

### callback payload (failed)

```json
{
    "requestId": "2fed7812-83a3-40c7-b764-6cb82eb640aa",
    "SyncTaskId": 666,
    "ActName": "SaveDiscount",
    "Status": "failed",
    "Result": null,
    "Error": {
        "Code": "DISCOUNT_NOT_FOUND",
        "Message": "discount parent does not exist"
    },
    "ProcessedAt": "2026-01-14T08:15:42Z",
    "Signature": "hmac-sha256-signature"
}
```

---

## 4. nguyên tắc xử lý callback phía a (skytool)

* callback endpoint **phải idempotent**
* map theo:

  * `requestId` (refagent)
  * `SyncTaskId` (skytool)
* nếu nhận callback trùng:

  * ignore hoặc update cùng trạng thái
* verify `Signature` trước khi xử lý

nói thẳng:

> callback không ký thì coi như thư nặc danh

---

## 5. những thứ cố tình không làm (và nên tránh)

* không dùng `referer`, `origin`, `host` để suy ra callback
* không hardcode domain skytool trong refagent
* không callback thiếu `requestId`
* không callback thiếu trạng thái cuối cùng

---

## 6. chốt lại một câu cho team

* callback là **contract theo request**
* payload nói rõ mọi thứ, config chỉ là phụ trợ
* refagent xử lý, skytool quyết định

nếu bước tiếp theo bạn cần:

* chuẩn hóa **hmac signature spec**
* vẽ **sequence diagram đúng chuẩn pm**
* hoặc đóng gói thành **api contract v1 markdown cho team**

mình đi tiếp được ngay, không cần đà.
