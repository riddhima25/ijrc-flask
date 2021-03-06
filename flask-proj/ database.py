from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp/test/db" #ask about this, what does it mean?
db = SQLAlchemy(app)

#

class Rights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.string(80), unique = False, nullable = True)
    subcat = db.Column(db.string(80), unique = False, nullable = True)
    disc= db.Column(db.string(80), unique = False, nullable = True)

    #primary key for category, subcategory adn discrimination? - Riddhima 
    #cat = category, subcat = subcategory, disc = discrimination.
    def __repr__(self):
        return "< Rights (cat = '%s', subcat = '%s', disc = '%s')>" % (
        self.cat, self.subcat, self.disc)
        #ask if this is accurate for flask sqlalchemy

class TtoF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, foreign_key=True, db.ForeignKey('Forum.id'))
    tid = db.Column(db.Integer, foreign_key=True, db.ForeignKey('Treaty.id'))
    #fid = forum id, tid = treaty id

    #ask about the id, how to state that they came from different tables
    def __repr__(self):
        return "<TtoF (fid ='%s', tid = '%s') %r>" % (self.rid , self.tid)


class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Forum %r>' % self.name

        #fix : string() and %r %s ask about.

class TtoR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, foreign_key=True, db.ForeignKey('Rights.id'))
    tid = db.Column(db.Integer, foreign_key=True, db.ForeignKey('Treaty.id'))

    #ask about the id, how to state that they came from different tables
    #ask about foreign key true and how refered to.
    def __repr__(self):
        return "<TtoR (rid ='%s', tid = '%s') %r>" % (self.rid , self.tid)
