from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField
from wtforms.validators import NumberRange, DataRequired, Email, NumberRange




class MAILS(FlaskForm):
    theme = StringField('Mail', validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])

class USER(FlaskForm):
    mail = StringField('Mail', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])