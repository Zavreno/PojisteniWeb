from .extensions import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(260), nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    insurance = db.relationship("InsuredPersons", lazy=True, backref="insured_person")

    def __repr__(self):
        return f"Users('{self.first_name}', '{self.last_name}', '{self.email}', '{self.city}', '{self.address}', '{self.zip}')"


class InsuredPersons(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(260), nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    insurance = db.relationship("Insurances", lazy=True, backref="author")


class Insurances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    i_person_id = db.Column(db.Integer, db.ForeignKey(InsuredPersons.id))
    insurance_name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    insured_item = db.Column(db.String(60), nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_till = db.Column(db.DateTime, nullable=False)
