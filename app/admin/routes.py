import json
import os
import sys

from flask import (abort, jsonify, redirect, render_template, request,
                   send_from_directory, session, url_for)

from .. import db

@main.route('/country/<string:country>')
def FilterTreatyByCountry(country):
    country = db.session.query(Country).filter_by(country=country).first()
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
def FilterTreatyByDiscrimination(discrimination):
    rights = db.session.query(Rights).filter_by(discrimination=discrimination).first()
    rightsids = db.session.query(TreatyToRights).filter_by(rid=rights.id).all()
    treaties = []
    for entry in rightsids:
        treaties.append(db.session.query(Treaty).filter_by(id=entry.tid).first())
    return treaties

@main.route('/subcategory/<string:subcategory>')
def FilterTreatyBySubcategory(subcategory):
    subcategory = db.session.query(Rights).filter_by(subcat=subcategory).first()
    subcategories = db.session.query(Rights).filter_by(fid=rights.id).all()
    treaties = []
    for entry in subcategories:
        treaties.append(db.session.query(Treaty).filter_by(id=entry.tid).first())
    return treaties


@main.route('/multiple/<datetime:date>/<string:subcategory>/<string:category>/<string:discrimination>/<string:forum>'country)
def FilterTreatybyMultiple(multiple):
    treatyids = db.session.query(TreatyToCountry).filter(TreatyToCountry.date>= date).with_entities(TreatyToCountry.tid)
    for tid in treatyids:
        treatylist.append(db.session.query(Treaty).filter_by(Treaty.id = tid)
    return treaties

@main.route('/multiple/<multiple:date>')
def filterTreatyMultipleFilters():
