**6 rủi ro giao thông–dữ liệu**
## mục tiêu

> **chạy được – nhìn thấy hành vi – hiểu cơ chế monitoring + auto-healing**

không cần database, không cần message broker thật.
ta dùng **in-memory + log + state machine** để não tập trung vào bản chất.

---

## 0. ý tưởng mini project (trước khi code)

### vai diễn

* `Event` = xe
* `Entity` = chiếc xe có biển số
* `SyncEngine` = trung tâm điều phối
* `POS` = bến nhận hàng
* `Monitor` = camera + bảng điện tử
* `AutoHealer` = phản xạ giao thông

### 6 rủi ro sẽ mô phỏng

1. trùng xe (duplicate)
2. xe tới sai thứ tự (out of order)
3. đường đã đóng (precondition fail)
4. không ký nhận (no ack)
5. có hàng nhưng không thấy
6. xe không đạt tải trọng (contract mismatch)

---

## 1. định nghĩa state & event

```python
from enum import Enum, auto
import time
import random
```

```python
class State(Enum):
    RECEIVED = auto()
    VALIDATED = auto()
    SENT = auto()
    ACKED = auto()
    VISIBLE = auto()
    FAILED_RETRYABLE = auto()
    FAILED_NON_RETRYABLE = auto()
    SKIPPED = auto()
```

```python
class EventType(Enum):
    CREATE = auto()
    UPDATE = auto()
    DISABLE = auto()
```

---

## 2. entity = chiếc xe có biển số

```python
class Entity:
    def __init__(self, business_id):
        self.id = business_id
        self.state = None
        self.enabled = True
```

---

## 3. pos – bến nhận hàng (có thể không ký)

```python
class POS:
    def receive(self, entity):
        # 20% chance không ký nhận
        if random.random() < 0.2:
            return None
        return "ACK"
```

---

## 4. monitor – camera giao thông

```python
class Monitor:
    def log(self, msg):
        print(f"[MONITOR] {msg}")

    def metric(self, name):
        print(f"[METRIC] {name}")
```

---

## 5. autohealer – phản xạ hệ thống

```python
class AutoHealer:
    def retry(self, entity):
        print(f"[HEAL] Retry entity {entity.id}")

    def skip(self, entity, reason):
        print(f"[HEAL] Skip {entity.id} | reason={reason}")
        entity.state = State.SKIPPED
```

---

## 6. syncengine – trung tâm điều phối (trái tim)

```python
class SyncEngine:
    def __init__(self):
        self.entities = {}
        self.idempotency_keys = set()
        self.pos = POS()
        self.monitor = Monitor()
        self.healer = AutoHealer()
```

---

## 7. xử lý event – nơi 6 rủi ro xuất hiện

```python
    def handle_event(self, business_id, event_type, payload=None):
        key = (business_id, event_type)

        # (1) Duplicate
        if key in self.idempotency_keys:
            self.monitor.metric("duplicate_event")
            return
        self.idempotency_keys.add(key)

        entity = self.entities.get(business_id)
```

---

### (2) out of order

```python
        if event_type == EventType.UPDATE and not entity:
            self.monitor.metric("out_of_order")
            return
```

---

### create entity

```python
        if event_type == EventType.CREATE:
            entity = Entity(business_id)
            self.entities[business_id] = entity
            entity.state = State.RECEIVED
```

---

### (3) precondition fail

```python
        if entity and not entity.enabled:
            self.monitor.metric("precondition_failed")
            self.healer.skip(entity, "disabled")
            return
```

---

### (6) contract mismatch

```python
        if payload and payload.get("invalid_contract"):
            self.monitor.metric("contract_mismatch")
            entity.state = State.FAILED_NON_RETRYABLE
            return
```

---

### gửi sang pos

```python
        entity.state = State.SENT
        ack = self.pos.receive(entity)
```

---

### (4) no ack

```python
        if not ack:
            self.monitor.metric("ack_timeout")
            entity.state = State.FAILED_RETRYABLE
            self.healer.retry(entity)
            return
```

---

### ack thành công → nhưng…

```python
        entity.state = State.ACKED
```

---

### (5) có dữ liệu nhưng user không thấy

```python
        if random.random() < 0.2:
            self.monitor.metric("not_visible")
            self.healer.retry(entity)
            return
```

---

### happy path

```python
        entity.state = State.VISIBLE
        self.monitor.log(f"Entity {entity.id} visible to user")
```

---

## 8. chạy mô phỏng 6 rủi ro

```python
engine = SyncEngine()

print("\n--- CREATE ---")
engine.handle_event("STORE_1", EventType.CREATE)

print("\n--- DUPLICATE CREATE ---")
engine.handle_event("STORE_1", EventType.CREATE)

print("\n--- OUT OF ORDER UPDATE ---")
engine.handle_event("STORE_X", EventType.UPDATE)

print("\n--- CONTRACT MISMATCH ---")
engine.handle_event("STORE_2", EventType.CREATE, payload={"invalid_contract": True})

print("\n--- NO ACK / NOT VISIBLE RANDOM ---")
for _ in range(5):
    engine.handle_event("STORE_3", EventType.CREATE)
```

---

## 9. bạn đang học được gì từ mini project này?

* **Monitoring không phải log**, mà là *tên rủi ro*
* **Auto-healing không phải retry**, mà là *quyết định có não*
* **State quan trọng hơn endpoint**
* **80% sự cố tái hiện được bằng mô phỏng nhỏ**

bạn có thể:

* thay `print` bằng Prometheus metric
* thay `POS` bằng mock API
* thay memory bằng Redis
* giữ nguyên **tư duy**

---

## câu chốt cho dân xây hệ thống

framework thay đổi.
cloud thay đổi.
tool đổi xoành xoạch.

nhưng **6 kiểu kẹt xe này không đổi**.

viết được mini project này nghĩa là:

> bạn không còn “đồng bộ dữ liệu”,
> bạn đang **điều phối một thành phố đang sống**.
> thử nghiệm với **BDD test + chaos test**.
