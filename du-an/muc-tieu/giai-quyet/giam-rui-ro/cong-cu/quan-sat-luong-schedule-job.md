#  quan sát luồng **scheduler / job**

## 1. mục tiêu (chỉ 1 dòng)

**giảm rủi ro bằng cách nhìn thấy thứ tự chạy thật của job theo từng store.**

không tối ưu hiệu năng.
không xây logging system.
không thay đổi nghiệp vụ.

---

## 2. phạm vi (để không dẫm chân ai)

* chỉ phục vụ **cá nhân dev senior quan sát**
* chỉ dùng cho **test luồng store**
* không public, không report, không dashboard
* có thể xóa bất cứ lúc nào

---

## 3. cách làm tổng thể (overview)

> đặt **1 camera giao thông tạm thời** trong db
> → code c# chỉ gọi ghi dấu
> → quan sát bằng query
> → ra quyết định
> → xóa

---

## 4. cách làm ngắn gọn

### 1. tạo bảng tạm trong db

ghi dấu job chạy khi nào, ở bước nào.

```sql
CREATE TABLE _flow_trace (
    id bigint identity primary key,
    store_id int,
    job_type varchar(50),
    phase varchar(30),
    status varchar(20),
    created_at datetime default getdate()
);
```

---

### 2. tạo stored procedure để ghi

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
### 3. c# chỉ gọi
helper tối giản
```csharp
public static async Task TraceFlowAsync(
    IADOServices adoServices,
    int? storeId,
    string jobType,
    string phase,
    string status,
    string note = null)
{

    DCFields AParams = new DCFields
    {
        { "store_id", storeId },
        { "job_type", jobType },
        { "phase", phase },
        { "status", status },
        { "note", note }
    };

    await adoServices.ExecProc(
                "sp_flow_trace",
                AParams
            );
}
```


chèn ở các điểm quan trọng của job.

```csharp

await Utils.TraceFlowAsync(_adoServices, null, "CREATE_STORE", "START", "RUN");
await Utils.TraceFlowAsync(_adoServices, storeId, "CREATE_STORE", "CALL_POS", "RUN");
await Utils.TraceFlowAsync(_adoServices, null, "CREATE_STORE", "END", "SUCCESS");
```

---

### 4. quan sát luồng

```sql
SELECT *
FROM _flow_trace
WHERE store_id = 123
ORDER BY created_at;
```

nhìn để biết:

* job nào chạy trước
* có job chạy khi job trước chưa xong không
* có chạy sai điều kiện không

---

### 5. ra quyết định

* thấy sai thứ tự → kết luận có rủi ro ordering
* không thấy → yên tâm test tiếp

---

### 6. xong thì xóa

```sql
DROP TABLE _flow_trace;
DROP PROCEDURE sp_flow_trace;
```

---

## câu chốt

không debug bằng cảm giác.
không đọc log hỗn loạn.
chỉ nhìn timeline thật rồi quyết.
