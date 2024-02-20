from flask import Flask

from .extensions import db, bcrypt, migrate, login_manager


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "cfef780a42e7539644a62d963efb6242"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///insurance_database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from root.main.routes import main
    from root.users.routes import users
    from root.insurance.routes import insurances

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(insurances)

    return app
