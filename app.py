from flask import Flask
from admin import *
app = Flask(__name__)
from views import *

#db.create_all()


if __name__ == '__main__':
    app.run()





