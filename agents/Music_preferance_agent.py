from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
import json
import os

class JSONPreferenceParser(BaseOutputParser):
    def parse(self, text: str) -> dict:
        try:
            text = text.strip()
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(f"Could not parse output: {text}")

class MusicPreferenceAgent:
    """
    Extracts genre, mood, explicit, and language (but language is ignored for Spotify API).
    """
    def __init__(self, api_key: str):
        os.environ["OPENAI_API_KEY"] = api_key
        self.llm = ChatOpenAI(model="gpt-4o")
        self.prompt = PromptTemplate.from_template(
            """
            You are a music preference extraction agent.
            Given a user prompt, extract a strict JSON object like:
            {{
                "genre": string or null,
                "mood": string or null,
                "explicit": true/false,
                "exclude_genres": [string],
                "language": "english" | "hindi" | null
            }}
            Output only valid JSON. No text outside the JSON block.
            User input: "{user_input}"
            """
        )
        self.parser = JSONPreferenceParser()

    def extract_preferences(self, user_input: str) -> dict:
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"user_input": user_input})
