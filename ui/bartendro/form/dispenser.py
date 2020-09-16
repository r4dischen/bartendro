#!/usr/bin/env python
from wtforms import Form, SubmitField


class DispenserForm(Form):
    save = SubmitField(u"save")
    cancel = SubmitField(u"cancel")


form = DispenserForm()
