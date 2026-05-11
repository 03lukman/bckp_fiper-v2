from flask import Flask
from app.core.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Import Blueprint di dalam fungsi (mencegah circular import)
    from app.modules.auth.routes import auth_bp
    from app.modules.dashboard.routes import dashboard_bp
    from app.modules.documents.routes import documents_bp
    
    app.register_blueprint(documents_bp)
    
    # 2. Registrasi Blueprint
    # url_prefix='/' membuat rute login ada di alamat utama (misal: localhost:5000/)
    app.register_blueprint(auth_bp, url_prefix='/')
    
    # Tanpa prefix membuat rute dashboard ada di /dashboard sesuai definisi di routes.py
    app.register_blueprint(dashboard_bp)

    return app