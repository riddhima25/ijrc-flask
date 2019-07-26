from flask import Blueprint, render_template, session, jsonify, request, redirect, flash, url_for
from sqlalchemy import or_

from app.models import EditableHTML
from .. import db
from ..models import Right, Forum, Country, TreatyToCountry, TreatyToRight, TreatyToForum, Results, Treaty
from .forms import TreatySearchForm
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    categories = []
    subcategories = []
    discriminations = []
    results = db.session.query(Right).all()
    for result in results:
      if result.cat not in categories:
        categories.append(result.cat)
      if result.subcat not in subcategories:
        subcategories.append(result.subcat)
      if result.disc not in discriminations:
        discriminations.append(result.disc)

    return render_template('main/index.html', categories=categories, subcategories=subcategories,
      discriminations=discriminations)


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)

@main.route('/admin', methods=['GET', 'POST'])
def admin(results=None):
  form = TreatySearchForm(request.form)

  categories = []
  subcategories = []
  discriminations = []
  initialResults = db.session.query(Right).all()
  for result in initialResults:
    if result.cat not in categories:
      categories.append(result.cat)
    if result.subcat not in subcategories:
      subcategories.append(result.subcat)
    if result.disc not in discriminations:
      discriminations.append(result.disc)

  if request.method == 'POST':

    treatyResult = db.session.query(Treaty).filter(Treaty.name.contains(form.data['treatyName'])).first()
    results = db.session.query(TreatyToRight).filter_by(tid=treatyResult.id).all()

    return render_template('/main/admin.html', results = results, form=form, categories=categories, subcategories=subcategories,
    discriminations=discriminations)

  return render_template('main/admin.html', results = results, form = form, categories=categories, subcategories=subcategories,
    discriminations=discriminations)


## SEARCH -- test functionality
@main.route('/search', methods=['GET', 'POST'])
def search(results=None):
  form = TreatySearchForm(request.form)
  if request.method == 'POST':
    results = db.session.query(Treaty).filter(Treaty.name.contains(form.data['treatyName'])).all()
    return render_template('/layouts/search.html', results = results, form=form)

  return render_template('/layouts/search.html', results = results, form=form)

## TREATY -- test functionality
@main.route('/treaty')
def editPage():
  return render_template('/main/treaty.html')


## ADDING, MODIFYING, DELETING RECORDS
@main.route('/add/right/<string:c>/<string:s>/<string:d>')
def add_right(c, s, d):
  result = Right.query.filter_by(cat=c, subcat=s, disc=d).with_entities(Right.id).first()
  if result is None:
    right = Right(cat=c, subcat=s, disc=d)
    db.session.add(right)
    db.session.commit()
    return Right.query.filter_by(cat=c, subcat=s, disc=d).with_entities(Right.id).first()[0]
  else: 
    return result[0]

@main.route('/add/ttof/<int:fi>/<int:ti>')
def add_ttof(fi, ti):
  if TreatyToForum.query.filter_by(fid=fi, tid=ti).first() is None:
    ttof = TreatyToForum(fid=fi, tid=ti)
    db.session.add(ttof)
    db.session.commit()
  return 'success'

@main.route('/add/forum/<string:n>')
def add_forum(n):
  result = Forum.query.filter_by(name=n).with_entities(Forum.id).first()
  if result is None:
    forum = Forum(name=n)
    db.session.add(forum)
    db.session.commit()
    return Forum.query.filter_by(name=n).with_entities(Forum.id).first()[0]
  else:
    return result[0]

@main.route('/add/ttor/<int:ri>/<int:ti>')
def add_ttor(ri, ti):
  if TreatyToRight.query.filter_by(rid=ri, tid=ti).first() is None:
    ttor = TreatyToRight(rid=ri, tid=ti)
    db.session.add(ttor)
    db.session.commit()
  return 'success'

@main.route('/add/treaty/<string:n>/<string:u>')
def add_treaty(n, u):
  result = Treaty.query.filter_by(name=n, url=u).with_entities(Treaty.id).first()
  if result is None:
    treaty = Treaty(name=n, url=u)
    db.session.add(treaty)
    db.session.commit()
    return Treaty.query.filter_by(name=n, url=u).with_entities(Treaty.id).first()[0]
  else:
    return result[0]

