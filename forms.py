from wtforms import Form, BooleanField, TextField, PasswordField, TextAreaField, SelectMultipleField, validators, widgets

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class IntentForm(Form):
    title = TextField('Title', [validators.Required()])
    description = TextAreaField('Description')

    measured_by = MultiCheckboxField(choices=[])

class MeasureForm(Form):
    title = TextField('Title', [validators.Required()])
    description = TextAreaField('Description')