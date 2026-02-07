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