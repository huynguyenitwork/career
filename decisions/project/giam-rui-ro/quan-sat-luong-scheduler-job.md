# quan sát luồng scheduler / job (tối giản)

## mục tiêu
- nhìn thấy thứ tự chạy thật của job theo từng store để giảm rủi ro ordering

loại:
- tối ưu hiệu năng
- xây logging system
- thay đổi nghiệp vụ

---

## phạm vi
- chỉ phục vụ dev senior tự quan sát
- chỉ dùng cho test luồng store
- không public, không report, không dashboard
- dùng xong xóa

---

## nguyên lý
- ghi dấu tạm thời vào db
- code chỉ có nhiệm vụ "đánh dấu"
- quyết định dựa trên timeline thật
- không suy đoán từ log rải rác

---

## cách làm chuẩn

### 1. bảng trace tạm
- mỗi dòng = 1 mốc job tại 1 thời điểm

```sql
CREATE TABLE _flow_trace (
    id bigint identity primary key,
    store_id int,
    job_type varchar(50),
    phase varchar(30),
    status varchar(20),
    created_at datetime default getdate()
);
````

dùng để làm gì:

* tạo timeline theo store

loại:

* field không phục vụ sắp xếp thời gian hoặc phân biệt job

---

### 2. stored procedure ghi dấu

* chuẩn hóa điểm ghi
* tránh logic rải trong code

```sql
CREATE PROCEDURE sp_flow_trace
 @store_id int,
 @job_type varchar(50),
 @phase varchar(30),
 @status varchar(20)
AS
INSERT INTO _flow_trace(store_id, job_type, phase, status)
VALUES (@store_id, @job_type, @phase, @status);
```

---

### 3. helper c# tối giản

* chỉ gọi proc
* không xử lý logic

```csharp
public static async Task TraceFlowAsync(
    IADOServices adoServices,
    int? storeId,
    string jobType,
    string phase,
    string status)
{
    DCFields AParams = new DCFields
    {
        { "store_id", storeId },
        { "job_type", jobType },
        { "phase", phase },
        { "status", status }
    };

    await adoServices.ExecProc("sp_flow_trace", AParams);
}
```

chèn ở các điểm quyết định thứ tự:

```csharp
await Utils.TraceFlowAsync(_adoServices, null, "CREATE_STORE", "START", "RUN");
await Utils.TraceFlowAsync(_adoServices, storeId, "CREATE_STORE", "CALL_POS", "RUN");
await Utils.TraceFlowAsync(_adoServices, null, "CREATE_STORE", "END", "SUCCESS");
```

---

### 4. quan sát

* chỉ query, không phân tích phức tạp

```sql
SELECT *
FROM _flow_trace
WHERE store_id = 123
ORDER BY created_at;
```

dùng để biết:

* job nào chạy trước
* có chồng job không
* có chạy sai điều kiện không

---

### 5. kết luận nhanh

* thấy sai thứ tự → có rủi ro ordering
* không thấy → tiếp tục test nghiệp vụ khác

---

### 6. dọn sạch

* không để lại dấu vết

```sql
DROP TABLE _flow_trace;
DROP PROCEDURE sp_flow_trace;
```

---

## câu chốt

* không debug bằng cảm giác
* không đọc log hỗn loạn
* chỉ nhìn timeline thật rồi quyết

