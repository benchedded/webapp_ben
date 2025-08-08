from wtforms import Form, StringField, RadioField, SelectField,TextAreaField, validators, TelField #type: ignore
from wtforms.validators import DataRequired, Length, Regexp

class emergency_nums_form(Form):

   
    emergency_num = emergency_num = StringField(
        'Emergency Number',
        [
            validators.DataRequired(),
            validators.Regexp(
                r'^\+?\d{7,15}$',
                message="Enter a valid phone number (7–15 digits, optional +)"
            )
        ]
    )

    contact_name = StringField('Contact Name', [
        DataRequired(),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
    ])


   
