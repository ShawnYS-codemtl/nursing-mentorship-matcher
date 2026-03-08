from flask import Flask
import app.models
from app.database import init_db

app = Flask(__name__)

@app.route("/")
def home():
    return "Mentorship Matcher Running"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)