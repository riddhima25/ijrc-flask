from .. import db
#import flask.ext.whooshalchemy

#table where each result is kept because we want to allow the user
#to fill out the form multiple times
class Results(db.Model):
    __tablename__ = 'Results'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, db.ForeignKey('Right.id'))
    cid = db.Column(db.Integer, db.ForeignKey('Country.id'))
    tid = db.Column(db.Integer, db.ForeignKey('Treaty.id'))
    fid = db.Column(db.Integer, db.ForeignKey('Forum.id'))
    right = db.relationship("Right", backref="Results", uselist=False)
    treaty = db.relationship("Treaty", backref="Results", uselist=False)
    forum = db.relationship("Forum", backref="Results", uselist=False)
    country = db.relationship("Country", uselist=False, backref="Results")

class Right(db.Model):
    __tablename__ = 'Right'
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(80), unique = False, nullable = True)
    subcat = db.Column(db.String(80), unique = False, nullable = True)
    disc= db.Column(db.String(80), unique = False, nullable = True)
    ttor = db.relationship("TreatyToRight", uselist=False, backref="Right")
    result = db.relationship("Results", uselist=False, backref="Right")
    tfc = db.Column(db.Integer, db.ForeignKey('TreatyForumCountry.id'))

    #cat = category, subcat = subcategory, disc = discrimination.
    def __repr__(self):
        return "< Rights (cat = '%s', subcat = '%s', disc = '%s')>" % (
        self.cat, self.subcat, self.disc)
        #ask if this is accurate for flask sqlalchemy

class Forum(db.Model):
    __tablename__ = 'Forum'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    ttof = db.relationship("TreatyToForum", uselist=False, backref="Forum")
    result = db.relationship("Results", uselist=False, backref="Forum")

    def __repr__(self):
        return '<Forum %r>' % self.name

        #fix : string() and %r %s ask about.

class Country(db.Model):
    __tablename__ = 'Country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    ttoc = db.relationship("TreatyToCountry", uselist=False, backref="Country")
    result = db.relationship("Results", uselist=False, backref="Country")

    def __init__(self, name):
        self.name = name

class Treaty(db.Model):
    __tablename__ = 'Treaty'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    url = db.Column(db.String(1000))
    ttof = db.relationship("TreatyToForum", uselist=False, backref="Treaty")
    ttor = db.relationship("TreatyToRight", uselist=False, backref="Treaty")
    ttoc = db.relationship("TreatyToCountry", uselist=False, backref="Treaty")
    result = db.relationship("Results", uselist=False, backref="Treaty")

    def __init__(self, name, url):
        self.name = name
        self.url = url


class TreatyToForum(db.Model):
    __tablename__ = 'TreatyToForum'
    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, db.ForeignKey('Forum.id'))
    tid = db.Column(db.Integer, db.ForeignKey('Treaty.id'))
    treaty = db.relationship("Treaty", backref="TreatyToForum", uselist=False)
    forum = db.relationship("Forum", backref="TreatyToForum", uselist=False)

    #fid = forum id, tid = treaty id

    #ask about the id, how to state that they came from different tables
    def __repr__(self):
        return "<TtoF (fid ='%s', tid = '%s') %r>" % (self.rid , self.tid)

class TreatyToRight(db.Model):
    __tablename__ = 'TreatyToRight'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, db.ForeignKey('Right.id'))
    tid = db.Column(db.Integer, db.ForeignKey('Treaty.id'))
    treaty = db.relationship("Treaty", backref="TreatyToRight", uselist=False)
    right = db.relationship("Right", backref="TreatyToRight", uselist=False)


    #ask about the id, how to state that they came from different tables
    #ask about foreign key true and how refered to.
    def __repr__(self):
        return "<TtoR (rid ='%s', tid = '%s') %r>" % (self.rid , self.tid)

class TreatyToCountry(db.Model):
    __tablename__ = 'TreatyToCountry'
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey('Country.id'))
    tid = db.Column(db.Integer, db.ForeignKey('Treaty.id'))
    date = db.Column(db.String(80))
    treaty = db.relationship("Treaty", backref="TreatyToCountry", uselist=False)
    country= db.relationship("Country", backref="TreatyToCountry", uselist=False)


    def __init__(self, cid, tid, date):
        self.date = date

class TreatyForumCountry(db.Model):
    __tablename__ = 'TreatyForumCountry'
    id = db.Column(db.Integer, primary_key=True)
    treaty = db.Column(db.String(100))
    country = db.Column(db.String(80))
    url = db.Column(db.String(1000))
    forum = db.Column(db.String(1000))
    date = db.Column(db.String(1000))
    right = db.relationship("Right")

    def __init__(self, treaty, forum, country, date, url):
        self.treaty = treaty
        self.forum = forum
        self.country = country
        self.date = date
        self.url = url
