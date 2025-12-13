#!/usr/bin/env python3

from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from config import girlfriend_name, user_name, premessage, chat_history_length

ollama_llm = ChatOllama(model="qwen2.5:0.5b")

chat_history = [
    SystemMessage(content=premessage),
]

while True:
    user_input=input(user_name+": ")
    chat_history.append(HumanMessage(content=user_input))
    chat_history = chat_history[-chat_history_length:]
    response = ollama_llm.invoke(chat_history)
    print(girlfriend_name+":",response.content)
