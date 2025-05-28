from fastapi import FastAPI, UploadFile, File
from services.pdf_reader import extract_text_from_pdf
from backend.utils import summarize_text

app = FastAPI()

@app.post("/uploadfile/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        pdf_content = await file.read()
        extracted_text = extract_text_from_pdf(pdf_content)
        if not extracted_text or extracted_text.startswith("Error"):
            return {"error": "Could not extract text from the PDF."}
        summary = summarize_text(extracted_text)
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "Backend is running!"}
