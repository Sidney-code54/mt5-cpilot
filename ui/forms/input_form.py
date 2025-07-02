from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AskForm(FlaskForm):
    question = StringField('Ask Your Question', validators=[DataRequired()])
    submit = SubmitField('Ask')
