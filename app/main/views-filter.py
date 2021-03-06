from flask import Blueprint, render_template, session, jsonify, url_for

from app.models import EditableHTML
from .. import db
from ..models import Results, Right, Forum, Country, TreatyToCountry, TreatyToRight, TreatyToForum, Treaty

from .. import db

@main.route('/start')
def startLanding():
    return render_template('/templates/layouts/landing.html')

@main.route('/start/<country>')
def endLanding(country):
    country_entry = db.session.query(Country).filter_by(name = country)
    session['Country'] = country_entry
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
    return render_template('/layouts/index.html', categories=categories,
    subcategories=subcategories, discrimination=discrimination)

@main.route('/form/<category>')
def showCategory(category):
    rights = db.session.query(Right).filter_by(cat=category).all()
    subcategories = []
    discrimination = []
    for right in rights:
        subcategories.append(right.subcat)
        discrimination.append(right.disc)
    return render_template('/layouts/index.html', categories=category,
    subcategories=subcategories, discrimination=discrimination)

@main.route('/form/<category>/<subcategory>')
def showSubcategory(category, subcategory):
    rights = db.session.query(Right).filter_by(cat=category, subcat=subcategory).all()
    discrimination = []
    for right in rights:
        discrimination.append(right.disc)
    return render_template('/layouts/index.html', categories=category,
    subcategories=subcategory.subcategory, discrimination=discrimination)

@main.route('/form/<category>/<subcategory>/<discrimination>')
def showDiscrimination(category, subcategory, discrimination):
    return render_template('/layouts/index.html', categories=category,
    subcategories=subcategory, discrimination=discrimination);

@main.route('/form/<category>/<subcategory>/<discrimination>', methods = ['POST'])
def submitForm(category, subcategory, discrimination):
    right = db.session.query(Right).filter_by(
        cat=category, 
        subcat=subcategory, 
        disc=discrimination).all()
    treaty = db.session.query(Treaty).filter_by(ttor = right.ttor, ttoc = session['Country'].ttoc)
    forums = db.session.query(Forum).filter_by(ttof = treaty.ttof)
    result = Results(
        right = right,
        treaty = treaty,
        forum = forums
    )
    db.session.add(result);
    db.session.commit();
    return jsonify(dict(redirect=url_for('layouts.index')))

@main.route('/results')
def showResults():
    results = Results.query.all();
    return render_template('/layouts/client_side_results.html',
        results=results)