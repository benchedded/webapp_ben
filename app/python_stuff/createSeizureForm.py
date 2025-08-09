from wtforms import Form, StringField, DateField, TimeField, SelectField, TextAreaField, validators

class SeizureForm(Form):
    date = DateField('Date of Seizure', format='%Y-%m-%d', validators=[validators.DataRequired()])
    time = TimeField('Time of Seizure', format='%H:%M', validators=[validators.DataRequired()])
    seizure_type = SelectField(
        'Seizure Type',
        choices=[
            ('', 'Select'),  # Default placeholder
            ('generalized_tonic_clonic', 'Generalized Tonic-Clonic'),
            ('focal_aware', 'Focal Aware'),
            ('focal_impaired_awareness', 'Focal Impaired Awareness'),
            ('absence', 'Absence'),
            ('myoclonic', 'Myoclonic'),
            ('atonic', 'Atonic'),
            ('unknown', 'Unknown/Other')
        ],
        default='',
        validators=[
            validators.DataRequired(message="Please select a valid seizure type.")
        ]
    )
    duration = StringField('Duration (e.g. 2 mins)', [validators.DataRequired()])
    severity = SelectField('Severity', choices=[
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe')
    ], validators=[validators.DataRequired()])
    calendar_color = StringField('Calendar Color', [validators.Optional()])
    triggers = StringField('Possible Triggers', [validators.Optional()])
    notes = TextAreaField('Additional Notes', [validators.Optional()])