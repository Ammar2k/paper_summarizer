import gradio as gr
from backend.utils import summarize_text
from services.pdf_reader import extract_text_from_pdf


def process_pdf(file_obj):
    """
    Processes the uploaded PDF file, extracts text, and summarizes it.

    Args:
        file_obj (gradio.File): The uploaded PDF file object from Gradio.

    Returns:
        str: The summarized text from the PDF.
    """
    # wait message while processing
    yield "## Processing PDF... ⏲️"

    try:
        # Get the file path from the Gradio file object
        file_path = file_obj.name

        # Read the file content as bytes
        with open(file_path, "rb") as f:
            pdf_content = f.read()

        # Extract text from the PDF bytes
        extracted_text = extract_text_from_pdf(pdf_content)
        if not extracted_text or extracted_text.startswith("Error"):
            yield "Error: Could not extract text from the PDF."
            return

        # Summarize the extracted text
        summary = summarize_text(extracted_text)

        yield summary
    except Exception as e:
        return f"An error occurred: {e}"
    
# Gradio interface
interface = gr.Interface(
    fn=process_pdf,
    inputs=gr.File(label="Upload a PDF"),
    outputs=gr.Markdown(
        label="Summarized Text"),
    title="Paper Simplifier",
    description="Upload a PDF file and get a summarized version of its content.",
)

if __name__ == "__main__":
    interface.launch()
