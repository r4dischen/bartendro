# -*- coding: utf-8 -*-
from bartendro import db
from sqlalchemy import Column, Integer, ForeignKey


class Dispenser(db.Model):
    """
    Information about a dispenser
    """

    __tablename__ = 'dispenser'
    id = Column(Integer, primary_key=True)
    booze_id = Column(Integer, ForeignKey('booze.id'), nullable=False)
    actual = Column(Integer, default=0)
    out = Column(Integer, default=0)

    query = db.session.query_property()

    def __init__(self, booze, actual):
        self.booze = booze
        self.booze_id = booze.id
        self.actual = actual

    def json(self):
        return {
            'id': self.id,
            'booze': self.booze_id
        }

    def __repr__(self):
        return "<Dispenser('%s','%s')>" % (self.id, self.booze_id)
