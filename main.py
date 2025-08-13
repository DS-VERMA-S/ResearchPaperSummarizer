import os
from dotenv import load_dotenv

# Ensure .env is loaded for HOST/PORT and GROQ_API_KEY
load_dotenv()


def get_host_port() -> tuple[str, int]:
    host = os.getenv("HOST", "0.0.0.0")
    port_str = os.getenv("PORT", "8000")
    try:
        port = int(port_str)
    except ValueError:
        port = 8000
    return host, port


if __name__ == "__main__":
    import uvicorn

    host, port = get_host_port()
    # Run the FastAPI app from src.app.main
    uvicorn.run("src.app.main:app", host=host, port=port, reload=True)