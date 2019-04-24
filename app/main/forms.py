from wtforms import Form, StringField, SelectField
 
class TreatySearchForm(Form):
    search = StringField('')