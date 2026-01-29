## 3 cách xử lý lỗi restore postgres (role không tồn tại)

### cách 1: tạo role trước khi restore

**làm**: `create role dcorp_dev;` rồi restore lại.

**ưu**

- giữ nguyên quyền như db gốc
- phù hợp môi trường gần/prod

**nhược**

- phải quản lý role
- không cần thiết cho dev/local

**dùng khi**

- cần tái tạo chính xác quyền truy cập

---

### cách 2: bỏ acl và owner khi restore (khuyến nghị cho dev)

**làm**:
kết nối và restore đồng thời
```bash
pg_restore -U postgres -h localhost -p 5432 --no-owner --no-acl -d your_db your_dump
```
**ưu**

- nhanh, sạch, không dính role cũ
- phù hợp 80% trường hợp dev/test

**nhược**

- không giữ lại quyền cũ

**dùng khi**

- dev, local, test
- chỉ cần schema + data

---

### cách 3: restore xong rồi grant lại

**làm**: restore bình thường, sau đó grant cho role hiện tại.

**ưu**

- không cần restore lại
- xử lý khi đã lỡ làm

**nhược**

- set quyền thủ công
- dễ lệch so với db gốc

**dùng khi**

- db đã restore xong, không muốn chạy lại

---

## kết luận nhanh

- dev/local: **cách 2**
- gần prod: **cách 1**
- lỡ restore rồi: **cách 3**

nếu cần, mình có thể viết sẵn **1 lệnh restore chuẩn dùng chung cho team dev** hoặc **checklist backup/restore để không gặp lại lỗi này**.