@main.route('/add/ttoc/<int:ci>/<int:ti>/<string:d>')
def add_ttoc(ci, ti, d):
  if TreatyToCountry.query.filter_by(cid=ci, tid=ti, date=d).first() is None:
    ttoc = TreatyToCountry(cid=ci, tid=ti, date=d)
    db.session.add(ttoc)
    db.session.commit()
  return 'success'

@main.route('/add/country/<string:n>')
def add_country(n):
  result = Country.query.filter_by(name=n).with_entities(Country.id).first()
  if result is None:
    country = Country(name= n)
    db.session.add(country)
    db.session.commit()
    return Country.query.filter_by(name=n).with_entities(Country.id).first()[0]
  else:
    return result[0]

@main.route('/delete/rights/cat/<string:c>')
def delete_rights_category(c):
  cats = Right.query.filter_by(cat=c).all()
  for i in range(len(cats)):
    db.session.delete(cats[i])
    db.session.commit()
    cats = Right.query.filter_by(cat=c).all()
  return 'success'

@main.route('/delete/rights/subcat/<string:s>')
def delete_rights_subcategory(s):
  subcats = Right.query.filter_by(subcat=s).all()
  while len(subcats) is not 0:
    db.session.delete(subcats)
    db.session.commit()
    subcats = Right.query.filter_by(subcat=s).all()
  return 'success'

@main.route('/delete/rights/disc/<string:d>')
def delete_rights_description(d):
  discs = Right.query.filter_by(disc=d).all()
  while len(discs) is not 0:
    db.session.delete(discs)
    db.session.commit()
    discs = Right.query.filter_by(disc=d).all()
  return 'success'

# @main.route('/delete/ttof/fid/<string:f>')
# def delete_ttof_fid(f):
#   ttof_entry = TreatyToForum.query.filter_by(fid=f).first()
#   if ttof_entry is not None:
#     db.session.delete(ttof_entry)
#     db.session.commit()
#   return 'success'

# @main.route('/delete/ttof/tid/<string:t>')
# def delete_ttof_tid(t):
#   ttof_entry = TreatyToForum.query.filter_by(tid=t).first()
#   if ttof_entry is not None:
#     db.session.delete(ttof_entry)
#     db.session.commit()
#   return 'success'

@main.route('/delete/ttof/fid/<string:f>/<string:t>')
def delete_ttof_fid(f,t):
  ttof_entry = TreatyToForum.query.filter_by(fid=f).filter_by(tid=t).first()
  if ttof_entry is not None:
    db.session.delete(ttof_entry)
    db.session.commit()
  return 'success'

@main.route('/delete/forum/<string:n>')
def delete_forum(n):
  forum = Forum.query.filter_by(name=n).first()
  if forum is not None:
    db.session.delete(forum)
    db.session.commit()
  return 'success'

@main.route('/delete/ttor/rid/<string:r>')
def delete_ttor_rid(r):
  ttor_entry = TreatyToRight.query.filter_by(rid=r).first()
  if ttor_entry is not None:
    db.session.delete(ttor_entry)
    db.session.commit()
  return 'success'

@main.route('/delete/ttor/tid/<string:t>')
def delete_ttor_fid(t):
  ttor_entry = TreatyToRight.query.filter_by(tid=t).first()
  if ttor_entry is not None:
    db.session.delete(ttor_entry)
    db.session.commit()
  return 'success'

# @main.route('/delete/treaty/<string:n>')
# def delete_treaty(n):
#   treaty = Treaty.query.filter_by(name=n).first()
#   if treaty is not None:
#     db.session.delete(treaty)
#     db.session.commit()
#   return 'success'

# only want to delete treaty based on both name and country
@main.route('/delete/treaty/<string:n>/<string:c>')
def delete_treaty(n,c):
  country = Country.query.filter_by(name=c).first()
  treaty = Treaty.query.filter_by(name=n).filter_by(cid=country.id).first()
  if treaty is not None:
    db.session.delete(treaty)
    db.session.commit()
  return 'success'

