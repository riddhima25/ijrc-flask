from flask import Blueprint, render_template

from app.models import EditableHTML
from .. import db
from ..models import Right, Forum, Country, TreatyToCountry, TreatyToRight, TreatyToForum

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)


## ADDING, MODIFYING, DELETING RECORDS 



## FILTERING -- USER SIDE

@main.route('/<country>/form')
def startForm():
    rights = db.session.query(Right).all()
    categories = []
    subcategories = []
    discrimination = []
    for right in rights:
        categories.append(right.cat)
        subcategories.append(right.subcat)
        discrimination.append(right.disc)
    # return render_template('/templates/layouts/index.html', categories=categories,
    #subcategories=subcategories, discrimination=discrimination)
    return rights
    
## FILTERING -- ADMIN SIDE 
