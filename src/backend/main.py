from fastapi import FastAPI, UploadFile, File, HTTPException
from services.pdf_reader import extract_text_from_pdf
from backend.utils import summarize_text, answer_question, create_discussion
from pydantic import BaseModel

app = FastAPI()

# Global variable to store the PDF text
pdf_text = None

class QuestionRequest(BaseModel):
    question: str

class DiscussionRequest(BaseModel):
    persona1: str
    persona2: str

@app.post("/uploadfile/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        global pdf_text
        pdf_content = await file.read()
        extracted_text = extract_text_from_pdf(pdf_content)
        if not extracted_text or extracted_text.startswith("Error"):
            return {"error": "Could not extract text from the PDF."}
        
        # Store the extracted text in the global variable
        pdf_text = extracted_text

        summary = summarize_text(extracted_text)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/ask/")
async def ask_question(question_req: QuestionRequest):
    global pdf_text
    if pdf_text is None:
        raise HTTPException(status_code=400, detail="No PDF has been uploaded yet.")
    
    try:
        response = answer_question(pdf_text, question_req.question)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/discuss/")
async def discuss(discussion_req: DiscussionRequest):
    global pdf_text
    if pdf_text is None:
        raise HTTPException(status_code=400, detail="No PDF has been uploaded yet.")
    
    try:
        persona_descriptions = {
            "Socrates": "a classical Greek philosopher known for the Socratic method of questioning",
            "Sun Tzu": "an ancient Chinese military strategist and author of 'The Art of War'",
            "Carl Sagan": "a renowned astrophysicist and science communicator known for poetic explanations"
        }

        p1_desc = persona_descriptions.get(discussion_req.persona1)
        p2_desc = persona_descriptions.get(discussion_req.persona2)

        # Simulate a discussion between two personas
        response = create_discussion(pdf_text, discussion_req.persona1, p1_desc, discussion_req.persona2, p2_desc)
        return {"discussion": response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "Backend is running!"}
