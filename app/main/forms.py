from wtforms import Form, StringField, SelectField, SubmitField
 
class TreatySearchForm(Form):
    treatyName = StringField('Search by Treaty Name')

class FilterForm(Form):
    forum = SelectField('Forum', coerce=str, choices=[("", "")], default="")
    country = SelectField('Country', coerce=str, choices=[("", "")], default="")
