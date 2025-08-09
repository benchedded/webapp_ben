#createActivityform.py
from wtforms import Form, StringField, IntegerField, TextAreaField, validators  # type: ignore

class activity_form(Form):
    activity_name = StringField('Activity Name', [validators.DataRequired()])
    estimated_time = StringField('Estimated Time (e.g. 30 mins)', [validators.DataRequired()])
    reps = IntegerField('Number of Repetitions', [validators.DataRequired()])
    instructions = TextAreaField('Instructions', [validators.DataRequired()])
    