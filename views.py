from forms import USER
from flask import render_template, request, session, redirect
from app import app
from models import *
from Config import *



#user = User(username = "test" ,password = "test", mail="test@gmail.com",)
#db.session.add(user)
#db.session.commit()

@app.route("/login", methods=["GET", "POST"])
def login():
    form = USER()
    if request.method == "POST":
        mail = form.mail.data
        password = form.password.data
        user = db.session.query(User).filter(User.mail == mail).first()
        print(user)
        if user and user.password_hash == password:
            session["access"] = user.role
            app.config['BASIC_AUTH_USERNAME'] = user.mail
            app.config['BASIC_AUTH_PASSWORD'] = user.password_hash
            return redirect("/")
        else:
            # Пользователь не найден или не верный пароль
            print("Не верное имя или пароль")

    return render_template("admin/auth.html", form=form)

@app.route('/')
def home():
    if not session.get('user_id'):
        return redirect('/login')
    return redirect('/admin')


@app.route('/logout', methods=["POST"])
def logout():
    if session.get("access"):
        session.pop("access")
    return redirect("/login")

