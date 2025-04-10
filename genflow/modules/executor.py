from http import client
from openai import OpenAI
import os

#Load environment variables from .env file
#Code omitted: load your OpenAI key

def call_openai_model(prompt, model="gpt-3.5-turbo", temperature=0.7):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an assistant who generates markdown outputs."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content

