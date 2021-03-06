from jeffcupdb.db.database import db


class Sackos(db.Model):
    PKEY_NAME = "sackos_year_pkey"

    year = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.String, nullable=False)
    db.PrimaryKeyConstraint(year, name=PKEY_NAME)

    def __str__(self):
        return ', '.join("%s: %s" % item for item in vars(self).items() if "_json" not in item)

    def __repr__(self):
        return ', '.join("%s: %s" % item for item in vars(self).items() if "_json" not in item)

    def __key(self):
        return (
            self.year,
            self.owner_id
        )

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.__key() == other.__key()

    def as_dict(self):
        return {
            'year': self.year,
            'owner_id': self.owner_id
        }

    def props_dict(self):
        return self.as_dict()
