import sys

from streamlit.web.cli import main

from core.definitions import FRONTEND_PORT


if __name__ == "__main__":
    sys.argv = [
        "streamlit", 
        "run", 
        "frontend/src/main.py", 
        "--server.port", f"{FRONTEND_PORT}"
    ]
    sys.exit(main(prog_name="streamlit"))