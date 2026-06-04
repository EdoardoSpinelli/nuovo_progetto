from dotenv import load_dotenv
from src.app import create_app
import os

load_dotenv()
PORT = os.getenv("PORT", "8082")
app = create_app()

if __name__ == "__main__":
    # Avvia il server sviluppato con Flask
    app.run(host='0.0.0.0', port=PORT)
