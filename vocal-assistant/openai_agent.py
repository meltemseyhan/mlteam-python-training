import openai
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIAgent:
    def __init__(self, model="gpt-3.5-turbo") -> None:
        self.model = model
        self.client = openai.OpenAI()
        self.memory = []
        self.memory_limit = 10

    def __create_chat_completion(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
    
    def get_response(self, command):
        messages=[
            {"role": "system", "content": "You are a vocal assistant. You have to answer in a simple, efficient and concise way. Your answer should not take more than 30 seconds to say out loud"},
        ]
        # Add the memory of previous interactions to the request
        messages.extend(self.memory)
        messages.append({"role": "user", "content": command})

        assistant_reply = self.__create_chat_completion(messages)

        if assistant_reply:
            # Add the question from user, and reply from GPT to the memory 
            self.memory.extend({"role": "user", "content": command}, {"role": "assistant", "content": assistant_reply})
            # Make sure that memory is always in limits. If the limit is 10, then it will take most recent 10 elements.
            self.memory = self.memory[-self.memory_limit:]
        return assistant_reply
    
    def get_command_label(self, command):
        messages=[
            {"role": "system", "content": "You are a vocal assistant."},
            {"role": "system", "content": "Your role is to classify the user's command and return only the corresponding label."},
            {"role": "system", "content": "The labels are: to-do list, normal question"},
            {"role": "system", "content": "If you recognize the user's command as a to-do list request (for example), then return 'to-do list'."},
            {"role": "user", "content": command},
        ]
        return self.__create_chat_completion(messages)
    
    def get_audio_from_text(self, text, file):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            speed=1.5,
            input=text,
        )
        response.stream_to_file(file)

    def get_todo_command_label(self, command):
        messages=[
            {"role": "system", "content": "You are a vocal assistant."},
            {"role": "system", "content": "Your role is to classify the user's command for a todo list functionality and return only the corresponding label."},
            {"role": "system", "content": "The labels are: add, remove, list, none"},
            {"role": "system", "content": "For example, if the user says 'I want to go running tomorrow at 10 am', then return 'add'."},
            {"role": "user", "content": command},
        ]
        return self.__create_chat_completion(messages)
    
    def generate_todo(self, command):
        messages=[
            {"role": "system", "content": "You are a vocal assistant."},
            {"role": "system", "content": "The user is trying to add a task to their to-do list, your job is to format their request into a concise task"},
            {"role": "system", "content": "For example, if the user says 'I want to go running tomorrow at 10 am', then you should rephrase it as 'Go running tomorrow at 10 am'"},
            {"role": "system", "content": "Ignore any words that are not part of the task itself"},
            {"role": "user", "content": command},
        ]
        return self.__create_chat_completion(messages)
    
    def get_approve_deny(self, command):
        messages=[
            {"role": "system", "content": "You are an assistant tasked with classifying user responses."},
            {"role": "system", "content": "The user will approve or deny a proposal."},
            {"role": "system", "content": "Determine whether the user approves or denies."},
            {"role": "system", "content": "Return 'approve' or 'deny'."},
            {"role": "user", "content": command},
        ]
        return self.__create_chat_completion(messages)
    
    def recognize_todo(self, tasks, command):
        messages=[
            {"role": "system", "content": "Your task is to match the user's command to the one of the elements of a todo list."},
            {"role": "system", "content": "The user wants to remove a specific task from their todo list."},
            {"role": "system", "content": "Identify the task from their command."},
            {"role": "system", "content": "If you find a task that matches their request, return the exact task text, nothing more. else return 'none'"},
            {"role": "system", "content": "Here is the task list to match:"},
        ]
        for index, task in enumerate(tasks):
            messages.append({"role": "system", "content": f"{index+1}: {task},"},)
        messages.append({"role": "user", "content": command})
        return self.__create_chat_completion(messages)