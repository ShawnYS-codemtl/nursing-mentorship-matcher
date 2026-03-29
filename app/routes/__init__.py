from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register routes
    from app.routes.matches import matches_bp
    from app.routes.matching import matching_bp
    from app.routes.import_routes import import_bp
    from app.routes.stats import stats_bp
    from app.routes.unmatched import unmatched_bp

    app.register_blueprint(matches_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(import_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(unmatched_bp)
    print(app.url_map)

    @app.route("/")
    def home():
        return "Mentorship Matcher Running"

    return app