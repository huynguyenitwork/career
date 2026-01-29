# so sánh thiết kế callback skytool → refagent

## 1. bối cảnh hiện tại (đặt nền cho khỏi lạc)

* skytool gọi api sang refagent
* refagent xử lý async
* refagent callback kết quả về skytool
* response hiện tại chỉ trả `requestId`, chưa có callback contract rõ ràng

payload hiện tại (a → b):

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
    }
}
```

refagent trả về:

```json
{
    "success": true,
    "message": "SetRefData request with ActName 'SaveDiscount' queued successfully. Processing and callback will happen asynchronously.",
    "data": {
        "requestId": "2fed7812-83a3-40c7-b764-6cb82eb640aa"
    }
}
```

---

## 2. phương án 1: truyền callback ngay khi gọi từ skytool

### 2.1 mô tả ngắn

* skytool gửi kèm thông tin callback trong request
* refagent không cần cấu hình domain skytool
* callback là một phần của hợp đồng api

### 2.2 payload đề xuất (mở rộng từ payload hiện tại)

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
        "Method": "POST"
    }
}
```

### 2.3 ưu điểm

* loose coupling đúng nghĩa
* refagent zero-config
* mỗi request tự mang định mệnh của nó
* scale môi trường dễ (dev / uat / prod không đụng code refagent)
* debug cực dễ vì callback explicit

### 2.4 nhược điểm

* skytool phải expose endpoint public
* cần ký callback để tránh bị fake
* payload dài hơn một chút (nhưng cái này là non-issue)

---

## 3. phương án 2: cấu hình callback cố định trong appsettings của refagent

### 3.1 mô tả ngắn

* refagent có config sẵn:

  * `SkytoolCallbackUrl`
* mọi callback đều bắn về url này
* skytool không cần truyền callback khi gọi

### 3.2 ưu điểm

* payload gọn
* code refagent callback đơn giản
* dễ làm ở giai đoạn rất sớm

### 3.3 nhược điểm (đây là phần đau)

* tight coupling
* đổi domain skytool là redeploy refagent
* multi-env là ác mộng config
* không hỗ trợ nhiều caller trong tương lai
* refagent biết quá nhiều về skytool

nói thẳng: **thuận tiện ngắn hạn, trả giá dài hạn**.

---

## 4. so sánh nhanh theo bảng tư duy 20/80

* khả năng mở rộng:

  * truyền callback: rất tốt
  * appsettings: kém
* độ độc lập service:

  * truyền callback: cao
  * appsettings: thấp
* chi phí vận hành dài hạn:

  * truyền callback: thấp
  * appsettings: cao
* phù hợp hệ thống lớn:

  * truyền callback: có
  * appsettings: không

---

## 5. nên chọn phương án nào?

### kết luận dứt khoát

* **nên chọn: truyền callback ngay khi gọi từ skytool**

### vì sao?

* callback là **hợp đồng theo request**, không phải **niềm tin cấu hình**
* refagent là service xử lý, không phải service đoán nhà người khác
* tương lai:

  * thêm caller khác ngoài skytool
  * tách hệ thống
  * đổi domain
  * thêm version api
    → phương án appsettings sẽ cản đường

nói kiểu đời:

> config là gánh nặng, payload là sự thật

---

## 6. gợi ý nâng cấp thêm (đi trước một bước)

* thêm `Callback.Secret` hoặc `Signature`
* callback payload trả về:

  * `requestId`
  * `SyncTaskId`
  * `ActName`
  * `Status`
  * `Error` (nếu có)
* callback endpoint của skytool xử lý idempotent

---

## 7. chốt hạ

* nếu đây là poc nhỏ, sống vài tuần: appsettings còn chịu được
* nếu đây là xương sống tích hợp: **truyền callback là con đường đúng**
* refactor sớm rẻ hơn rewrite muộn

nếu bạn muốn, bước tiếp theo mình có thể:

* chuẩn hóa **callback payload schema**
* viết **sequence diagram đúng chuẩn pm đọc phát hiểu**
* hoặc draft luôn **api contract v1** cho refagent

đường này đi rồi là khỏi quay đầu.
