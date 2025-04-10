from modules.executor import call_openai_model

class EvaluatorAgent:
    def __init__(self, config, model):
        self.criteria = config.get("evaluation", [])
        self.model = model

    def run(self, task_description, input_text, generated_output):
        criteria_text = "\n".join([f"- {c}" for c in self.criteria])
        prompt = (
            f"Evaluate the following output with respect of these criterias:\n{criteria_text}\n\n"
            f"### Task\n{task_description}\n\n"
            f"### Input\n{input_text}\n\n"
            f"### Output\n{generated_output}\n\n"
            f"Assign a mark from 1 to 5 to each criteria, justifying it. Answer in markdown."
        )
        return call_openai_model(prompt, model=self.model)