# @main.route('/delete/ttoc/cid/<string:c>')
# def delete_ttoc_cid(c):
#   ttoc_entry = TreatyToCountry.query.filter_by(cid=c).first()
#   if ttoc_entry is not None:
#     db.session.delete(ttoc_entry)
#     db.session.commit()
#   return 'success'

# @main.route('/delete/ttoc/tid/<string:t>')
# def delete_ttoc_tid(t):
#   ttoc_entry = TreatyToCountry.query.filter_by(tid=t)
#   if ttoc_entry is not None:
#     db.session.delete(ttoc_entry)
#     db.session.commit()
#   return 'success'

# only want to delete treatytocountry entry based on both country and treaty
@main.route('/delete/ttoc/cid/<string:t>/<string:c>')
def delete_ttoc_cid_tid(t, c):
  ttoc_entry = TreatyToCountry.query.filter_by(cid=c).filter_by(tid=t).first()
  if ttoc_entry is not None:
    db.session.delete(ttoc_entry)
    db.session.commit()
  return 'success'

## FILTERING -- USER SIDE

@main.route('/start')
def startLanding():
    countries = db.session.query(Country).all()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return render_template('/layouts/landing.html', countries = countries, months = months)

@main.route('/start/<country>')
def endLanding(country):
    country = db.session.query(Country).filter_by(name = country).all()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return render_template('/layouts/landing.html', countries = [country], months = months)

@main.route(('/start/<country>'), methods = ['POST'])
def submitLanding(country):
    country = db.session.query(Country).filter_by(name = country).all()
    db.session.add(country);
    db.session.commit();
    return jsonify(dict(redirect=url_for('layouts.index')))

@main.route('/form')
def startForm():
    rights = db.session.query(Right).all()
    categories = []
    subcategories = []
    discrimination = []
    for right in rights:
        categories.append(right.cat)
    return render_template('/layouts/index.html', categories=categories,
    subcategories=subcategories, discrimination=discrimination)
    # return str(rights)

@main.route('/form/<category>')
def showCategory(category):
    rights = db.session.query(Right).filter_by(cat=category).all()
    subcategories = []
    discrimination = []
    for right in rights:
        subcategories.append(right.subcat)
    return render_template('/layouts/index.html', categories=[category],
    subcategories=subcategories, discrimination=discrimination)
    #return str(rights)

@main.route('/form/<category>/<subcategory>')
def showSubcategory(category, subcategory):
    rights = db.session.query(Right).filter_by(cat=category).filter(or_(Right.subcat==subcategory, Right.subcat=="")).all()
    discrimination = []
    for right in rights:
        discrimination.append(right.disc)
    return render_template('/layouts/index.html', categories=[category],
    subcategories=[subcategory], discrimination=discrimination)
    #return str(rights)

@main.route('/form/<category>/<subcategory>/<discrimination>')
def showDiscrimination(category, subcategory, discrimination):
    rights = db.session.query(Right).filter_by(cat=category).filter(or_(Right.subcat==subcategory, Right.subcat=="")).filter(or_(Right.disc==discrimination, Right.disc=="")).all()
    return render_template('/layouts/index.html', categories=[category],
    subcategories=[subcategory], discrimination=[discrimination]);
    #return str(rights)

## FILTERING -- ADMIN SIDE

@main.route('/results')
def showResults():
    right = db.session.query(Right).filter_by(
        cat=session['Category'],
        subcat=session['Subcategory'],
        disc=session['Discrimination']).all()
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


## ADMIN FILTERING
@main.route('/country/<string:country>')
def FilterTreatyByCountry(country):
    # country = db.session.query(Country).filter_by(name=country).first()
    # ttoc = db.session.query(TreatyToCountry).filter_by(cid=country.id).all()
    # treaties =[]
    # for entry in ttoc:
    #     treaties.append(db.session.query(Treaty).filter_by(id=entry.tid).first())
    treaties = db.session.query(Treaty).join(Country, Treaty.cid == Country.id).filter(Country.name == country)
    return treaties

