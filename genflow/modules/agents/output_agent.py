from modules.agents.utils.audio import text_to_speech_openai

class OutputAgent:
    def __init__(self, output_path, eval_path):
        self.output_path = output_path
        self.eval_path = eval_path

    def write_summary(self, text):
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(text)

        audio_path = text_to_speech_openai(text, "genflow/outputs/text_audio.mp3")
        print(f"[OutputAgent] Audio saved to {audio_path}")

    def write_evaluation(self, text):
        with open(self.eval_path, "w", encoding="utf-8") as f:
            f.write(text)
