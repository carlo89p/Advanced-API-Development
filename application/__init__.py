from flask import Flask, Response
from config import DevConfig
from extensions import db, ma, limiter, cache
from models import Customer, Mechanic, ServiceTicket
from flask_swagger_ui import get_swaggerui_blueprint
import os

SWAGGER_URL = '/api/docs'
API_URL = '/swagger/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Chop Shop API"}
)

def create_app(config=DevConfig):
    app = Flask(__name__)
    
    if isinstance(config, str):
        import importlib
        config_module = importlib.import_module('config')
        config = getattr(config_module, config)
    
    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'swagger.yaml')

    @app.route('/swagger/swagger.yaml')
    def swagger_yaml():
        with open(yaml_path, 'r') as f:
            content = f.read()
        return Response(content, mimetype='text/yaml')

    from application.blueprints.customers import customers_bp
    app.register_blueprint(customers_bp, url_prefix='/customers')

    from application.blueprints.mechanics import mechanics_bp
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')

    from application.blueprints.service_tickets import service_tickets_bp
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')

    from application.blueprints.inventory import inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    with app.app_context():
        db.create_all()

    return app