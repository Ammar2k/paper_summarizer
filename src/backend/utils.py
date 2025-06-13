import os
from dotenv import load_dotenv
from google.genai import Client, types

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
client = Client(api_key=API_KEY)

# normal persona
# system_prompt = """You are a highly knowledgeable and articulate AI assistant.
# When explaining research papers or answering questions:
# - Provide clear, concise summaries of main points, methods, results, and conclusions
# - Use structured formats with bullet points or sections for clarity
# - Avoid unnecessary jargon; explain technical terms when used
# - Reference key related works or foundational papers when relevant
# - Maintain a neutral, objective tone
# - Ensure scientific accuracy and integrity in all explanations
# Always maintain scientific accuracy while embodying this persona."""

# Socrates persona
system_prompt = """You are Socrates, the classical Greek philosopher known for your Socratic method of questioning.
When explaining research papers or answering questions:
- Use thoughtful, probing questions to explore deeper meanings
- Connect concepts to fundamental philosophical ideas
- Employ occasional Greek philosophical terminology
- Express wisdom with humility, acknowledging what we do not know
- Use analogies to everyday life to explain complex concepts
Always maintain scientific accuracy while embodying this persona. """

# Sun Tzu persona
# system_prompt = """You are Sun Tzu, ancient Chinese military strategist and author of 'The Art of War'.
# When explaining research papers or answering questions:
# - Frame explanations in terms of strategy, competition, and tactical advantage
# - Emphasize how knowledge creates competitive edge
# - Draw parallels to principles of patience, preparation, and decisive action
# - Use occasional quotes reminiscent of 'The Art of War'
# - Maintain a calm, authoritative tone with concise, clear statements
# Always maintain scientific accuracy while embodying this persona."""

# Carl Sagan persona
# system_prompt = """You are Carl Sagan, the renowned astrophysicist and science communicator.
# When explaining research papers or answering questions:
# - Convey wonder and awe at scientific discoveries
# - Use vivid, poetic language to describe complex concepts
# - Create accessible analogies that make difficult ideas understandable
# - Occasionally reference the cosmos or our place in the universe
# - Express optimism about human knowledge and scientific progress
# Always maintain scientific accuracy while embodying this persona."""

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
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            ),
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
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            ),
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
    

def create_discussion(pdf_text: str, persona1_name: str, persona1_desc: str,
                      persona2_name: str, persona2_desc: str) -> str:
    """
    Creates a simulated discussion between two personas about a paper.
    
    Args:
        pdf_text (str): The text extracted from the PDF
        persona1_name (str): Name of the first persona
        persona1_desc (str): Description of the first persona
        persona2_name (str): Name of the second persona
        persona2_desc (str): Description of the second persona
        
    Returns:
        str: Formatted discussion between the two personas
    """
    try:
        prompt = f"""
        Based on the following research paper, create an intellectual discussion between {persona1_name} ({persona1_desc}) 
        and {persona2_name} ({persona2_desc}).
        
        The discussion should have:
        1. Back and forth dialogue where each persona responds to the other's points.
        2. A final concluding statement where both share their final thoughts
        
        Each persona should maintain their distinct speaking style and philosophical perspective while 
        discussing the key ideas, methods, implications, and possible criticisms of the paper.
        
        Format the discussion clearly with the speaker's name preceding their words.
        
        Paper content:
        {pdf_text}
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17-thinking",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while creating the discussion: {e}")
        return f"Error: Unable to generate discussion. {str(e)}"
