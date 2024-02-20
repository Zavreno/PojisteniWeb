from flask import Blueprint, render_template, flash, redirect, url_for, request
from root.users.forms import LoginForm, RegistrationForm, AddNewInsuredPerson, EditInsuredPerson
from root.models import Users, InsuredPersons, Insurances
from root.extensions import db, bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_


users = Blueprint("users", __name__, template_folder="templates")


@users.route("/přihlášení", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Přihlášení proběhlo úspěšně!", "success")
            if user.email == "admin@blog.com":
                return redirect(url_for("main.home"))
            else:
                return redirect(url_for("users.my_account"))
        else:
            flash("Nepodařilo se přihlásit. Prosím zkontrolujte své údaje", "danger")
    return render_template("login.html", title="Přihlášení", form=form)


@users.route("/registrace", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                     password=hashed_password, city=form.city.data, address=form.address.data, zip=form.zip.data)
        db.session.add(user)
        db.session.commit()
        ip_id = user.id
        i_person = InsuredPersons(user_id=ip_id, first_name=form.first_name.data, last_name=form.last_name.data,
                                  email=form.email.data, city=form.city.data, address=form.address.data,
                                  zip=form.zip.data)
        db.session.add(i_person)
        db.session.commit()
        flash("Váš účet byl vytvořen. Nyní se můžete přihlásit!", 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", title="Registrace", form=form)


@users.route("/účet")
@login_required
def my_account():
    if current_user.email != "admin@blog.com":
        user = InsuredPersons.query.filter_by(user_id=current_user.id).first()
        page = request.args.get('page', 1, type=int)
        insuarences_list = Insurances.query.filter_by(i_person_id=user.id).paginate(page=page, per_page=5)
        return render_template("account.html", title="Můj účet", user=user, insurances_list=insuarences_list)


@users.route("/účet/<int:user_id>")
@login_required
def user_account(user_id):
    registered_user = Users.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    insurances_list = Insurances.query.filter_by(i_person_id=registered_user.id).paginate(page=page, per_page=5)
    return render_template("user_account.html", title="Účet", user=registered_user, insurances_list=insurances_list)


@users.route("/pojištěnec_účet/<int:user_id>")
@login_required
def insured_user_account(user_id):
    insured_user = InsuredPersons.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    insurances_list = Insurances.query.filter_by(i_person_id=insured_user.id).paginate(page=page, per_page=5)
    return render_template("user_account.html", title="Účet", user=insured_user, insurances_list=insurances_list)


@users.route("/odhlášení")
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/pojištěnci", methods=["POST", "GET"])
@login_required
def insured_persons():
    if current_user.email != "admin@blog.com":
        flash("Na tuto stránku nemáte povolení vstoupit!", "danger")
        return redirect(url_for("main.home"))
    page = request.args.get("page", 1, type=int)
    insured_persons_list = InsuredPersons.query.paginate(page=page, per_page=10)
    return render_template("insured_persons.html", title="Pojištěnci", insured_persons_list=insured_persons_list)


@users.route("/pojištěnci/odstranit", methods=["POST"])
def delete_insured_person():
    if current_user.email != "admin@blog.com":
        flash("Na tuto stránku nemáte povolení vstoupit!", "danger")
        return redirect(url_for("main.home"))
    user_id = request.form.get("user_id")
    user = InsuredPersons.query.get_or_404(user_id)
    insurances = Insurances.query.filter_by(i_person_id=user.id).all()
    if insurances:
        for ins in insurances:
            db.session.delete(ins)
    db.session.delete(user)
    db.session.commit()
    flash('Pojištěnec byl odstraněn!', "info")
    return redirect(url_for('users.insured_persons'))


@users.route("/pojištěnci/nový_pojištěnec", methods=["GET", "POST"])
@login_required
def add_insured_person():
    form = AddNewInsuredPerson()
    if form.validate_on_submit():
        user = InsuredPersons(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                              city=form.city.data, address=form.address.data, zip=form.zip.data)
        db.session.add(user)
        db.session.commit()
        flash('Byl přidán nový pojištěnec!', "info")
        return redirect(url_for('users.insured_persons'))
    return render_template("add_insured_person.html", title="Nový pojištěnec", form=form)


@users.route("/správa_uživatelů")
@login_required
def users_management():
    if current_user.email != "admin@blog.com":
        flash("Na tuto stránku nemáte povolení vstoupit!", "danger")
        return redirect(url_for("main.home"))
    page = request.args.get('page', 1, type=int)
    users_list = Users.query.paginate(per_page=10, page=page)
    return render_template("users_management.html", title="Uživatelé", users_list=users_list)


@users.route("/účet/<int:user_id>/úprava_údajů", methods=["GET", "POST"])
@login_required
def edit_insured_person(user_id):
    form = EditInsuredPerson()
    if current_user.email != "admin@blog.com":
        insured_person = InsuredPersons.query.filter_by(user_id=current_user.id).first()
        user = Users.query.get_or_404(current_user.id)
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.city = form.city.data
            user.address = form.address.data
            user.zip = form.zip.data

            insured_person.first_name = form.first_name.data
            insured_person.last_name = form.last_name.data
            insured_person.email = form.email.data
            insured_person.city = form.city.data
            insured_person.address = form.address.data
            insured_person.zip = form.zip.data
            db.session.commit()
            flash("Změny byly uloženy!", "success")
            return redirect(url_for("users.my_account"))
        elif request.method == "GET":
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.email.data = user.email
            form.original_email.data = user.email
            form.city.data = user.city
            form.address.data = user.address
            form.zip.data = user.zip
    else:
        user = InsuredPersons.query.get_or_404(user_id)
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.city = form.city.data
            user.address = form.address.data
            user.zip = form.zip.data
            db.session.commit()
            flash("Změny byly uloženy!", "success")
            return redirect(url_for("users.user_account", user_id=user.id))
        elif request.method == "GET":
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.email.data = user.email
            form.original_email.data = user.email
            form.city.data = user.city
            form.address.data = user.address
            form.zip.data = user.zip
    return render_template("edit_insured_person.html", title="Úprava údajů", form=form, user=user)


@users.route("/správa_uživatelů/odstranit", methods=["POST"])
def delete_user():
    if current_user.email != "admin@blog.com":
        flash("Na tuto stránku nemáte povolení vstoupit!", "danger")
        return redirect(url_for("main.home"))
    user_id = request.form.get("user_id")
    user = Users.query.get_or_404(user_id)
    insured_person = InsuredPersons.query.filter_by(user_id=user.id).first()
    if insured_person:
        insurances = Insurances.query.filter_by(i_person_id=insured_person.id).all()
        if insurances:
            for ins in insurances:
                db.session.delete(ins)
    db.session.delete(insured_person)
    db.session.delete(user)
    db.session.commit()
    flash('Uživatel byl odstraněn!', "info")
    return redirect(url_for('users.users_management'))
