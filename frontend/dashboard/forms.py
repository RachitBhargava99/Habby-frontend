from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AddHabitForm(FlaskForm):
    habit = StringField('Habit')
    submit = SubmitField('Log In')
