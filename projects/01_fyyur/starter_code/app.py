#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from enum import unique
import sys
import json
from datetime import datetime
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler, error
from flask_wtf import Form
from flask_wtf import form
from forms import *
from flask_migrate import Migrate, show
from sqlalchemy import distinct
from models import attach_db, Artist, Venue, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# TODO: connect to a local postgresql database [Done]
db = attach_db(app)
migrate = Migrate(app, db)

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
    q = db.session.query(Venue).distinct(Venue.city, Venue.state).all()
    for v in q:
        data.append({'city': v.city,
                     'state': v.state,
                     'venues': []
                     })
    print(data)
    venues = Venue.query.all()
    for i, v in enumerate(data):
        for venue in venues:
            print(i, v)
            if v['city'] == venue.city and v['state'] == venue.state:
                data[i]["venues"].append({'id': venue.id,
                                          'name': venue.name,
                                          'num_upcoming_shows': len([0 for show in venue.shows if show.start_time < datetime.now()])
                                          })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive [Done]
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.contains(search_term.lower())).all()
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


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id [Done]
    data = {}
    shows = []
    join_query = db.session.query(Venue, Show).filter(Venue.id == Show.venue_id).first()
    venue = join_query[0]
    if join_query[1] is not list:
        shows.append(join_query[1])
    else:
        shows = join_query[1]
    if venue:
        data['id'] = venue.id
        data['name'] = venue.name
        data['genres'] = venue.genres
        data['address'] = venue.address
        data['city'] = venue.city
        data['state'] = venue.state
        data['phone'] = venue.phone
        data['facebook_link'] = venue.facebook_link
        data['past_shows'] = [{
            'artist_id': show.artist_id,
            'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        } for show in shows if show.start_time < datetime.now()]
        data['upcoming_shows'] = [{
            'artist_id': show.artist_id,
            'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        } for show in shows if show.start_time > datetime.now()]
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
    form = VenueForm()
    temp = {}
    temp['name'] = request.form.get('name', '')
    temp['city'] = request.form.get('city', '')
    temp['address'] = request.form.get('address', '')
    temp['city'] = request.form.get('city', '')
    temp['state'] = request.form.get('state', '')
    temp['genres'] = request.form.get('genres', '')
    temp['seeking_description'] = request.form.get('seeking_description', '')
    if request.form.get('seeking_talent') == 'y':
        temp['seeking_talent'] = True
    else:
        temp['seeking_talent'] = False
    temp['facebook_link'] = request.form.get('facebook_link', '')
    temp['image_link'] = request.form.get('image_link', '')
    temp['website'] = request.form.get('website', '')
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


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id [Done]
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
    form = ArtistForm()
    print(request.form)
    data = {}
    data['name'] = request.form.get('name', '')
    data['city'] = request.form.get('city', '')
    data['state'] = request.form.get('state', '')
    data['genres'] = request.form.get('genres', '')
    data['facebook_link'] = request.form.get('facebook_link', '')
    data['image_link'] = request.form.get('image_link', '')
    data['website'] = request.form.get('website', '')
    if request.form.get('seeking_venue', '') == 'y':
        data['seeking_venue'] = True
    else:
        data['seeking_venue'] = False
    data['seeking_description'] = request.form.get('seeking_description', '')
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
        venue = Venue.query.get(show.venue_id)
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
    form = ShowForm()
    if form.validate():
        data = {}
        data['artist_id'] = request.form.get('artist_id', '')
        data['venue_id'] = request.form.get('venue_id', '')
        data['start_time'] = request.form.get('start_time', '')
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
    return 'Invalid or Missing Input', 401


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
