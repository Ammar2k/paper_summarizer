import gradio as gr
import requests

# Track if the PDF has been uploaded successfully
pdf_uploaded = False


def process_pdf(file_obj):
    """
    Processes the uploaded PDF file by sending it to a backend service,
    which extracts text and summarizes it.

    Args:
        file_obj (gradio.File): The uploaded PDF file object from Gradio.

    Returns:
        str: The summarized text from the PDF.
    """
    global pdf_uploaded
    # reset the flag
    pdf_uploaded = False

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
            files = {"file": (original_filename, f)}
            response = requests.post(backend_url, files=files, timeout=300)

        response.raise_for_status()
        
        data = response.json()
        if "summary" in data:
            # set the flag to true
            pdf_uploaded = True
            yield f"## Summary\n\n{data['summary']}\n\n---\n\nYou can now ask questions about this paper in the Q&A tab."
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

def ask_question(question, history):
    """
    Sends a question to the backend service to get an answer based on the uploaded PDF text.

    Args:
        question (str): The question to ask.
        history (list): The conversation history.

    Returns:
        str: The answer to the question.
    """
    global pdf_uploaded

    if not pdf_uploaded:
        return history + [(question, "Please upload a PDF first.")]
    
    if not question.strip():
        return history
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask/",
            json={"question": question},
            timeout=60
        )
        response.raise_for_status()

        data = response.json()
        if "answer" in data:
            answer = data["answer"]
        else:
            answer = f"Error: {data.get('error', 'No answer found in response.')}"

    except Exception as e:
        answer = f"Error connecting to backend: {str(e)}"

    return history + [(question, answer)]


def generation_discussion(persona1, persona2):
    """
    Generates a simulated discussion between two AI personas about the uploaded paper.
    
    Args:
        persona1 (str): Name of the first persona
        persona2 (str): Name of the second persona
        
    Returns:
        str: Formatted conversation between the two personas
    """
    global pdf_uploaded

    if not pdf_uploaded:
        return "Please upload a PDF first."

    try:
        response = requests.post(
            "http://127.0.1:8000/discuss/",
            json={"persona1": persona1, "persona2": persona2},
            timeout=120 # since it might take longer for discussion generation
        )
        response.raise_for_status()

        data = response.json()
        if "discussion" in data:
            return data["discussion"]
        else:
            return f"Error: {data.get('error', 'No discussion generated.')}"

    
# Gradio interface with tabs
with gr.Blocks(title="Paper Simplifier") as interface:
    gr.Markdown("# 📑 Paper Simplifier")
    gr.Markdown("Upload a PDF file and get a summarized version and ask questions about it.")

    with gr.Tabs():
        with gr.Tab("Upload and Summarize"):
            with gr.Row():
                with gr.Column():
                    pdf_input = gr.File(label="Upload a PDF", file_types=[".pdf"])
                    summarize_button = gr.Button("Upload and Summarize", variant="primary")     
                summary_output = gr.Markdown(label="Summarized Text")
                summarize_button.click(
                    process_pdf,
                    inputs=pdf_input,
                    outputs=summary_output
                )

        with gr.Tab("Q&A"):
            gr.Markdown("### Ask questions about the uploaded paper")
            chatbot = gr.Chatbot(height=400)
            question_input = gr.Textbox(
                label="Ask a question about the paper", 
                placeholder="Type your question here..."
            )
            ask_button = gr.Button("Ask")

            # Connect the button to the ask_question function
            ask_button.click(
                fn=ask_question,
                inputs=[question_input, chatbot],
                outputs=chatbot
            )

            # Also enable pressing Enter to submit
            question_input.submit(
                fn=ask_question,
                inputs=[question_input, chatbot],
                outputs=chatbot
            )

        with gr.Tab("AI Discussion"):
            gr.Markdown("### Simulated Discussion between AI Personas")
            with gr.Row():
                persona1 = gr.Dropdown(
                    choices=["Socrates", "Sun Tzu", "Carl Sagan"],
                    label="First Discussant",
                    value="Socrates"
                )
                persona2 = gr.Dropdown(
                    choices=["Socrates", "Sun Tzu", "Carl Sagan"],
                    label="Second Discussant",
                    value="Sun Tzu"
                )
                
            generate_button = gr.Button("Generate Discussion", variant="primary")
            discussion_output = gr.Markdown()

            generate_button.click(
                fn=generation_discussion,
                inputs=[persona1, persona2],
                outputs=discussion_output
            )

if __name__ == "__main__":
    interface.launch()
