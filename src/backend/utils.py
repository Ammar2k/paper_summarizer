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
    

def answer_question(pdf_text: str, question: str) -> str:
    """
    Answers a question based on the provided PDF text using Google Gemini.

    Args:
        pdf_text (str): The text extracted from the PDF.
        question (str): The question to answer.

    Returns:
        str: The answer to the question.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17-thinking",
            contents=f"""Based on the following research paper, please answer this question: "{question}"
            
            Paper content:
            {pdf_text}
            
            Provide a clear and specific answer based only on information in the paper.
            If the answer isn't covered in the paper, say so honestly."""
        )
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while answering the question: {e}")
        return "Error: Unable to answer the question."
