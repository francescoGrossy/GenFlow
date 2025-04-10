import yaml
from modules.agents.input_agent import InputAgent
from modules.agents.summarizer_agent import SummarizerAgent
from modules.agents.evaluator_agent import EvaluatorAgent
from modules.agents.output_agent import OutputAgent
from modules.agents.utils.audio import (
    record_audio_from_microphone,
    speech_to_text_openai,
    text_to_speech_openai,
    play_audio_file,
)

class AgentOrchestrator:
    def __init__(self, config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        self.model = self.config["model"]

    def build_prompt(self, input_text):
        prompt = ""

        # Output format
        output_format = self.config.get("output_format", "plain_text")
        structured = self.config.get("structured_output", False)
        few_shot = self.config.get("few_shot", False)

        # Structured output
        if structured:
            prompt += "Provide the output in JSON format with fields: title, summary, keywords.\n\n"
        elif output_format == "markdown":
            prompt += "Provide the output in markdown format.\n\n"
        else:
            prompt += "Provide a direct response.\n\n"

        # Few-shot example
        if few_shot:
            prompt += (
                "**Example**:\n"
                "Input: The stock market experienced a significant fluctuation today.\n"
                "Output:\n"
                "{\n"
                '  "title": "Market Volatility",\n'
                '  "summary": "The market underwent strong oscillations due to geopolitical tensions.",\n'
                '  "keywords": ["market", "volatility"]\n'
                "}\n\n"
            )

        # Task description and actual input
        if self.config.get("voice_input_description", False):
            audio_path = record_audio_from_microphone()
            spoken_description = speech_to_text_openai(audio_path)
            self.config["description"] = spoken_description
            print(f"[Orchestrator] Recorded description: {spoken_description}")
        else:
            spoken_description = self.config.get("description", "No description provided.")

        prompt += f"Task: {spoken_description}\n\nInput:\n{input_text}"

        return prompt

    def run(self):
        # Initialize agents
        input_agent = InputAgent(self.config["input_file"])
        summarizer = SummarizerAgent(self.config)
        evaluator = EvaluatorAgent(self.config, self.model)
        output_agent = OutputAgent("genflow/outputs/output.md", "genflow/outputs/evaluation.md")

        # Read input
        input_text = input_agent.run()

        # Build prompt dynamically
        prompt = self.build_prompt(input_text)

        # Run summarizer with prompt
        summary = summarizer.run(prompt)
        output_agent.write_summary(summary)

        if self.config.get("voice_output_summary", False):
            summary_audio_path = text_to_speech_openai(summary)
            print(f"[Orchestrator] Audio saved to {summary_audio_path}")
            play_audio_file(summary_audio_path)

        # Run evaluation if enabled
        if self.config.get("evaluation"):
            evaluation = evaluator.run(self.config["description"], input_text, summary)
            output_agent.write_evaluation(evaluation)

        print("GenFlow completed successfully.")
