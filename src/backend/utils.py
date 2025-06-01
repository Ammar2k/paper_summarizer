from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

def summarize_text(text: str) -> str:
    """
    Summarizes the given text using Google Gemini.

    Args:
        text (str): The text to summarize.

    Returns:
        str: The summarized text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17-thinking",
            contents=f"""Summarize the following paper in a structured way.
            Explain the main points, methods, results, and conclusion.
            Also mention (if present) 2-3 key references to other works.
            Avoid going into mathematical details:\n\n{text}"""
        )
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while summarizing the text: {e}")
        return "Error: Unable to summarize the text."
