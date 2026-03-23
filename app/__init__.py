import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///pharmacie.db",
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", os.path.join(app.root_path, "uploads"))
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp as main_bp

    app.register_blueprint(main_bp)

    with app.app_context():
        from . import models  # noqa: F401
        # db.create_all() # Commenté pour éviter les conflits si la table existe déjà sans la colonne
        try:
            db.create_all()
        except Exception:
            pass
        seed_if_empty()

    return app


def seed_if_empty():
    from .models import Product
    if Product.query.count() == 0:
        demo_products = [
            Product(name="Paracétamol 500mg", quantity=25),
            Product(name="Amoxicilline 1g", quantity=0),
            Product(name="Ibuprofène 400mg", quantity=40),
            Product(name="Vitamine C 1g", quantity=12),
        ]
        db.session.add_all(demo_products)
        db.session.commit()

