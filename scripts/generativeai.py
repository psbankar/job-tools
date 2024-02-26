import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv

class GenerativeAI:
    def __init__(self):
        load_dotenv(find_dotenv())
        genai.configure(api_key=os.getenv("GENERATIVEAI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")
