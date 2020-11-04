from os import getenv

from dotenv import load_dotenv

from api import app

if __name__ == "__main__":
    load_dotenv()

    app.run(host=getenv(
        "host"), port=getenv(
        "port"), debug=True)
