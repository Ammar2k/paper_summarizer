import fitz # PyMuPDF

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extracts text from PDF content bytes.

    Args:
        pdf_content (bytes): The content of the PDF file as bytes.

    Returns:
        str: The extracted text from the PDF file, or an error message.
    """ 
    text = ""
    try:
        # Open PDF from bytes
        with fitz.open(stream=pdf_content, filetype="pdf") as pdf_document:
            for page in pdf_document:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"An error occurred while reading the PDF content: {e}")
        return "Error: Unable to extract text from the PDF."
