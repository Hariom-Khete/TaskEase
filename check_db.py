from flask import Flask , render_template , request , redirect , flash , session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
def set_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

set_password('1234')
