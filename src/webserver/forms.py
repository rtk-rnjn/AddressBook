from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddressForm(FlaskForm):
    recipient_name = StringField("Recipient Name", validators=[DataRequired()])
    organization_name = StringField("Organization Name")
    building_number = StringField("Building Number")
    apartment_number = StringField("Apartment Name")
    street_name = StringField("Street Name")
    city = StringField("City")
    state = StringField("State", validators=[DataRequired()])
    postal_code = StringField("Postal Code")

    submit = SubmitField("Submit")
