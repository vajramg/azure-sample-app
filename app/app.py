from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Read secrets directly from Azure Key Vault mounted files
with open("/mnt/secret-store/db-user1", "r") as f:
    db_user = f.read().strip()

with open("/mnt/secret-store/db-password", "r") as f:
    db_psw = f.read().strip()

# PostgreSQL StatefulSet primary pod
db_host = "db-0.db-svc"

# Database name
db_name = "launchpage"

# SQLAlchemy connection string
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql://{db_user}:{db_psw}@{db_host}/{db_name}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return f'<E-mail {self.email}>'


# Auto-create tables if not existing
with app.app_context():
    db.create_all()


# Homepage
@app.route('/')
def index():
    return render_template('index.html')


# Register email
@app.route('/prereg', methods=['POST'])
def prereg():

    try:

        email = request.form['email']

        # Check duplicate email
        existing_user = db.session.query(User).filter(
            User.email == email
        ).first()

        if existing_user:
            return render_template(
                'index.html',
                message="Email already registered"
            )

        # Insert new user
        reg = User(email)

        db.session.add(reg)

        db.session.commit()

        return render_template('success.html')

    except Exception as e:

        print("ERROR:", str(e))

        return f"Application Error: {str(e)}", 500


if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )