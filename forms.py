from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import NumberRange, DataRequired, Email, NumberRange




class MAILS(FlaskForm):
    theme = StringField('Mail', validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])