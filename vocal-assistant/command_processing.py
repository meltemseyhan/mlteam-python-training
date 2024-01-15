from openai_agent import OpenAIAgent

class CommandProcessing:
    def __init__(self) -> None:
        self.openai_agent = OpenAIAgent()

    def handle_command(self, command):
        return self.openai_agent.get_command_label(command)