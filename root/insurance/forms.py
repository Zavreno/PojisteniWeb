from wtforms import StringField, SubmitField, IntegerField, SelectField, DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class AddInsurance(FlaskForm):
    insurance_name = SelectField("Pojištění", choices=[("Pojištění majetku", "Pojištění majetku"),
                                                       ("Pojištění osob", "Pojištění osob"),
                                                       ("Cestovní pojištění", "Cestovní pojištění"),
                                                       ("Zdravotní pojištění", "Zdravotní pojištění")])
    amount = IntegerField("Částka", validators=[DataRequired()])
    insured_item = StringField("Předmět pojištění", validators=[DataRequired()])
    valid_from = DateField("Platný od", validators=[DataRequired()])
    valid_till = DateField("Platný dd", validators=[DataRequired()])
    submit = SubmitField("Uložit")


class EditInsurance(FlaskForm):
    insurance_name = SelectField("Pojištění", choices=[("Pojištění majetku", "Pojištění majetku"),
                                                       ("Pojištění osob", "Pojištění osob"),
                                                       ("Cestovní pojištění", "Cestovní pojištění"),
                                                       ("Zdravotní pojištění", "Zdravotní pojištění")])
    amount = IntegerField("Částka", validators=[DataRequired()])
    insured_item = StringField("Předmět pojištění", validators=[DataRequired()])
    valid_from = DateField("Platný od", validators=[DataRequired()])
    valid_till = DateField("Platný dd", validators=[DataRequired()])
    submit = SubmitField("Uložit")
