from sqlalchemy.orm import validates
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, IntegerField, HiddenField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import email_validator
from root.models import InsuredPersons


class LoginForm(FlaskForm):
    email = EmailField("Emailová adresa",
                       validators=[DataRequired(), Email()])
    password = PasswordField("Heslo",
                             validators=[DataRequired()])
    remember = BooleanField("Zapamatovat údaje")
    submit = SubmitField("Přihlásit")


class RegistrationForm(FlaskForm):
    first_name = StringField("Jméno",
                             validators=[DataRequired(), Length(min=1, max=15)])
    last_name = StringField("Příjmení",
                             validators=[DataRequired(), Length(min=1, max=15)])
    email = EmailField("Emailová adresa",
                       validators=[DataRequired(), Email()])
    password = PasswordField("Heslo",
                             validators=[DataRequired(), Length(min=5, max=30)])
    confirm_password = PasswordField("Potvrzení hesla",
                             validators=[DataRequired(), EqualTo("password")])
    city = StringField("Město",
                             validators=[DataRequired(), Length(min=1, max=15)])
    address = StringField("Adresa",
                             validators=[DataRequired(), Length(min=1, max=15)])
    zip = IntegerField("Zip", validators=[DataRequired()])
    submit = SubmitField("Zaregistrovat")

    @validates('first_name', 'last_name', 'city', 'address')
    def capitalize_name(self, key, value):
        return value.capitalize()


class AddNewInsuredPerson(FlaskForm):
    first_name = StringField("Jméno",
                             validators=[DataRequired(), Length(min=1, max=15)])
    last_name = StringField("Příjmení",
                            validators=[DataRequired(), Length(min=1, max=15)])
    email = EmailField("Emailová adresa",
                       validators=[DataRequired(), Email()])
    city = StringField("Město",
                       validators=[DataRequired(), Length(min=1, max=15)])
    address = StringField("Adresa",
                          validators=[DataRequired(), Length(min=1, max=15)])
    zip = IntegerField("Zip", validators=[DataRequired()])
    submit = SubmitField("Přidat")


class EditInsuredPerson(FlaskForm):
    first_name = StringField("Jméno",
                             validators=[DataRequired(), Length(min=1, max=15)])
    last_name = StringField("Příjmení",
                            validators=[DataRequired(), Length(min=1, max=15)])
    original_email = HiddenField()
    email = EmailField("Emailová adresa",
                       validators=[DataRequired(), Email()])
    city = StringField("Město",
                       validators=[DataRequired(), Length(min=1, max=15)])
    address = StringField("Adresa",
                          validators=[DataRequired(), Length(min=1, max=15)])
    zip = IntegerField("Zip", validators=[DataRequired()])
    submit = SubmitField("Uložit")

    def validate_email(self, email):
        user = InsuredPersons.query.filter_by(email=email.data).first()

        if user and email.data != self.original_email.data:
            raise ValidationError("Tato emailová adresa je již zabraná jiným uživatelem!")

