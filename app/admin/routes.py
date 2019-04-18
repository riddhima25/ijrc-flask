import json
import os
import sys

from flask import (abort, jsonify, redirect, render_template, request,
                   send_from_directory, session, url_for)

from .. import db

@main.route('/country/<string:country>')
def startForm():
    for country in countryids:
        countryids.append(db.session.query(Country).filter_by(cid=x))
    return countryids
    treatyids = db.session.query(TreatyToCountry).filter_by(country=country).with_entities(TreatyToCountry.tid)
    for x in treatyids:
        treaties.append(db.session.query(Treaty).filter_by(tid=x))
    return treaties

@main.route('/forum/<string:forum>')
def startForm():
    forums = db.session.query(Forum).filter_by(forum=forum).with_entities(TreatyToCountry.ttof)
    for x in forums:
        forumlist.append(db.session.query(Treaty).filter_by(ttof=x))
    return forumlist

@main.route('/discrimination/<string:discrimination>')
def startForm():
    discriminations = db.session.query(Rights).filter_by(discrimination=discrimination).with_entities(Rights.discrimination)
    for discs in discriminations:
        disclist.append(db.session.query(Rights).filter_by(discrimination=discs))
    return disclist

@main.route('/subcategory/<string:subcategory>')
def startForm():
    subcategories = db.session.query(Rights).filter_by(subcategory=subcategory).with_entities(Rights.subcategory)
    for subs in subcategories:
        sublist.append(db.session.query(Rights).filter_by(subcategory=subs))
    return sublist

@main.route('/date/<datetime:date>')
def startForm():
    date = db.session.query(TreatyToCountry).filter_by(date=date).with_entities(TreatyToCountry.date)
    return date
    #because each treaty would have just one date for each coutry?

@main.route('/multiple/<datetime:date>')
def startForm():
    date = db.session.query(Treaty).filter_by(date=date).with_entities(Treaty.date)
    return date
    #because each treaty would have just one date for each coutry?


@main.route('/country/<string:country>')
def startForm():
    for country in countryids:
        countryids.append(db.session.query(Country).filter_by(cid=x))
    return countryids
    #what to do after? is this correct? ask tomorrow!

    treatyids = db.session.query(TreatyToCountry).filter_by(country=country).with_entities(TreatyToCountry.tid)
    for  in treatyids:
        treaties.append(db.session.query(Treaty).filter_by(tid=x))
    return treaties