@main.route('/forum/<string:forum>')
def FilterTreatyByForum(forum):
    # forum = db.session.query(Forum).filter_by(name=forum).first()
    # ttof = db.session.query(TreatyToForum).filter_by(fid=forum.id).all()
    # treaties = []
    # for entry in ttof:
    #     treaties.append(db.session.query(Treaty).filter_by(id=entry.tid).first())
    treaties = db.session.query(Treaty).join(Forum, Treaty.fid == Forum.id).filter(Forum.name == forum)
    return treaties

@main.route('/discrimination/<string:discrimination>')
def FilterByDiscrimination(discrimination):
    # right = db.session.query(Right).filter_by(disc=discrimination).first()
    # rightsids = db.session.query(TreatyToRight).filter_by(rid=rights.id).all()
    # treaties = []
    # for entry in rightsids:
    #     treaties.append(db.session.query(Treaty).filter_by(id=entry.tid).first())
    treaties = db.session.query(Treaty).join(TreatyToRight, Treaty.id == TreatyToRight.tid).join(Right).filter(TreatyToRight.rid == Right.id, Right.disc == discrimination)
    return treaties

@main.route('/subcategory/<string:subcat>')
def FilterBySubcategory(subcat):
    # right = db.session.query(Right).filter_by(subcat=subcat).first()
    # rights = db.session.query(TreatyToRight).filter_by(rid=right.id).all()
    # treaties = []
    # for entry in rights:
    #     treaties.append(db.session.query(Treaty).filter_by(id=entry.tid).first())
    treaties = db.session.query(Treaty).join(TreatyToRight, Treaty.id == TreatyToRight.tid).join(Right).filter(TreatyToRight.rid == Right.id, Right.subcat == subcat)
    return treaties

# @main.route('/date/<datetime:date>/<string:subcategory>/<string:category>/<string:discrimination>/<string:forum>'country)
# def FilterTreatybyDate(date):
#     treatyids = db.session.query(TreatyToCountry).filter(TreatyToCountry.date>= date).with_entities(TreatyToCountry.tid)
#     for tid in treatyids:
#         treatylist.append(db.session.query(Treaty).filter_by(Treaty.id = tid)
#     return treaties

## TESTING ROUTES ## 

@main.route('/testrights')
def testAddingR():
    rights = db.session.query(Right).all()
    categories = []
    subcategories = []
    discrimination = []
    for right in rights:
        categories.append(right.cat)
        subcategories.append(right.subcat)
        discrimination.append(right.disc)
    return str(rights)

@main.route('/testtreaties')
def testAddingT():
    treaties = db.session.query(Treaty).all()
    return str(treaties)

@main.route('/testforums')
def testAddingF():
    forums = db.session.query(Forum).first().name
    return str(forums)

@main.route('/testcountries')
def testAddingC():
    countries = db.session.query(Country).all()
    return str(countries)

@main.route('/testttor')
def testAddingTtor():
    ttors = db.session.query(TreatyToRight).all()
    return str(ttors)
    
@main.route('/date/<date>')
def FilterTreatybyDate(date):
    input_date = datetime.strptime(date, "%m-%d-%Y").date()
    treatyids = db.session.query(TreatyToCountry).filter(datetime.strptime(TreatyToCountry.date, "%m-%d-%Y").date() >= input_date).with_entities(TreatyToCountry.tid)
    treatylist = []
    for tid in treatyids:
        treatylist.append(db.session.query(Treaty).filter_by(id = tid))
    return str(treatylist)

@main.route('/multiple/<string:cat>/<string:subcat>/<string:disc>/<string:forum>/<string:country>/<date>/')
def FilterTreatybyMultiple(date, subcat, cat, disc, forum, country):
    rights = db.session.query(Right).filter_by(cat=category, subcat=subcategory, disc=discrimination).all().with_entities(Right.id)
    treatyIds = []
    for right in rights:
      treatyIds.extend(db.session.query(TreatyToRight).filter_by(rid=right).all())

    country = db.session.query(Country).filter_by(name=country).first().with_entities(Country.id)
    forum = db.session.query(Forum).filter_by(name=forum).first().with_entities(Forum.id)
    input_date = datetime.strptime(date, "%m-%d-%Y").date()

    return "hello"


