from modules.executor import call_openai_model

class SummarizerAgent:
    def __init__(self, config):
        self.prompt = config["description"]
        self.model = config["model"]

    def run(self, prompt):
        return call_openai_model(prompt, model=self.model)
