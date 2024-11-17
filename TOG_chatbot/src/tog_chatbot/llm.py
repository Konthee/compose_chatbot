from openai import OpenAI
from groq import Groq
from typing import List, Any
from dotenv import load_dotenv
import os

class LLMClient():

    def __init__(
            self,
            model_name : str ="llama-3.1-70b-versatile" 
            ):
        # loading variables from .env file
        load_dotenv()
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model_name = model_name

    def gennerate(
            self,
            messages: List[dict],
            **kwargs: Any
        ):
        response = self.client.chat.completions.create(model=self.model_name, messages=messages, **kwargs)
        return response.choices[0].message.content