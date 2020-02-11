import password as password
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False)
    can_view_details = False

    def __repr__(self):
        return "id {0} имя:{1}".format(self.id, self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


applicants_groups_association = db.Table('users_chats',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('aplicant_id', db.Integer, db.ForeignKey('applicants.id'))
)


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    startdate = db.Column(db.String(50), nullable=False)
    applicants = db.relationship('Applicant', secondary=applicants_groups_association, back_populates='groups')
    can_view_details = True
    size = db.Column(db.Integer, default=0, nullable=False)
    max = db.Column(db.Integer, default=10, nullable=False)

    def __repr__(self):
        return self.title



class Applicant(db.Model):
    __tablename__ = "applicants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    groups = db.relationship('Group', secondary=applicants_groups_association, back_populates='applicants')

    def __repr__(self):
        return "Заявка номер #{0} имя:{1}".format(self.id, self.name)