import flask_wtf
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired


class MAILS(flask_wtf.FlaskForm):
    theme = StringField('Mail', validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])

class USER(flask_wtf.FlaskForm):
    mail = StringField('Mail', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])