# refagent api specification bản dùng chung

mục tiêu:
- làm tài liệu api chính thức
- dùng cho dev tích hợp
- bỏ toàn bộ phần phân tích nội bộ, chỉ giữ cái cần truyền

---

## 1. endpoint

```

POST /api/set-ref-data

````

---

## 2. headers

bắt buộc:
- x-source-service: <service_name>
- content-type: application/json

---

## 3. request body

### 3.1 cấu trúc chuẩn

```json
{
    "ActName": "<string>",
    "Payload": { }
}
````

---

### 3.2 actname

* kiểu: string
* bắt buộc
* là mã nghiệp vụ đã được đăng ký trong hệ thống
* quyết định loại dữ liệu trong payload

ví dụ:

```json
"ActName": "SaveMenuItem"
```

---

### 3.3 payload

* kiểu: object
* tùy chọn (phụ thuộc actname)
* hệ thống không áp đặt schema chung
* payload được chuyển nguyên vẹn tới handler tương ứng

---

## 4. callback result

### 4.1 callback url

* hệ thống sử dụng callback để trả kết quả xử lý
* callback url được cấu hình khi đăng ký service
* **không truyền callback url trong request**

ví dụ:

```
http://localhost:5003/api/refagent/callback-result
```

---

## 5. payload chuẩn – save menu item

### 5.1 cấu trúc tổng

```json
{
    "SyncTaskId": <number>,
    "MenuItem": {
        "<EntityName>": [
            {
                "Action": <number>,
                "Data": [ { ... } ]
            }
        ]
    }
}
```

---

### 5.2 synctaskid

* kiểu: number
* bắt buộc
* định danh cho một lần đồng bộ dữ liệu
* dùng để đối chiếu kết quả callback

---

### 5.3 entityname

các entity hỗ trợ:

* menuitem
* selectordetail
* generatedpropdata
* dishgroup

mỗi entity là một mảng các nhóm action.

---

### 5.4 action

* kiểu: number
* bắt buộc

giá trị:

* 1: create
* 2: update
* 3: hard_delete
* 4: soft_delete

---

### 5.5 data

* kiểu: array
* danh sách item cần xử lý
* mỗi phần tử đại diện một đối tượng nghiệp vụ

---

## 6. response (callback)

### 6.1 cấu trúc tổng

```json
{
    "SyncTaskId": <number>,
    "SuccessMenuItem": <boolean>,
    "Results": { }
}
```

---

### 6.2 results

```json
{
    "<EntityName>": [
        {
            "Action": <number>,
            "Items": [
                {
                    "Ident": "<string>",
                    "GuidString": "<string>",
                    "ErrorCode": "<string|null>",
                    "ErrorMessage": "<string|null>"
                }
            ]
        }
    ]
}
```

---

### 6.3 item result

* ident:

  * id phía hệ thống nguồn
* guidstring:

  * id phía hệ thống đích
* errorcode:

  * null: xử lý thành công
  * khác null: lỗi nghiệp vụ
* errormessage:

  * mô tả lỗi (nếu có)

---

## 7. quy ước xử lý

* api xử lý bất đồng bộ
* không trả kết quả chi tiết ngay lập tức
* lỗi từng item không làm hỏng toàn bộ request
* kết quả trả về theo từng entity và action

---

## 8. ghi chú sử dụng

* actname phải đúng theo cấu hình hệ thống
* payload phải đúng schema theo actname
* synctaskid phải duy nhất theo từng lần sync
* client phải xử lý callback để nhận kết quả

---

kết luận:
đây là api trung gian dùng để gửi dữ liệu nghiệp vụ theo hành vi (actname). api không xử lý logic, chỉ tiếp nhận – điều phối – và trả kết quả qua callback.


