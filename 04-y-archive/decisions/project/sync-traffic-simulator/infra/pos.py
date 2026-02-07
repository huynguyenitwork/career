import random

class POS:
    def receive(self, entity_id: str):
        # 20% chance không ACK
        if random.random() < 0.2:
            return None
        return "ACK"