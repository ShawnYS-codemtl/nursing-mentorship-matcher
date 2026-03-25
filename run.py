from app.routes import create_app
from app.database import init_db

app = create_app()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)