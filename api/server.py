#!/usr/bin/python3
# coding: utf-8
"""Api server and db

Usage:
  server.py run [--db-location=<str>] [--debug]
  server.py (-h | --help)

Options:
  -h --help             Show this screen.
  --db-location=<path>  Set the database location (e.g sqlite:////tmp/test.db) [default: in-memory].
  --debug               Allow to stop the server on /shutdown
"""

from docopt import docopt

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_potion.routes import Relation
from flask_potion import Api, fields, ModelResource

debug = False

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

###
# Defining database
###


db = SQLAlchemy(app)

class Campaign(db.Model):
    id_campaign = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    decription = db.Column(db.String(150))
    id_rederbro = db.Column(db.Integer)

class Sensors(db.Model):
    id_sensors = db.Column(db.Integer, primary_key=True)
    # gps
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)
    alt = db.Column(db.Float)
    # Compass
    degrees = db.Column(db.Float)
    minutes = db.Column(db.Float)

class Lot(db.Model):
    id_lot = db.Column(db.Integer, primary_key=True)
    pictures_path = db.Column(db.Integer, nullable=False)
    goprofailed = db.Column(db.Integer, nullable=False)
    takenDate = db.Column(db.DateTime, nullable=False)

    id_sensors = db.Column(db.Integer, db.ForeignKey('sensors.id_sensors'), nullable=False)
    sensors = db.relationship('Sensors', uselist=False, backref=backref('lot', lazy='dynamic'), foreign_keys=[id_sensors])

    id_campaign = db.Column(db.Integer, db.ForeignKey('campaign.id_campaign'), nullable=False)
    campaign = db.relationship('Campaign', backref=backref('lots', lazy='dynamic'), foreign_keys=[id_campaign])

    id_tile = db.Column(db.Integer, db.ForeignKey('tile.id_tile'))
    tile = db.relationship('Tile', uselist=False, foreign_keys=[id_tile])

class Cp(db.Model):
    id_cp = db.Column(db.Integer, primary_key=True)
    search_algo_version = db.Column(db.String(20), nullable=False)
    nb_cp = db.Column(db.Integer, nullable=False)
    stichable = db.Column(db.Boolean, nullable=False)
    optimized = db.Column(db.Boolean, default=False)

    id_lot = db.Column(db.Integer, db.ForeignKey('lot.id_lot'), nullable=False)
    lot = db.relationship(Lot, backref=backref('cps', lazy='dynamic'))

class Panorama(db.Model):
    id_panorama = db.Column(db.Integer, primary_key=True)
    equirectangular_path = db.Column(db.Integer)

    id_cp = db.Column(db.Integer, db.ForeignKey('cp.id_cp'), nullable=False)
    cp = db.relationship(Cp, backref=backref('panorama', lazy='dynamic'))

class Tile(db.Model):
    id_tile = db.Column(db.Integer, primary_key=True)
    param_location = db.Column(db.Integer, nullable=False)
    fallback_path = db.Column(db.Integer, nullable=False)
    extension = db.Column(db.String(5), nullable=False)
    resolution = db.Column(db.Integer, nullable=False)
    max_level = db.Column(db.Integer, nullable=False)
    cube_resolution = db.Column(db.Integer, nullable=False)

    id_panorama = db.Column(db.Integer, db.ForeignKey('panorama.id_panorama'), nullable=False)
    panorama = db.relationship(Panorama, uselist=False, backref=backref('tiles', lazy='dynamic'), foreign_keys=[id_panorama])

###
# Defining all ressources
###

class SensorsRessource(ModelResource):
    lot = Relation('lot')

    class Meta:
        model = Sensors

class CampaignRessource(ModelResource):
    lots = Relation('lot')

    class Meta:
        model = Campaign

class LotRessource(ModelResource):
    cps = Relation('cp')

    class Meta:
        model = Lot

    class Schema:
        campaign = fields.ToOne('campaign')
        sensors = fields.ToOne('sensors')

class ParonamaRessource(ModelResource):
    tiles = Relation('tile')

    class Meta:
        model = Panorama

    class Schema:
        cp = fields.ToOne('cp')

class CpRessource(ModelResource):
    panorama = Relation('panorama')

    class Meta:
        model = Cp

    class Schema:
        lot = fields.ToOne('lot')

class TileRessource(ModelResource):
    class Meta:
        model = Tile

    class Schema:
        panorama = fields.ToOne('panorama')


api = Api(app)
api.add_resource(TileRessource)
api.add_resource(ParonamaRessource)
api.add_resource(CpRessource)
api.add_resource(LotRessource)
api.add_resource(SensorsRessource)
api.add_resource(CampaignRessource)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    if debug:
        shutdown_server()
        return 'Server shutting down...'
    return "You can't shut the server down"

def makeAndRun(db_location):
    if db_location and db_location != "in-memory":
        app.config['SQLALCHEMY_DATABASE_URI'] = db_location
    db.create_all()
    app.run()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    debug = bool(arguments.get('--debug'))
    makeAndRun(arguments['--db-location'])
