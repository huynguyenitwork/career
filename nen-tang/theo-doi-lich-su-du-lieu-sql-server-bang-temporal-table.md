#  Biến database thành camera an ninh dữ liệu

# Mục tiêu

**20% thao tác → 80% hiệu quả:**

* Toàn bộ DB được bật Temporal Table
* SQL Server tự ghi lại mọi thay đổi
* Không sửa ứng dụng, không thêm trigger, không ảnh hưởng hiệu năng
* Có thể tra cứu **lịch sử toàn hệ thống**:

  * bảng nào vừa có thay đổi
  * thay đổi ở dòng nào
  * cột nào bị chỉnh
  * thời điểm xảy ra

---

# 1) Bật Temporal Table (CREATE) cho từng bảng

Dành cho bảng *chưa có* temporal.

```sql
ALTER TABLE EcomStore
ADD 
    SysStartTime datetime2 GENERATED ALWAYS AS ROW START HIDDEN 
        NOT NULL DEFAULT SYSUTCDATETIME(),
    SysEndTime datetime2 GENERATED ALWAYS AS ROW END HIDDEN 
        NOT NULL DEFAULT CONVERT(datetime2,'9999-12-31 23:59:59.9999999');

ALTER TABLE EcomStore
ADD PERIOD FOR SYSTEM_TIME (SysStartTime, SysEndTime);

ALTER TABLE EcomStore
SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.EcomStoreHistory));
```

📌 *Kết quả:*
Mỗi UPDATE hoặc DELETE → SQL tự tạo bản ghi lịch sử.

INSERT sẽ được ghi trong lịch sử khi bản đó bị UPDATE/DELETE lần đầu.

---

# 2) Hoàn tác (DROP) – trả bảng về “bình thường”

```sql
ALTER TABLE EcomStore
SET (SYSTEM_VERSIONING = OFF);

ALTER TABLE EcomStore
DROP PERIOD FOR SYSTEM_TIME;

ALTER TABLE EcomStore
DROP COLUMN SysStartTime, SysEndTime;

DROP TABLE IF EXISTS dbo.EcomStoreHistory;
```

---

# 3) Bật Temporal Table cho TẤT CẢ BẢNG TRONG DATABASE

Tự động thêm cột, bật period và tạo bảng lịch sử.

```sql
DECLARE @table NVARCHAR(128);

DECLARE cur CURSOR FOR
    SELECT t.name
    FROM sys.tables t
    WHERE t.temporal_type = 0
      AND t.is_ms_shipped = 0;

OPEN cur;
FETCH NEXT FROM cur INTO @table;

WHILE @@FETCH_STATUS = 0
BEGIN
    DECLARE @sql NVARCHAR(MAX) = '
        IF NOT EXISTS (SELECT * FROM sys.columns 
                       WHERE object_id = OBJECT_ID('''+@table+''') 
                         AND name = ''SysStartTime'')
        BEGIN
            ALTER TABLE ' + @table + '
            ADD 
                SysStartTime datetime2 GENERATED ALWAYS AS ROW START HIDDEN 
                    NOT NULL DEFAULT SYSUTCDATETIME(),
                SysEndTime datetime2 GENERATED ALWAYS AS ROW END HIDDEN 
                    NOT NULL DEFAULT (''9999-12-31 23:59:59.9999999'');

            ALTER TABLE ' + @table + '
            ADD PERIOD FOR SYSTEM_TIME (SysStartTime, SysEndTime);

            ALTER TABLE ' + @table + '
            SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.' + @table + 'History));
        END
    ';

    EXEC(@sql);
    FETCH NEXT FROM cur INTO @table;
END

CLOSE cur;
DEALLOCATE cur;
```

📌 Sau khi chạy:
Toàn DB trở thành "chế độ giám sát" – không cần đụng app.

---

# 4) Tra cứu lịch sử của 1 bảng

```sql
SELECT *
FROM EcomStore
FOR SYSTEM_TIME ALL
ORDER BY SysStartTime DESC;
```

---

# 5) Tra cứu lịch sử của TOÀN HỆ THỐNG

*(Phát hiện bảng nào có thay đổi trong ngày / giờ / tuần)*

## 5.1 Liệt kê bảng nào có bản ghi lịch sử mới hôm nay

```sql
SELECT 
    t.name AS TableName,
    h.name AS HistoryTable
FROM sys.tables t
JOIN sys.tables h ON t.history_table_id = h.object_id
WHERE t.temporal_type = 2   -- SYSTEM_VERSIONED
  AND EXISTS (
        SELECT 1
        FROM sys.dm_db_partition_stats ps
        WHERE ps.object_id = h.object_id
          AND ps.row_count > 0
    );
```

## 5.2 Xem thay đổi theo từng bảng (động)

Danh sách tất cả bản ghi thay đổi trong ngày cho toàn DB:

```sql
DECLARE @Start DATETIME2 = CAST(GETDATE() AS DATE);
DECLARE @End   DATETIME2 = DATEADD(DAY, 1, @Start);

SELECT 
    t.name AS TableName,
    h.name AS HistoryTable,
    @Start AS StartRange,
    @End AS EndRange
FROM sys.tables t
JOIN sys.tables h ON t.history_table_id = h.object_id
WHERE t.temporal_type = 2;
```

Sau đó, dùng template để query từng bảng:

```sql
SELECT *
FROM <HistoryTable>
WHERE SysStartTime BETWEEN @Start AND @End;
```

---

# 6) Tự động xem chi tiết CỘT NÀO THAY ĐỔI (Diff)

*(Không trigger, không code)*

Query dùng JSON để so sánh dữ liệu giữa bản hiện tại và bản lịch sử:

```sql
SELECT 
    t.Id,
    'Before' AS VersionType,
    h.*
FROM EcomStore FOR SYSTEM_TIME AS OF '2025-12-10T00:00:00' AS h
JOIN EcomStore AS t ON t.Id = h.Id

UNION ALL

SELECT 
    t.Id,
    'After' AS VersionType,
    t.*
FROM EcomStore AS t;
```

Có thể mở rộng thành diff engine nếu muốn.

---
