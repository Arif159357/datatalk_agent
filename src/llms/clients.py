from google import genai
from google.genai import types

class GoogleGenAIClient:
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-3-flash-preview"

    def call(self, messages, system_prompt, temperature=0.0, top_p=1.0):
        response = self.client.models.generate_content(
            model=self.model,
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt,
                                               temperature=temperature, top_p=top_p, top_k=1)
        )
        return response.text or ""
