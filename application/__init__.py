from flask import Flask, app
from config import DevConfig
from extensions import db, ma, limiter, cache
from models import Customer, Mechanic, ServiceTicket


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    

    from application.blueprints.customers import customers_bp
    app.register_blueprint(customers_bp, url_prefix='/customers')

    from application.blueprints.mechanics import mechanics_bp
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    
    from application.blueprints.service_tickets import service_tickets_bp
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')

    from application.blueprints.inventory import inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    with app.app_context():
        db.create_all()

    return app