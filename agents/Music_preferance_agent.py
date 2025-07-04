# agents/music_preference_agent.py

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
import os

class JSONPreferenceParser(BaseOutputParser):
    """
    A simple parser to force a strict JSON output.
    """

    def parse(self, text: str) -> dict:
        import json
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(f"Could not parse output: {text}")

class MusicPreferenceAgent:
    """
    Production-grade class to extract user music preferences from free text.
    """

    def __init__(self, api_key: str):
        os.environ["OPENAI_API_KEY"] = api_key
        self.llm = ChatOpenAI(model="gpt-4o")  # you can use gpt-4o
        self.prompt = PromptTemplate.from_template(
            """
            You are a domain-aware Music Recommendation Extraction Agent.
            Parse the user prompt and return a JSON in this schema:
            {{"genre": string or null, "mood": string or null, "explicit": true/false, "exclude_genres": [string]}}
            Strictly output only JSON, no other text.

            User prompt: "{user_input}"
            """
        )
        self.parser = JSONPreferenceParser()

    def extract_preferences(self, user_input: str) -> dict:
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"user_input": user_input})

