from flask import request
from flask_admin import AdminIndexView, expose, BaseView, Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_required, current_user
from flask_mail import Message

from Config import mail
from app import app
from forms import MAILS
from models import User, Applicant, Group, db
from views import session

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class DashboardView(AdminIndexView):

    @expose('/')
    @login_required
    def index(self):
        apptotal = db.session.query(Applicant).count()
        if apptotal == 0:
            return self.render('admin/admin_dashboard.html', apptotal=apptotal)
        else:
            satisfied = db.session.query(Applicant).filter(Applicant.status == "распределена в группу").count()
            notsatisfied = apptotal-satisfied
            lastapplicants_query = db.session.query(Applicant).order_by(Applicant.id.desc()).limit(3)
            lastappl = lastapplicants_query.all()
            groups = db.session.query(Group).all()
            return self.render('admin/admin_dashboard.html', apptotal=apptotal, satisfied=satisfied,
                                   notsatisfied=notsatisfied, appliclist=lastappl, groups=groups,
                                   name=session.get("name"))


class MailsView(BaseView):
    @login_required
    @expose('/', methods=["POST", "GET"])
    def mailer(self):
            form = MAILS()
            if request.method == "POST":
                adress = request.form.get('adress')
                theme = form.theme.data
                text = form.text.data
                applicant = db.session.query(Applicant).get(adress)
                with app.app_context():
                        msg = Message(subject=theme,
                                      sender="timoshaborisov@yandex.ru",
                                      recipients=[applicant.mail],
                                      body=text)
                        mail.send(msg)
                return self.render('admin/admin_mail_sent.html', applicant=applicant, theme=theme, text=text)
            applicants = db.session.query(Applicant).all()
            return self.render('admin/admin_mail_edit.html', applicants=applicants, form=form)



class ApplicantView(ModelView):
        column_searchable_list = ['mail', "phone", "name"]
        column_filters = ['groups.title']
        page_size = 25
        form_choices = {"status": [('новая', 'новая'), ("обрабатывается", "обрабатывается"), ("оплачена", "оплачена"),
                         ("распределена в группу", "распределена в группу")]}
        column_list = ("name", "phone", "mail", "groups", "status")

        def is_accessible(self):
            return current_user.is_authenticated


class GroupView(ModelView):
        form_excluded_columns = ['applicants', "size"]
        column_searchable_list = ["startdate", "title"]
        column_filters = ['course']
        page_size = 25
        form_choices = {"status": [('набирается', 'набирается'), ("набрана", "набрана"), ("идет", "идет"),
                        ("в архиве", "в архиве")], "course": [("python", "python"), ("vue", "vue"),
                                                              ("django", "django"), ("php", "php"),
                                                              ("html", "html")]}

        def is_accessible(self):
            return current_user.is_authenticated


class UserView(ModelView):
    column_exclude_list = ['password']
    column_searchable_list = ['name', 'mail']
    form_choices = {"role": [('user', 'Пользователь'), ("admin", "Адмнистратор")]}

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app, template_mode='bootstrap3', index_view=DashboardView())

admin.add_view(UserView(User, db.session))
admin.add_view(GroupView(Group, db.session))
admin.add_view(ApplicantView(Applicant, db.session))
admin.add_view(MailsView(name='Письма', endpoint='mail'))
