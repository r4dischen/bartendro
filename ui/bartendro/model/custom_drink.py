# -*- coding: utf-8 -*-
from bartendro import db
from sqlalchemy import Column, Integer, UnicodeText, ForeignKey


class CustomDrink(db.Model):
    """
    This class provides details about customizable drinks. 
    """

    __tablename__ = 'custom_drink'
    id = Column(Integer, primary_key=True)
    drink_id = Column(Integer, ForeignKey('drink.id'), nullable=False)
    name = Column(UnicodeText, nullable=False)

    query = db.session.query_property()

    def __init__(self, name=u''):
        self.name = name
        db.session.add(self)

    def __repr__(self):
        return "<CustomDrink(%d,<Drink>(%d),'%s')>" % (self.id or -1,
                                                       self.drink_id,
                                                       self.name)
