# mini project – timeout & cancel

## 1. vấn đề cốt lõi

* gọi service bên ngoài **có thể treo / chậm / không phản hồi**
* nếu **chờ mãi**:

  * treo request
  * tắc worker
  * lan sự cố sang toàn hệ thống
* giải pháp bắt buộc:

  * **timeout rõ ràng**
  * **cancel thật sự**, không chỉ log

---

## 2. nguyên lý quan trọng

* **timeout phải hủy task đang chạy**, không chỉ trả lỗi
* **cancel là hành động chủ động**, không phụ thuộc timeout
* **processing đang chạy thì không retry**
* không cancel được → async chưa đúng nghĩa

---

## 3. cấu trúc project (tối giản, đúng chất)

```
timeout_cancel_demo/
│
├── app/
│   ├── service.py        # external service giả lập
│   ├── safe_call.py      # logic timeout + cancel
│
├── tests/
│   └── test_cases.py     # các case thực tế
│
└── main.py               # entry point demo
```

---

### 3.1. external service (giả lập api ngoài)

`app/service.py`

```python
import asyncio

async def external_service(delay: int):
    """
    Giả lập service bên ngoài:
    - delay nhỏ: OK
    - delay lớn: coi như treo
    """
    print(f"[external] start, delay={delay}s")
    await asyncio.sleep(delay)
    print("[external] done")
    return "OK"
```

---

### 3.2. safe call – timeout + cancel

`app/safe_call.py`

```python
import asyncio
from app.service import external_service

class ExternalTimeout(Exception):
    pass

async def safe_call(delay: int, timeout: int):
    """
    Gọi external service có timeout.
    Timeout xảy ra => task bị cancel.
    """
    try:
        return await asyncio.wait_for(
            external_service(delay),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        print("[safe_call] timeout, task cancelled")
        raise ExternalTimeout("External service timeout")
```

**đây là xương sống của project.**
`asyncio.wait_for` = timeout + cancel thật sự.

---

### 3.3. test case thực tế

`tests/test_cases.py`

```python
import asyncio
from app.safe_call import safe_call, ExternalTimeout

async def case_success():
    print("\n--- CASE SUCCESS ---")
    result = await safe_call(delay=2, timeout=5)
    print("result:", result)

async def case_timeout():
    print("\n--- CASE TIMEOUT ---")
    try:
        await safe_call(delay=10, timeout=3)
    except ExternalTimeout as e:
        print("handled:", e)

async def case_cancel():
    print("\n--- CASE CANCEL ---")
    task = asyncio.create_task(
        safe_call(delay=10, timeout=20)
    )

    await asyncio.sleep(2)
    print("cancel task manually")
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("task cancelled cleanly")
```

---

### 3.4. entry point chạy demo

`main.py`

```python
import asyncio
from tests.test_cases import (
    case_success,
    case_timeout,
    case_cancel
)

async def main():
    await case_success()
    await case_timeout()
    await case_cancel()

if __name__ == "__main__":
    asyncio.run(main())
```

---

### 3.5. Chạy project

```bash
python main.py
```

kết quả bạn sẽ thấy:

* case success chạy bình thường
* case timeout **không chờ hết delay**
* case cancel **dừng ngay**, không zombie task

---

## 4. áp dụng thực tế

dùng cho:

* api gọi service khác
* consumer queue
* background job
* batch processing

không dùng cho:

* logic nội bộ chạy rất nhanh
* processing đã hoàn tất

---

## 5. checklist khi review code

* có timeout không?
* timeout có cancel task không?
* có phân biệt timeout và business error không?
* có tránh retry khi đang processing không?

---

## 6. câu chốt để nhớ

> **timeout là để bảo vệ hệ thống, không phải để sửa lỗi.**
> **cancel được thì hệ thống mới sống lâu.**

tài liệu này đủ để:

* giải thích với team
* review pr
* viết guideline nội bộ