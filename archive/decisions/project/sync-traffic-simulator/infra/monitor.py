class Monitor:
    def metric(self, name: str):
        print(f"[METRIC] {name}")

    def log(self, message: str):
        print(f"[LOG] {message}")