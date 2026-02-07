## 1. cây thư mục dự án

```
sync-traffic-simulator/
│
├── main.py                 # entry point – chạy mô phỏng
│
├── core/
│   ├── __init__.py
│   ├── state.py            # state machine
│   ├── event.py            # event definition
│   ├── entity.py           # entity (xe)
│
├── engine/
│   ├── __init__.py
│   ├── sync_engine.py      # trung tâm điều phối
│   ├── auto_healer.py      # phản xạ tự lành
│
├── infra/
│   ├── __init__.py
│   ├── pos.py              # hệ nhận (POS)
│   ├── monitor.py          # monitoring / metrics
│
└── README.md               # mô tả nhanh
```

không thừa, không thiếu.
mỗi folder = **một tầng tư duy**.

---

## 2. code chi tiết từng file

### `core/state.py`

```python
from enum import Enum, auto

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

---

### `core/event.py`

```python
from enum import Enum, auto

class EventType(Enum):
    CREATE = auto()
    UPDATE = auto()
    DISABLE = auto()
```

---

### `core/entity.py`

```python
from core.state import State

class Entity:
    def __init__(self, business_id: str):
        self.id = business_id
        self.state = None
        self.enabled = True

    def disable(self):
        self.enabled = False
```

---

## 3. hạ tầng

### `infra/monitor.py`

```python
class Monitor:
    def metric(self, name: str):
        print(f"[METRIC] {name}")

    def log(self, message: str):
        print(f"[LOG] {message}")
```

---

### `infra/pos.py`

```python
import random

class POS:
    def receive(self, entity_id: str):
        # 20% chance không ACK
        if random.random() < 0.2:
            return None
        return "ACK"
```

---

## 4. auto healing

### `engine/auto_healer.py`

```python
from core.state import State

class AutoHealer:

    def retry(self, entity):
        print(f"[HEAL] Retry entity={entity.id}")
        entity.state = State.FAILED_RETRYABLE

    def skip(self, entity, reason: str):
        print(f"[HEAL] Skip entity={entity.id} reason={reason}")
        entity.state = State.SKIPPED
```

---

## 5. trái tim hệ thống

### `engine/sync_engine.py`

```python
from core.event import EventType
from core.entity import Entity
from core.state import State
from infra.monitor import Monitor
from infra.pos import POS
from engine.auto_healer import AutoHealer


class SyncEngine:
    def __init__(self):
        self.entities = {}
        self.idempotency_keys = set()
        self.monitor = Monitor()
        self.pos = POS()
        self.healer = AutoHealer()

    def handle_event(self, business_id, event_type, payload=None):
        key = (business_id, event_type)

        # (1) Duplicate
        if key in self.idempotency_keys:
            self.monitor.metric("duplicate_event")
            return
        self.idempotency_keys.add(key)

        entity = self.entities.get(business_id)

        # (2) Out of order
        if event_type == EventType.UPDATE and not entity:
            self.monitor.metric("out_of_order_event")
            return

        # CREATE
        if event_type == EventType.CREATE:
            entity = Entity(business_id)
            self.entities[business_id] = entity
            entity.state = State.RECEIVED

        # DISABLE
        if event_type == EventType.DISABLE and entity:
            entity.disable()

        # (3) Precondition fail
        if entity and not entity.enabled:
            self.monitor.metric("precondition_failed")
            self.healer.skip(entity, "entity_disabled")
            return

        # (6) Contract mismatch
        if payload and payload.get("invalid_contract"):
            self.monitor.metric("contract_mismatch")
            entity.state = State.FAILED_NON_RETRYABLE
            return

        # Send to POS
        entity.state = State.SENT
        ack = self.pos.receive(entity.id)

        # (4) No ACK
        if not ack:
            self.monitor.metric("ack_timeout")
            self.healer.retry(entity)
            return

        entity.state = State.ACKED

        # (5) Not visible to user
        from random import random
        if random() < 0.2:
            self.monitor.metric("not_visible")
            self.healer.retry(entity)
            return

        entity.state = State.VISIBLE
        self.monitor.log(f"Entity {entity.id} is visible to user")
```

---

## 6. entry point – chạy phim

### `main.py`

```python
from engine.sync_engine import SyncEngine
from core.event import EventType

engine = SyncEngine()

print("\n--- CREATE STORE_1 ---")
engine.handle_event("STORE_1", EventType.CREATE)

print("\n--- DUPLICATE CREATE ---")
engine.handle_event("STORE_1", EventType.CREATE)

print("\n--- OUT OF ORDER UPDATE ---")
engine.handle_event("STORE_X", EventType.UPDATE)

print("\n--- CONTRACT MISMATCH ---")
engine.handle_event("STORE_2", EventType.CREATE, payload={"invalid_contract": True})

print("\n--- DISABLE BEFORE SEND ---")
engine.handle_event("STORE_3", EventType.CREATE)
engine.handle_event("STORE_3", EventType.DISABLE)
engine.handle_event("STORE_3", EventType.UPDATE)

print("\n--- RANDOM ACK / VISIBILITY ---")
for _ in range(5):
    engine.handle_event("STORE_4", EventType.CREATE)
```

Chạy:

```
python main.py
```

Bạn sẽ **thấy metric + hành vi khác nhau mỗi lần chạy**, đúng tinh thần *đời không deterministic*.

---

## 7. vì sao cấu trúc này “đúng bài”?

* **state tách riêng** → dễ reason
* **monitoring không dính business** → thay tool không đau
* **auto-healing không nằm trong handler** → tránh retry mù
* **syncengine chỉ điều phối** → không ôm đồm

đây là **phiên bản giao thông đô thị tối giản**, nhưng:

* kéo lên production được
* nhét vào ci test được
* mở rộng chaos test được

---