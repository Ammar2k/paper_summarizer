import uvicorn
from backend.main import app
from frontend.interface import interface
import threading

def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)

def run_gradio():
    interface.launch()

if __name__ == "__main__":
    # Start FastAPI backend in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.daemon = True  # Set as a daemon thread
    fastapi_thread.start()
    # Launch the Gradio interface in the main thread
    try:
        run_gradio()
    except KeyboardInterrupt:
        print("Shutting down Gradio interface...")
    finally:
        print("Exiting application...")
