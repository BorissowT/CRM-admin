from flask import session, redirect, render_template
from app import *
from flask_login import current_user, login_user, logout_user, login_required

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
            session["user_id"] = user.id
            login_user(user)
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
