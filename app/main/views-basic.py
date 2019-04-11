from flask import session
from app.models import treaty
from app.main import main

@main.route('/add/right/<string:c>/<string:s>/<string:d>')
def add_right():
    if Rights.query.filter_by(cat=c, subcat=s, desc=d).first() is None:
      right = Rights(cat=c, subcat=s, desc=d)
      db.session.add(right)
      db.session.commit()

@main.route('/add/ttof/<int:fi>/<int:ti>')
def add_ttof():
    if TreatyToForum.query.filter_by(fid=fi, tid=ti).first() is None:
      tttof = TreatyToForum(fid=fi, tid=ti)
      db.session.add(ttof)
      db.session.commit()

@main.route('/add/forum/<string:n>')
def add_forum():
  if Forum.query.filter_by(name=n).first() is None:
    forum = Forum(name=n)
    db.session.add(forum)
    db.session.commit()

@main.route('/add/ttor/<int:ri>/<int:ti>')
def add_ttor():
  if TreatyToRight.query.filter_by(rid=ri, tid=ti).first() is None:
    ttor = TreatytoRight(rid=ri, tid=ti)
    db.session.add(ttor)
    db.session.commit()

@main.route('/add/treaty/<string:n>/<string:u>')
def add_treaty():
  if Treaty.query.filter_by(name=n, url=u) is None:
    treaty = Treaty(name=n, url=u)
    db.session.add(treaty)
    db.session.commit()

@main.route('/add/ttoc/<int:ci>/<int:ri>/<string:d>')
def add_ttoc():
  if TreatyToCountry.query.filter_by(cid=ci, tid=ti, date=d).first() is None:
    ttoc = TreatyToCountry(cid=ci, tid=ti, date=d)
    db.session.add(ttoc)
    db.commit()

@main.route('/add/country/<string:n>')
def add_country():
  if Country.query.filter_by(name=n).first() is None:
    country = Country(name= n)
    db.session.add(country)
    db.commit()

@main.route('/delete/rights/cat/<string:c>')
def delete_rights_category():
  cats = Rights.query.filter_by(cat=c).all()
  while len(cats) is not 0:
    db.session.delete(cats)
    db.session.commit()
    cats = Rights.query.filter_by(cat=c).all()

@main.route('delete/rights/subcat/<string:s>')
def delete_rights_subcategory():
  subcats = Rights.query.filter_by(subcat=s).all()
  while len(subcats) is not 0:
    db.session.delete(subcats)
    db.session.commit()
    subcats = Rights.query.filter_by(subcat=s).all()

@main.route('delete/rights/disc/<string:d>')
def delete_rights_description():
  descs = Rights.query.filter_by(desc=d).all()
  while len(descs) is not 0:
    db.session.delete(descs)
    db.session.commit()
    descs = Rights.query.filter_by(desc=d).all()

@main.route('delete/ttof/fid/<string:f>')
def delete_ttof_fid():
  ttof_entry = TreatytoForum.query.filter_by(fid=f).first()
  if ttof_entry is not None:
    db.session.delete(ttof_entry)
    db.session.commit()

@main.route('delete/ttof/tid/<string:t>')
def delete_ttof_tid():
  ttof_entry = TreatytoFormat.query.filter_by(tid=t).first()
  if ttof_entry is not None:
    db.session.delete(ttof_entry)
    db.session.commit()

@main.route('delete/forum/<string:n>')
def delete_forum():
  forum = Forum.query.filter_by(name=n).first()
  if forum is not None:
    db.session.delete(forum)
    db.session.commit()

@main.route('delete/ttor/rid/<string:r>')
def delete_ttor_rid():
  ttor_entry = TreatyToRight.query.filter_by(rid=r).first()
  if ttor_entry is not None:
    db.session.delete(ttor_entry)
    db.session.commit()

@main.route('delete/ttor/tid/<string:t>')
def delete_ttor_fid():
  ttor_entry = TreatyToRight.query.filter_by(tid=t).first()
  if ttor_entry is not None:
    db.session.delete(ttor_entry)
    db.session.commit()

@main.route('delete/treaty/<string:n>')
def delete_treaty():
  treaty = Treaty.query.filter_by(name=n).first()
  if treaty is not None:
    db.session.delete(treaty)
    db.session.commit()

@main.route('delete/ttoc/cid/<string:c>')
def delete_ttoc_cid():
  ttoc_entry = TreatyToCountry.query.filter_by(countryid=c).first()
  if ttoc_entry is not None:
    db.session.delete(ttoc_entry)
    db.session.commit()

@main.route('delete/ttoc/tid/<string:t>')
def delete_ttoc_tid():
  ttoc_entry = TreatyToCountry.query.filter_by(treatyid=t)
  if ttoc_entry is not None:
    db.session.delete(ttoc_entry)
    db.session.commit()