from wtforms import Form, StringField, DateField, TimeField, SelectField, TextAreaField, validators

class MedicationForm(Form):
    medication_name = StringField('Medication Name', [validators.DataRequired()])
    dosage = StringField('Dosage', [validators.DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[validators.DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[validators.Optional()])
    time_to_take = TimeField('Time to Take', format='%H:%M', validators=[validators.DataRequired()])
    frequency = SelectField('Frequency', choices=[
        ('daily', 'Daily'),
        ('twice_daily', 'Twice Daily'),
        ('three_times_daily', 'Three Times Daily'),
        ('as_needed', 'As Needed')
    ], validators=[validators.DataRequired()])
    calendar_color = StringField('Calendar Color', [validators.Optional()])
    instructions = TextAreaField('Special Instructions', [validators.Optional()])