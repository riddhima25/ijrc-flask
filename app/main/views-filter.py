import json
import os
import sys

from flask import (abort, jsonify, redirect, render_template, request,
                   send_from_directory, session, url_for)

from .. import db

@main.route('/category')
def startForm():
    rights = db.session.query(Right).all()
    categories = {}
    subcategories = {}
    discrimination = {}
    for right in rights:
        categories.add(right.category)
        subcategories.add(right.subcategory)
        discrimination.add(right.discrimination)
    # return render_template('/templates/layouts/index.html', categories=categories,
    #subcategories=subcategories, discrimination=discrimination)
    return rights

@main.route('/category/<string:category>')
def showCategory():
    category = db.session.query(Right).filter_by(categoryId=category).all()
    session['currentCategory'] = category
    subcategories = {}
    discrimination = {}
    for right in category:
        subcategories.add(right.subcategory)
        discrimination.add(right.discrimination)
    #return render_template('/templates/layouts/index.html', categories=category,
    #subcategories=subcategories, discrimination=discrimination)
    return category;

@main.route('/category/<string:category>/<string:subcategory>')
def showSubcategory():
    subcategory = db.session.query(Right).filter_by(category=category, subcategory=subcategory).all()
    session['currentSubcategory'] = subcategory.subcategory
    discrimination = {}
    for right in subcategory:
        discrimination.add(right.discrimination)
    #return render_template('/templates/layouts/index.html', categories=category,
    #subcategories=subcategory.subcategory, discrimination=discrimination)
    return subcategory;

@main.route('/category/<string:category>/<string:subcategory>/<string:discrimination>')
def showDiscrimination():
    discrimination = db.session.query(Right).filter_by(category=category, subcategory=subcategory, discrimination=discrimination).all()
    session['currentDiscrimination'] = discrimination.discrimination
    #return render_template('/templates/layouts/index.html', categories=category,
    #subcategories=subcategory, discrimination=discrimination.discrimination)
    return discrimination

@main.route('/category/<string:category>/<string:subcategory>/<string:discrimination>/<string:age>')
def showAge():
    age = db.session.query(Right).filter_by(category=category, subcategory=subcategory, discrimination=discrimination, age=age).all()
    session['currentAge'] = age.age
    #return render_template('/templates/layouts/index.html', categories=category,
    #subcategories=subcategory, discrimination=discrimination, age=age.age)
    return age

@main.route('/results')
def showResults():
    return render_template('/templates/layouts/client_side_results.html', categories=category,
    #subcategories=subcategory, discrimination=discrimination, age=age.age)