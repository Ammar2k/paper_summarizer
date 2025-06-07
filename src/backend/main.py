from fastapi import FastAPI, UploadFile, File, HTTPException
from services.pdf_reader import extract_text_from_pdf
from backend.utils import summarize_text

app = FastAPI()

# Global variable to store the PDF text
pdf_text = None

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
async def ask_question(question: str):
    global pdf_text
    if pdf_text is None:
        raise HTTPException(status_code=400, detail="No PDF has been uploaded yet.")
    
    try:
        response = answer_question(pdf_text, question)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "Backend is running!"}
