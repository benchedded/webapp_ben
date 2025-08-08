from wtforms import Form, StringField, RadioField, SelectField,TextAreaField, validators #type: ignore

class module_form(Form):
    module_type = SelectField('Module Type', [validators.DataRequired()], choices=[('', 'Select'),('S', 'Seizure'),('MD', 'Mood Disorders'), ('N', 'Nutrition'),('SI','Sleep Issues')], default='')
    module_num = SelectField('Module Type', [validators.DataRequired()], choices=[('','Select'),('1', '1'),('2', '2'), ('3', '3'),('4','4')], default='')


