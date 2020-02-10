
from admin import *

app.secret_key = 'my-super-secret-phrase-I-do-not-tell-this-to-nobody'
db.create_all()

if __name__ == '__main__':
    app.run()





