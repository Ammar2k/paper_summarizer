import gradio as gr
import requests
from backend.utils import summarize_text
from services.pdf_reader import extract_text_from_pdf


def process_pdf(file_obj):
    """
    Processes the uploaded PDF file by sending it to a backend service,
    which extracts text and summarizes it.

    Args:
        file_obj (gradio.File): The uploaded PDF file object from Gradio.

    Returns:
        str: The summarized text from the PDF.
    """
    # wait message while processing
    yield "## Processing PDF... ⏲️"

    if file_obj is None:
        yield "Error: No file uploaded."
        return

    backend_url = "http://127.0.0.1:8000/uploadfile/"
    file_path = file_obj.name

    try:
        with open(file_path, "rb") as f:
            # Extracting the original filename for the backend
            original_filename = file_path.split('/')[-1]
            files = {"file": (original_filename, f, "application/pdf")}
            response = requests.post(backend_url, files=files, timeout=300)

        response.raise_for_status()
        
        data = response.json()
        if "summary" in data:
            yield data["summary"]
        elif "error" in data:
            yield f"Error from backend: {data['error']}"
        else:
            yield "Error: Unexpected response from backend."

    except requests.exceptions.ConnectionError:
        yield f"Error: Could not connect to the backend at {backend_url}. Please ensure the backend server is running."
    except requests.exceptions.Timeout:
        yield "Error: The request to the backend timed out."
    except requests.exceptions.RequestException as e:
        yield f"An error occurred while communicating with the backend: {e}"
    except Exception as e:
        yield f"An unexpected error occurred: {e}"
    
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
