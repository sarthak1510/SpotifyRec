from openai import OpenAI
import ast

class LanguageFilterAgent:
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)

    def filter_by_language(self, recommendations: list[dict], language: str, top_k: int = 10) -> list[dict]:
        if not recommendations:
            print("⚠️ No recommendations to filter.")
            return []

        track_list = "\n".join(f"{track['name']} by {track['artist']}" for track in recommendations)

        prompt = f"""
        Act as an expert music language classifier, don't do it just based on titles, understand the lyrics of each song and based 
        on percentage lyric clasify it based on language. Some hindi songs might have english words but that does not mean it is
        in english- so understand the entire lyrics and for example 75% of it is hindi and 25% of it is in english that means the song is hindi
        and not english.
        From the songs listed below:

        {track_list}

        Return a valid Python list of up to {top_k} **song titles only** that are most likely in the **{language}** language.
        - Return only the song titles, no artist names.
        - Format: ["song1", "song2", ...]
        - Output must be valid Python list syntax with double quotes.

        
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You only return a valid Python list of strings. No explanation."},
                    {"role": "user", "content": prompt}
                ]
            )
            raw = response.choices[0].message.content.strip()
            print(f"✅ Raw LLM response: {raw}")
            if raw.startswith("```"):
                raw = raw.replace("```python", "").replace("```", "").strip()
            filtered_titles = ast.literal_eval(raw)
        except Exception as e:
            print(f"❌ Error during language filtering: {e}")
            return recommendations

        filtered = [
            track for track in recommendations if track["name"] in filtered_titles
        ]
        if not filtered:
            print("⚠️ No songs matched language filter. Using unfiltered set.")
            return recommendations

        print(f"✅ Language filter kept {len(filtered)} tracks.")
        return filtered
