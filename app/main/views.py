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


@main.route('/category')
def startForm():
    rights = db.session.query(Right).all()
    categories = {}
    subcategories = {}
    discrimination = {}
    editable_html_obj = EditableHTML.get_editable_html('about')
    for right in rights:
        categories.add(right.cat)
        subcategories.add(right.subcat)
        discrimination.add(right.disc)
    return render_template('/templates/layouts/index.html')
#     return render_template('/templates/layouts/index.html', categories=categories,
#     subcategories=subcategories, discrimination=discrimination)
    #return render_template('main/about.html', editable_html_obj=editable_html_obj)
