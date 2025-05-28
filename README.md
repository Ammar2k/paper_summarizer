# Paper Simplifier

This project is a simple chat application that summarizes the content of academic papers. It utilizes FastAPI for the backend, Gradio for the frontend, and PyMuPDF for reading PDF files.

## Project Structure

```
paper_simplifier
├── src
│   ├── app.py               # Entry point for the application
│   ├── backend
│   │   ├── main.py          # Main logic for the FastAPI backend
│   │   └── utils.py         # Utility functions for backend operations
│   ├── frontend
│   │   └── interface.py      # Gradio interface for the frontend
│   └── services
│       └── pdf_reader.py    # Functions for reading and extracting text from PDFs
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
└── .gitignore                # Files and directories to ignore by Git
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd paper_simplifier
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage Guidelines

1. Ensure you have created a `.env` file in the root directory with your `GOOGLE_API_KEY`. You can use `.env.example` as a template.

2. Start the application:
   ```
   python src/app.py
   ```

3. Open the Gradio interface link (usually http://127.0.0.1:7860 or similar, as indicated in your terminal) in your browser to access the application. The FastAPI backend will be running concurrently.

## Overview of the Application

The application allows users to upload PDF files of academic papers. It extracts the text from the PDF using PyMuPDF and provides a summarized version of the content. Users can interact with the application through a chat interface, asking questions and receiving responses based on the summarized content.
