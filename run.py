from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
