from flask import Flask, redirect, url_for

from apps import Dining_info, Dish, First, Stu
from config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(First.views_bp)
    app.register_blueprint(Dish.dish_bp)
    app.register_blueprint(Stu.stu_bp)
    app.register_blueprint(Dining_info.dining_bp)

    @app.route("/")
    def index():
        return redirect(url_for("views.index"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run()
    
