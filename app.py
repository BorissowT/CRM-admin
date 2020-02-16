from flask import Flask
app = Flask(__name__)

from flask_login import LoginManager
from admin import *
from views import *
from models import User

admin = db.session.query(User).filter(User.role == "admin").first()

if (admin == None):
    user = User(name="DefaultAdmin", role="admin", mail="admin@mail.com", password_hash="12345")
    db.session.add(user)
    db.session.commit()





if __name__ == '__main__':
    app.run()





