from flask import Blueprint, render_template, flash, redirect, url_for, request
from root.models import InsuredPersons, Insurances
from root.extensions import db
from root.insurance.forms import AddInsurance, EditInsurance
from flask_login import login_required, current_user


insurances = Blueprint("insurances", __name__, template_folder="templates")


@insurances.route("/účet/<int:user_id>/nové_pojištění", methods=["GET", "POST"])
@login_required
def add_insurance(user_id):
    form = AddInsurance()
    if current_user and (current_user.email != "admin@blog.com"):
        user = InsuredPersons.query.filter_by(user_id=current_user.id).first()
        if form.validate_on_submit():
            insurance = Insurances(insurance_name=form.insurance_name.data, author=user, amount=form.amount.data,
                                   insured_item=form.insured_item.data, valid_from=form.valid_from.data,
                                   valid_till=form.valid_till.data)
            db.session.add(insurance)
            db.session.commit()
            flash("Nové pojištění bylo úspěšně uloženo!", "success")
            return redirect(url_for("users.my_account"))
    else:
        user = InsuredPersons.query.get_or_404(user_id)
        if form.validate_on_submit():
            insurance = Insurances(insurance_name=form.insurance_name.data, author=user, amount=form.amount.data,
                                   insured_item=form.insured_item.data, valid_from=form.valid_from.data,
                                   valid_till=form.valid_till.data)
            db.session.add(insurance)
            db.session.commit()
            flash("Nové pojištění bylo úspěšně uloženo!", "success")
            return redirect(url_for("users.user_account", user_id=user.id))
    return render_template("add_insurance.html", title="Nové pojištění", form=form, user=user)


@insurances.route("/účet/<int:user_id>/úprava_pojištění/<int:ins_id>", methods=["GET", "POST"])
@login_required
def edit_insurance(user_id, ins_id):
    form = EditInsurance()
    if current_user and (current_user.email != "admin@blog.com"):
        user = InsuredPersons.query.filter_by(user_id=current_user.id).first()
        ins = Insurances.query.get_or_404(ins_id)
        if form.validate_on_submit():
            ins.insurance_name = form.insurance_name.data
            ins.amount = form.amount.data
            ins.insured_item = form.insured_item.data
            ins.valid_from = form.valid_from.data
            ins.valid_till = form.valid_till.data
            db.session.commit()
            flash("Změny byly uloženy!", "success")
            return redirect(url_for("users.my_account"))
        elif request.method == "GET":
            form.insurance_name.data = ins.insurance_name
            form.amount.data = ins.amount
            form.insured_item.data = ins.insured_item
            form.valid_from.data = ins.valid_from
            form.valid_till.data = ins.valid_till
    else:
        user = InsuredPersons.query.get_or_404(user_id)
        ins = Insurances.query.get_or_404(ins_id)
        if form.validate_on_submit():
            ins.insurance_name = form.insurance_name.data
            ins.amount = form.amount.data
            ins.insured_item = form.insured_item.data
            ins.valid_from = form.valid_from.data
            ins.valid_till = form.valid_till.data
            db.session.commit()
            flash("Změny byly uloženy!", "success")
            return redirect(url_for("users.user_account", user_id=user.id))
        elif request.method == "GET":
            form.insurance_name.data = ins.insurance_name
            form.amount.data = ins.amount
            form.insured_item.data = ins.insured_item
            form.valid_from.data = ins.valid_from
            form.valid_till.data = ins.valid_till
    return render_template("edit_insurance.html", form=form, user=user, ins=ins, title="Úprava pojištění")


@insurances.route("/účet/<int:user_id>/odstranění_pojištění", methods=["POST"])
@login_required
def delete_insurance(user_id):
    if current_user and (current_user.email != "admin@blog.com"):
        user = InsuredPersons.query.filter_by(user_id=current_user.id)
        ins_id = request.form.get("ins_id")
        ins = Insurances.query.get_or_404(ins_id)
        db.session.delete(ins)
        db.session.commit()
        flash("Pojištění bylo odstraněno!", "info")
        return redirect(url_for('users.my_account'))
    else:
        user = InsuredPersons.query.get_or_404(user_id)
        ins_id = request.form.get("ins_id")
        ins = Insurances.query.get_or_404(ins_id)
        db.session.delete(ins)
        db.session.commit()
        flash("Pojištění bylo odstraněno!", "info")
        return redirect(url_for('users.user_account', user_id=user.id))
