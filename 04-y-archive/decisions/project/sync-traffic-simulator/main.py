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