class InputAgent:
    def __init__(self, path):
        self.path = path

    def run(self):
        with open(self.path, "r", encoding="latin1") as f:
            return f.read()

