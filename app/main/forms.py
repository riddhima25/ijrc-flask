from wtforms import Form, StringField, SelectField
 
class TreatySearchForm(Form):
    treatyName = StringField('Search by Treaty Name')
    #country = SelectField('Country', coerce=str)
    forum = SelectField('Forum', coerce=str)