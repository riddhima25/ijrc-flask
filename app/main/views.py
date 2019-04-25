from flask import Blueprint, render_template, session, jsonify, request, redirect, flash, url_for

from app.models import EditableHTML
from .. import db
from ..models import Right, Forum, Country, TreatyToCountry, TreatyToRight, TreatyToForum, Results, Treaty
from .forms import TreatySearchForm

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

@main.route('/add/right/<string:c>/<string:s>/<string:d>')
def add_right(c, s, d):
    if Right.query.filter_by(cat=c, subcat=s, disc=d).first() is None:
      right = Right(cat=c, subcat=s, disc=d)
      db.session.add(right)
      db.session.commit()
    return 'success'

@main.route('/add/ttof/<int:fi>/<int:ti>')
def add_ttof(fi, ti):
    if TreatyToForum.query.filter_by(fid=fi, tid=ti).first() is None:
      tttof = TreatyToForum(fid=fi, tid=ti)
      db.session.add(ttof)
      db.session.commit()
    return 'success'

@main.route('/add/forum/<string:n>')
def add_forum(n):
  if Forum.query.filter_by(name=n).first() is None:
    forum = Forum(name=n)
    db.session.add(forum)
    db.session.commit()
  return 'success'

@main.route('/add/ttor/<int:ri>/<int:ti>')
def add_ttor(ri, ti):
  if TreatyToRight.query.filter_by(rid=ri, tid=ti).first() is None:
    ttor = TreatyToRight(rid=ri, tid=ti)
    db.session.add(ttor)
    db.session.commit()
  return 'success'

@main.route('/add/treaty/<string:n>/<string:u>')
def add_treaty(n, u):
  if Treaty.query.filter_by(name=n, url=u) is None:
    treaty = Treaty(name=n, url=u)
    db.session.add(treaty)
    db.session.commit()
  return 'success'

@main.route('/add/ttoc/<int:ci>/<int:ti>/<string:d>')
def add_ttoc(ci, ti, d):
  if TreatyToCountry.query.filter_by(cid=ci, tid=ti, date=d).first() is None:
    ttoc = TreatyToCountry(cid=ci, tid=ti, date=d)
    db.session.add(ttoc)
    db.session.commit()
  return 'success'

@main.route('/add/country/<string:n>')
def add_country(n):
  if Country.query.filter_by(name=n).first() is None:
    country = Country(name= n)
    db.session.add(country)
    db.session.commit()
  return 'success'

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
    session['Country'] = country
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return render_template('/layouts/landing.html', countries = country, months = months)

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
        subcategories.append(right.subcat)
        discrimination.append(right.disc)
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
        discrimination.append(right.disc)
    return render_template('/layouts/index.html', categories=[category],
    subcategories=subcategories, discrimination=discrimination)
    #return str(rights)

@main.route('/form/<category>/<subcategory>')
def showSubcategory(category, subcategory):
    rights = db.session.query(Right).filter_by(cat=category, subcat=subcategory).all()
    discrimination = []
    for right in rights:
        discrimination.append(right.disc)
    return render_template('/layouts/index.html', categories=[category],
    subcategories=[subcategory], discrimination=discrimination)
    #return str(rights)

@main.route('/form/<category>/<subcategory>/<discrimination>')
def showDiscrimination(category, subcategory, discrimination):
    rights = db.session.query(Right).filter_by(cat=category, subcat=subcategory, disc=discrimination).all()
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

@main.route('/results')
def showResults():
    results = Results.query.all();
    return render_template('/layouts/client_side_results.html', 
      country = session['Country'],
      date = session['Date'],
      results=results)

## SEARCH
@main.route('/search', methods=['GET', 'POST'])
def search(results=None):
  form = TreatySearchForm(request.form)
  #treaties = models.Course.query

  if request.method == 'POST':
      return (search.treatyName.data)
      #courses = courses.filter(models.Course.name.like('%' + search.treatyName.data + '%')

  return render_template('/layouts/search.html', results = results, form=form)

## ADMIN FILTERING
@main.route('/country/<string:country>')
def FilterTreatyByCountry(country):
    country = db.session.query(Country).filter_by(name=country).first()
    ttoc = db.session.query(TreatyToCountry).filter_by(cid=country.id).all()
    treaties =[]
    for entry in ttoc:
        treaties.append(db.session.query(Treaty).filter_by(id=entry.tid).first())
    return treaties

@main.route('/forum/<string:forum>')
def FilterTreatyByForum(forum):
    forum = db.session.query(Forum).filter_by(name=forum).first()
    ttof = db.session.query(TreatyToForum).filter_by(fid=forum.id).all()
    treaties = []
    for entry in ttof:
        treaties.append(db.session.query(Treaty).filter_by(id=entry.tid).first())
    return treaties

@main.route('/discrimination/<string:discrimination>')
def FilterByDiscrimination(discrimination):
    right = db.session.query(Right).filter_by(disc=discrimination).first()
    rightsids = db.session.query(TreatyToRight).filter_by(rid=rights.id).all()
    treaties = []
    for entry in rightsids:
        treaties.append(db.session.query(Treaty).filter_by(id=entry.tid).first())
    return treaties

@main.route('/subcategory/<string:subcat>')
def FilterBySubcategory(subcat):
    right = db.session.query(Right).filter_by(subcat=subcat).first()
    rights = db.session.query(TreatyToRight).filter_by(rid=right.id).all()
    treaties = []
    for entry in rights:
        treaties.append(db.session.query(Treaty).filter_by(id=entry.tid).first())
    return treaties

