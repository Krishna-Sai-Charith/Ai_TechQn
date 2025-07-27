import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Initialization
load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
openai = OpenAI(api_key=openai_api_key)

MODEL = "gpt-4o-mini"

system_message = (
    "You are a helpful assistant. You will carefully review technical questions "
    "and answer them with proper reasoning and analysis. "
    "Give short, on-to-the-point answers."
)

def stream_gpt(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    result = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            result += content
            yield result

gr.ChatInterface(fn=stream_gpt, type="messages").launch()
