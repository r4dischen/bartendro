# -*- coding: utf-8 -*-
from bartendro import db
from sqlalchemy import Column, Integer, UnicodeText, Index


class Option(db.Model):
    """
    Configuration options for Bartendro
    """

    __tablename__ = 'option'
    id = Column(Integer, primary_key=True)
    key = Column(UnicodeText, nullable=False)
    value = Column(UnicodeText)

    query = db.session.query_property()

    def __init__(self, key='', value=''):
        self.key = key
        self.value = value

    def __repr__(self):
        return "<Option('%s','%s'='%s')>" % (self.id, self.key, self.value)


Index('options_key_ndx', Option.key)
