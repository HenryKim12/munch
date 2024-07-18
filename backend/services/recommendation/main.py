from app import create_app
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == "__main__":
    debug = False;
    if (os.getenv("ENV") == "DEV"):
        debug = True;
    app.run(debug=debug)