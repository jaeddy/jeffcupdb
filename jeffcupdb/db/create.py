import argparse
from jeffcupdb import util
from jeffcupdb.db.database import db
# noinspection PyUnresolvedReferences
from jeffcupdb.db.model import champions, matchups, owners, records, sackos, teams
from flask import Flask
import logging
from typing import Mapping

app = Flask(__name__)


def parse_args() -> Mapping:
    """

    :return: dict of parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Create tables and insert into database.")
    return vars(parser.parse_args())


# noinspection DuplicatedCode
def main():
    args = parse_args()
    config = util.get_config()
    app.config.from_object(util.get_config())
    util.set_logger(config=config, filename=__file__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get("DB_URI")
    db.init_app(app)

    with app.app_context():
        logging.info("Dropping tables")
        db.drop_all()
        logging.info("Creating tables")
        db.create_all()


if __name__ == "__main__":
    main()
