from flask_admin import AdminIndexView, expose, BaseView, Admin
from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, request
from flask_basicauth import BasicAuth

from models import *
from forms import MAILS
from Config import *
from app import app

basic_auth = BasicAuth(app)


class DashboardView(AdminIndexView):

    @expose('/')

    def index(self):
        if session.get("access")=="admin":
            print(session["user_id"])
            #session.pop("user_id")
            apptotal = db.session.query(Applicant).count()
            satisfied = db.session.query(Applicant).filter(Applicant.status == "распределена в группу").count()
            notsatisfied = apptotal-satisfied
            lastapplicants_query = db.session.query(Applicant).order_by(Applicant.id.desc()).limit(3)
            lastappl = lastapplicants_query.all()
            lstapp = lastappl[0]
            ndapp = lastappl[1]
            thrdapp = lastappl[2]
            groups = db.session.query(Group).all()

            return self.render('admin/admin_dashboard.html', apptotal=apptotal, satisfied=satisfied,
                               notsatisfied=notsatisfied, lstapp=lstapp, ndtapp=ndapp, thrdapp=thrdapp, groups=groups)
        else:
            return redirect('/login')

class MailsView(BaseView):

    @expose('/', methods=["POST", "GET"])
    def mailer(self):
        if session.get("access")=="admin":
            form = MAILS()
            if request.method == "POST":
                adress = request.form.get('adress')
                theme = form.theme.data
                text = form.text.data
                applicant = db.session.query(Applicant).get(adress)
                with app.app_context():
                        msg = Message(subject=theme,
                                      sender="timoshaborisov@yandex.ru",
                                      recipients=[applicant.mail],  # replace with your email for testing
                                      body=text)
                        mail.send(msg)
                return self.render('admin/admin_mail_sent.html', applicant=applicant, theme=theme, text=text)
            applicants = db.session.query(Applicant).all()
            return self.render('admin/admin_mail_edit.html', applicants=applicants, form=form)
        else:
            return redirect('/login')


class ApplicantView(ModelView):
        column_searchable_list = ['mail', "phone", "name"]
        column_filters = ['groups.title']
        page_size = 25
        form_choices = {"status": [('новая', 'новая'), ("обрабатывается", "обрабатывается"), ("оплачена", "оплачена"),
                         ("распределена в группу", "распределена в группу")]}



class GroupView(ModelView):
        form_excluded_columns = ['applicants', "size"]
        column_searchable_list = ["startdate", "title"]
        column_filters = ['course']
        page_size = 25
        form_choices = {"status": [('набирается', 'набирается'), ("набрана", "набрана"), ("идет", "идет"),
                        ("в архиве", "в архиве")], "course": [("python", "python"), ("vue", "vue"),
                                                              ("django", "django"), ("php", "php"),
                                                              ("html", "html")]}




class UserView(ModelView):
    column_exclude_list = ['password']
    column_searchable_list = ['name', 'mail']


admin = Admin(app, template_mode='bootstrap3', index_view=DashboardView())

admin.add_view(UserView(User, db.session))
admin.add_view(GroupView(Group, db.session))
admin.add_view(ApplicantView(Applicant, db.session))
admin.add_view(MailsView(name='Письма', endpoint='mail'))

