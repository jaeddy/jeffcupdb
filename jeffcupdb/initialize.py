import argparse
from jeffcupdb import util
from jeffcupdb.db import create, insert
from jeffcupdb.db.database import db
from flask import Flask
from typing import Mapping

app = Flask(__name__)


def parse_args() -> Mapping:
    """

    :return: dict of parsed arguments
    """
    parser = argparse.ArgumentParser(description="Create tables and insert into database.")
    return vars(parser.parse_args())


def main():
    # args = parse_args()
    app.config.from_object(util.get_config())

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get("DB_URI")
    db.init_app(app)

    with app.app_context():
        create.main()
        insert.main()


if __name__ == "__main__":
    main()
