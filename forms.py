from wtforms import Form, BooleanField, TextField, PasswordField, TextAreaField, SelectMultipleField, validators, widgets

class IntentForm(Form):
    title = TextField('Title', [validators.Required()])
    description = TextAreaField('Description')

class MeasureForm(Form):
    title = TextField('Title', [validators.Required()])
    description = TextAreaField('Description')