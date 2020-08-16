from jeffcupdb import util
from jeffcupdb.db.database import db
from jeffcupdb.db.model.champions import Champions
from jeffcupdb.db.model.matchups import Matchups
from jeffcupdb.db.model.owners import Owners
from jeffcupdb.db.model.records import Records
from jeffcupdb.db.model.sackos import Sackos
from jeffcupdb.db.model.teams import Teams
from jeffcupdb.db.query import Query
from jeffcupdb.views.champions import champions
from jeffcupdb.views.h2h_records import h2h_records
from jeffcupdb.views.matchup_history import matchup_history
from jeffcupdb.views.standings import standings
from flask import Flask, redirect
import logging
import sys

LOG_FORMAT = "%(asctime)s %(levelname)s %(pathname)s %(lineno)d: %(message)s"

app = Flask(__name__)
app.config.from_object(util.get_config())
app.register_blueprint(champions)
app.register_blueprint(h2h_records)
app.register_blueprint(matchup_history)
app.register_blueprint(standings)
app.static_folder = "web/static"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get("DB_URI")
db.init_app(app)
query = Query(db)
app.config['QUERY'] = query


@app.template_filter()
def number_format(value):
    return "{:,}".format(value)


@app.before_first_request
def setup_logging():
    if not app.debug:
        formatter = logging.Formatter(LOG_FORMAT)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)


@app.route('/', methods=['GET'])
def show_index():
    return redirect("/standings/overall", code=302)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
