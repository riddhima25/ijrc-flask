from flask import Blueprint, render_template, session

from app.models import EditableHTML
from .. import db
from ..models import Right, Forum, Country, TreatyToCountry, TreatyToRight, TreatyToForum, Treaty

from .. import db

@main.route('/start')
def startLanding():
    return render_template('/templates/layouts/landing.html')

@main.route('/start/<country>')
def startLanding():
    country_entry = db.session.query(Country).filter_by(name = country)
    session['Country'] = country_entry;
    return render_template('/templates/layouts/landing.html', country = country)

@main.route('/form')
def startForm():
    rights = db.session.query(Right).all()
    categories = []
    subcategories = []
    discrimination = []
    for right in rights:
        categories.append(right.cat)
        subcategories.append(right.subcat)
        discrimination.append(right.disc)
    #return render_template('/layouts/index.html', categories=categories,
    #subcategories=subcategories, discrimination=discrimination)
    return rights

@main.route('/form/<category>')
def showCategory():
    rights = db.session.query(Right).filter_by(cat=category).all()
    session['Category'] = category
    subcategories = []
    discrimination = []
    for right in rights:
        subcategories.append(right.subcat)
        discrimination.append(right.disc)
    #return render_template('/layouts/index.html', categories=category,
    #subcategories=subcategories, discrimination=discrimination)
    return rights;

@main.route('/form/<category>/<subcategory>')
def showSubcategory():
    rights = db.session.query(Right).filter_by(cat=category, subcat=subcategory).all()
    session['Subcategory'] = subcategory
    discrimination = []
    for right in rights:
        discrimination.append(right.disc)
    #return render_template('/layouts/index.html', categories=category,
    #subcategories=subcategory.subcategory, discrimination=discrimination)
    return rights;

@main.route('/form/<category>/<subcategory>/<discrimination>')
def showDiscrimination():
    right = db.session.query(Right).filter_by(cat=category, subcat=subcategory, disc=discrimination).all()
    session['Discrimination'] = right.disc
    #return render_template('/layouts/index.html', categories=category,
    #subcategories=subcategory, discrimination=discrimination.discrimination)
    return right;

@main.route('/results')
def showResults():
    right = db.session.query(Right).filter_by(
        cat=session['Category'], 
        subcat=session['Subcategory'], 
        disc=session['Discrimination']).all()
    treaty = db.session.query(Treaty).filter_by(ttor = right.ttor, ttoc = session['Country'].ttoc)
    forums = db.session.query(Forum).filter_by(ttof = treaty.ttof)
    #return render_template('/layouts/client_side_results.html',
    #    right = right, treaty = treaty, forums = forums)
    return [right, treaty, forums]