from core.state import State

class AutoHealer:

    def retry(self, entity):
        print(f"[HEAL] Retry entity={entity.id}")
        entity.state = State.FAILED_RETRYABLE

    def skip(self, entity, reason: str):
        print(f"[HEAL] Skip entity={entity.id} reason={reason}")
        entity.state = State.SKIPPED