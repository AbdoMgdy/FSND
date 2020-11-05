#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
from datetime import datetime
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler, error
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database [Done]

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

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data [Done]
    # num_shows should be aggregated based on number of upcoming shows per venue.
    data = []

    venues = Venue.query.all()
    for venue in venues:
        data.append({
            'city': venue.city,
            'state': venue.state,
            'venues': [
                {
                    'id': venue.id,
                    'name': venue.name,
                    'num_upcoming_shows': len([0 for show in venue.shows if show.start_time < datetime.now()])
                }
            ]
        })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive [Done]
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.contains(search_term)).all()
    response = {
        "count": 0,
        "data": []
    }
    if venues:
        for venue in venues:
            response['data'].append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': len([0 for show in venue.shows if show.start_time < datetime.now()])
            })
            response['count'] += 1
        return render_template('pages/search_venues.html', results=response, search_term=search_term)
    return 'Error Venue not found !', 404


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id [Done]
    data = {}
    venue = Venue.query.get(venue_id)
    if venue:
        data['id'] = venue.id
        data['name'] = venue.name
        data['genres'] = venue.genres.replace('{', '').replace('}', '').split(',')
        data['address'] = venue.address
        data['city'] = venue.city
        data['state'] = venue.state
        data['phone'] = venue.phone
        data['facebook_link'] = venue.facebook_link
        data['past_shows'] = [{
            'artist_id': show.artist_id,
            'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        } for show in venue.shows if show.start_time < datetime.now()]
        data['upcoming_shows'] = [{
            'artist_id': show.artist_id,
            'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        } for show in venue.shows if show.start_time > datetime.now()]
        data['past_shows_count'] = len([0 for show in venue.shows if show.start_time < datetime.now()])
        data['upcoming_shows_count'] = len([0 for show in venue.shows if show.start_time > datetime.now()])
        return render_template('pages/show_venue.html', venue=data)
    return 'Error Venue not found !', 404

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead [Done]
    # TODO: modify data to be the data object returned from db insertion
    temp = {}
    temp['name'] = request.form.get('name', '')
    temp['city'] = request.form.get('city', '')
    temp['address'] = request.form.get('address', '')
    temp['city'] = request.form.get('city', '')
    temp['state'] = request.form.get('state', '')
    temp['genres'] = request.form.getlist('genres', '')
    temp['facebook_link'] = request.form.get('facebook_link', '')
    temp['phone'] = request.form.get('phone', '')
    error = False
    try:
        venue = Venue(**temp)
        db.session.add(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    # TODO: on unsuccessful db insert, flash an error instead [Done]
    if error:

        flash('An error occured. Venue ' + request.form['name'] + 'coulb not be listed.')
    # on successful db insert, flash success
    else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return 'Venue Deleted.'

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database [Done]
    data = []
    artists = Artist.query.all()
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive[Done]
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {'count': 0, 'data': []}
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.contains(search_term)).all()
    if artists:
        for artist in artists:
            response['data'].append({
                'id': artist.id,
                'name': artist.name,
                'num_upcoming_shows': len([0 for show in artist.show if show.start_time < datetime.now()])
            })
            response['count'] += 1

        return render_template('pages/search_artists.html', results=response, search_term=search_term)
    return 'Artist Not Found !', 404


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id [Done]
    # data1 = {
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "genres": ["Rock n Roll"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "326-123-5000",
    #     "website": "https://www.gunsnpetalsband.com",
    #     "facebook_link": "https://www.facebook.com/GunsNPetals",
    #     "seeking_venue": True,
    #     "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #     "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "past_shows": [{
    #         "venue_id": 1,
    #         "venue_name": "The Musical Hop",
    #         "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #         "start_time": "2019-05-21T21:30:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data2 = {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    #     "genres": ["Jazz"],
    #     "city": "New York",
    #     "state": "NY",
    #     "phone": "300-400-5000",
    #     "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    #     "seeking_venue": False,
    #     "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #     "past_shows": [{
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2019-06-15T23:00:00.000Z"
    #     }],
    #     "upcoming_shows": [],
    #     "past_shows_count": 1,
    #     "upcoming_shows_count": 0,
    # }
    # data3 = {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    #     "genres": ["Jazz", "Classical"],
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "432-325-5432",
    #     "seeking_venue": False,
    #     "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "past_shows": [],
    #     "upcoming_shows": [{
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-01T20:00:00.000Z"
    #     }, {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-08T20:00:00.000Z"
    #     }, {
    #         "venue_id": 3,
    #         "venue_name": "Park Square Live Music & Coffee",
    #         "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #         "start_time": "2035-04-15T20:00:00.000Z"
    #     }],
    #     "past_shows_count": 0,
    #     "upcoming_shows_count": 3,
    # }
    # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    artist = Artist.query.get(artist_id)
    if artist:
        data = {}
        data['id'] = artist.id
        data['name'] = artist.name
        data['genres'] = artist.genres.replace('{', '').replace('}', '').split(',')
        data['city'] = artist.city
        data['state'] = artist.state
        data['phone'] = artist.phone
        data['facebook_link'] = artist.facebook_link
        data['past_shows'] = [{
            'artist_id': show.artist_id,
            'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        } for show in artist.show if show.start_time < datetime.now()]
        data['upcoming_shows'] = [{
            'artist_id': show.artist_id,
            'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        } for show in artist.show if show.start_time > datetime.now()]
        data['past_shows_count'] = len([0 for show in artist.show if show.start_time < datetime.now()])
        data['upcoming_shows_count'] = len([0 for show in artist.show if show.start_time > datetime.now()])

        return render_template('pages/show_artist.html', artist=data)
    return 'Artist not found !', 404

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    if artist:
        data = {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres,
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link
        }
    # TODO: populate form with fields from artist with ID <artist_id> [Done]
        return render_template('forms/edit_artist.html', form=form, artist=data)

    return 'Artist not Found', 404


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    artist = Artist.query.get(artist_id)
    error = False
    if artist:
        try:
            artist.name = request.form.get('name', '')
            artist.genres = request.form.getlist('genres', '')
            artist.city = request.form.get('city', '')
            artist.state = request.form.get('state', '')
            artist.phone = request.form.get('phone', '')
            artist.website = request.form.get('website', '')
            artist.facebook_link = request.form.get('facebook_link', '')
            artist.seeking_venue = request.form.get('seeking_venue', '')
            artist.seeking_description = request.form.get('seeking_description', '')
            artist.image_link = request.form.get('image_link', '')
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        if error:
            flash('An error occurred.')
        else:
            flash('Artist was successfully updated!')

    # artist record with ID <artist_id> using the new attributes

        return redirect(url_for('show_artist', artist_id=artist_id))
    return 'Artist Was not found.', 404


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm()
    if venue:
        data = {
            "id": venue.id,
            "name": venue.name,
            "genres": venue.genres,
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link
        }

    # TODO: populate form with values from venue with ID <venue_id> [Done]

        return render_template('forms/edit_venue.html', form=form, venue=data)
    return 'Venue not found.', 404


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing [Done]
    venue = Venue.query.get(venue_id)
    error = False
    if venue:
        try:
            venue.name = request.form.get('name', '')
            venue.address = request.form.get('address', '')
            venue.genres = request.form.get.getlist('genres,''')
            venue.city = request.form.get('city', '')
            venue.state = request.form.get('state', '')
            venue.phone = request.form.get('phone', '')
            venue.website = request.form.get('website', '')
            venue.facebook_link = request.form.get('facebook_link', '')
            venue.seeking_talent = request.form.get('seeking_talent', '')
            venue.seeking_description = request.form.get('seeking_description', '')
            venue.image_link = request.form.get('image_link', '')
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            flash('An error occurred. Venue could not be updated.')
        else:
            flash('Venue was successfully updated!')
    # venue record with ID <venue_id> using the new attributes
        return redirect(url_for('show_venue', venue_id=venue_id))
    return 'Venue not found', 404

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead [Done]
    # TODO: modify data to be the data object returned from db insertion [Done]

    data = {}
    data['name'] = request.form.get('name', '')
    data['city'] = request.form.get('city', '')
    data['state'] = request.form.get('state', '')
    data['genres'] = request.form.get('genres', '')
    data['facebook_link'] = request.form.get('facebook_link', '')
    data['phone'] = request.form.get('phone', '')
    error = False
    try:
        artist = Artist(**data)
        db.session.add(artist)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    # TODO: on unsuccessful db insert, flash an error instead. [Done]
    if error:
        flash('An error occurred. Artist ' + request.form.get('name', '') + ' could not be listed.')
    # on successful db insert, flash success
    else:
        flash('Artist ' + request.form.get('name', '') + ' was successfully listed!')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data [Donw]
    data = []
    shows = Show.query.all()
    for show in shows:
        artist = Artist.query.get(show.artist_id)
        venue = Venue.query.get(show.venu_id)
        data.append({
            "venue_id": show.venue_id,
            "venue_name": venue.name,
            "artist_id": show.artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead [Done]
    data = {}
    data['artist_id'] = request.form('artist_id', '')
    data['venue_id'] = request.form('venue_id', '')
    data['start_time'] = request.form('start_time', '')
    error = False
    try:
        show = Show(**data)
        db.session.add(show)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    # TODO: on unsuccessful db insert, flash an error instead. [Done]
    if error:
        flash('An error occurred. Show could not be listed.')
    # on successful db insert, flash success
    else:
        flash('Show was successfully listed!')

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
