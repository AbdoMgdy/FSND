from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def attach_db(app):
    db.init_app(app)
    return db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    seeking_description = db.Column(db.String(120))
    seeking_talent = db.Column(db.String())
    website = db.Column(db.String())
    shows = db.relationship('Show', backref='venue', lazy=True, cascade="all")
    # TODO: implement any missing fields, as a database migration using Flask-Migrate [Done]


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))
    show = db.relationship('Show', backref='artist', lazy=True, cascade="all")

    # TODO: implement any missing fields, as a database migration using Flask-Migrate [Done]

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration [Done]


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete="CASCADE"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete="CASCADE"), nullable=False)
