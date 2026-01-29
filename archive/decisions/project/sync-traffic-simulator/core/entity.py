from core.state import State

class Entity:
    def __init__(self, business_id: str):
        self.id = business_id
        self.state = None
        self.enabled = True

    def disable(self):
        self.enabled = False