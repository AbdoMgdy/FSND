from datetime import datetime

from flask_wtf import Form
from wtforms import (DateTimeField, SelectField, SelectMultipleField,
                     StringField)
from wtforms.fields.core import BooleanField
from wtforms.validators import (URL, AnyOf, DataRequired, Length,
                                ValidationError)


class VenueForm(Form):

    name = StringField(
        'name', validators=[DataRequired()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[('Alternative', 'Alternative'),
                 ('Blues', 'Blues'),
                 ('Classical', 'Classical'),
                 ('Country', 'Country'),
                 ('Electronic', 'Electronic'),
                 ('Folk', 'Folk'),
                 ('Funk', 'Funk'),
                 ('Hip-Hop', 'Hip-Hop'),
                 ('Heavy Metal', 'Heavy Metal'),
                 ('Instrumental', 'Instrumental'),
                 ('Jazz', 'Jazz'),
                 ('Musical Theatre', 'Musical Theatre'),
                 ('Pop', 'Pop'),
                 ('Punk', 'Punk'),
                 ('R&B', 'R&B'),
                 ('Reggae', 'Reggae'),
                 ('Rock n Roll', 'Rock n Roll'),
                 ('Soul', 'Soul'),
                 ('Other', 'Other'), ]
    )
    address = StringField(
        'address', validators=[DataRequired(), Length(max=120)]
    )
    city = StringField(
        'city', validators=[DataRequired(), Length(max=120)]
    )
    state = SelectField(
        'state', validators=[DataRequired(), Length(max=120)],
        choices=[('AL', 'AL'),
                 ('AK', 'AK'),
                 ('AZ', 'AZ'),
                 ('AR', 'AR'),
                 ('CA', 'CA'),
                 ('CO', 'CO'),
                 ('CT', 'CT'),
                 ('DE', 'DE'),
                 ('DC', 'DC'),
                 ('FL', 'FL'),
                 ('GA', 'GA'),
                 ('HI', 'HI'),
                 ('ID', 'ID'),
                 ('IL', 'IL'),
                 ('IN', 'IN'),
                 ('IA', 'IA'),
                 ('KS', 'KS'),
                 ('KY', 'KY'),
                 ('LA', 'LA'),
                 ('ME', 'ME'),
                 ('MT', 'MT'),
                 ('NE', 'NE'),
                 ('NV', 'NV'),
                 ('NH', 'NH'),
                 ('NJ', 'NJ'),
                 ('NM', 'NM'),
                 ('NY', 'NY'),
                 ('NC', 'NC'),
                 ('ND', 'ND'),
                 ('OH', 'OH'),
                 ('OK', 'OK'),
                 ('OR', 'OR'),
                 ('MD', 'MD'),
                 ('MA', 'MA'),
                 ('MI', 'MI'),
                 ('MN', 'MN'),
                 ('MS', 'MS'),
                 ('MO', 'MO'),
                 ('PA', 'PA'),
                 ('RI', 'RI'),
                 ('SC', 'SC'),
                 ('SD', 'SD'),
                 ('TN', 'TN'),
                 ('TX', 'TX'),
                 ('UT', 'UT'),
                 ('VT', 'VT'),
                 ('VA', 'VA'),
                 ('WA', 'WA'),
                 ('WV', 'WV'),
                 ('WI', 'WI'),
                 ('WY', 'WY'), ]
    )
    phone = StringField(
        'phone', validators=[DataRequired()]
    )
    website = StringField(
        'website', validators=[DataRequired(), URL(), Length(max=120)]
    )
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired(), URL()]
    )
    seeking_talent = BooleanField(
        'seeking_talent'
    )
    seeking_description = StringField(
        'seeking_description', validators=[Length(max=500)]
    )
    image_link = StringField(
        'image_link', validators=[DataRequired(), URL(), Length(max=500)]
    )
# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM [Done]


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired(), Length(max=120)]
    )
    city = StringField(
        'city', validators=[DataRequired(), Length(max=120)]
    )
    state = SelectField(
        # TODO implement validation logic for state
        'state', validators=[DataRequired(), Length(max=120)],
        choices=[('AL', 'AL'),
                 ('AK', 'AK'),
                 ('AZ', 'AZ'),
                 ('AR', 'AR'),
                 ('CA', 'CA'),
                 ('CO', 'CO'),
                 ('CT', 'CT'),
                 ('DE', 'DE'),
                 ('DC', 'DC'),
                 ('FL', 'FL'),
                 ('GA', 'GA'),
                 ('HI', 'HI'),
                 ('ID', 'ID'),
                 ('IL', 'IL'),
                 ('IN', 'IN'),
                 ('IA', 'IA'),
                 ('KS', 'KS'),
                 ('KY', 'KY'),
                 ('LA', 'LA'),
                 ('ME', 'ME'),
                 ('MT', 'MT'),
                 ('NE', 'NE'),
                 ('NV', 'NV'),
                 ('NH', 'NH'),
                 ('NJ', 'NJ'),
                 ('NM', 'NM'),
                 ('NY', 'NY'),
                 ('NC', 'NC'),
                 ('ND', 'ND'),
                 ('OH', 'OH'),
                 ('OK', 'OK'),
                 ('OR', 'OR'),
                 ('MD', 'MD'),
                 ('MA', 'MA'),
                 ('MI', 'MI'),
                 ('MN', 'MN'),
                 ('MS', 'MS'),
                 ('MO', 'MO'),
                 ('PA', 'PA'),
                 ('RI', 'RI'),
                 ('SC', 'SC'),
                 ('SD', 'SD'),
                 ('TN', 'TN'),
                 ('TX', 'TX'),
                 ('UT', 'UT'),
                 ('VT', 'VT'),
                 ('VA', 'VA'),
                 ('WA', 'WA'),
                 ('WV', 'WV'),
                 ('WI', 'WI'),
                 ('WY', 'WY'), ]
    )
    phone = StringField(
        'phone', validators=[DataRequired()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[('Alternative', 'Alternative'),
                 ('Blues', 'Blues'),
                 ('Classical', 'Classical'),
                 ('Country', 'Country'),
                 ('Electronic', 'Electronic'),
                 ('Folk', 'Folk'),
                 ('Funk', 'Funk'),
                 ('Hip-Hop', 'Hip-Hop'),
                 ('Heavy Metal', 'Heavy Metal'),
                 ('Instrumental', 'Instrumental'),
                 ('Jazz', 'Jazz'),
                 ('Musical Theatre', 'Musical Theatre'),
                 ('Pop', 'Pop'),
                 ('Punk', 'Punk'),
                 ('R&B', 'R&B'),
                 ('Reggae', 'Reggae'),
                 ('Rock n Roll', 'Rock n Roll'),
                 ('Soul', 'Soul'),
                 ('Other', 'Other'), ]
    )
    seeking_venue = BooleanField(
        'seeking_venue'
    )
    seeking_description = StringField(
        'seeking_description', validators=[Length(max=500)]
    )
    website = StringField(
        'website', validators=[DataRequired(), URL(), Length(max=120)]
    )
    image_link = StringField(
        'image_link', validators=[DataRequired(), URL(), Length(max=500)]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )
