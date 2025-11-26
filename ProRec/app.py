"""
ProRec Flask Application Factory.
Main entry point for the application.
"""
import os
from flask import Flask, redirect, url_for
from config import config
from extensions import db, login_manager, init_extensions


def create_app(config_name=None):
    """
    Application factory pattern.
    Creates and configures the Flask application.

    Args:
        config_name: Configuration to use ('development', 'production', 'testing')

    Returns:
        Configured Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app.config.from_object(config[config_name])

    # Initialize extensions
    init_extensions(app)

    # Register Flask-Login user loader
    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login."""
        return User.query.get(int(user_id))

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Register context processors
    register_context_processors(app)

    # Create upload directory if it doesn't exist
    upload_folder = app.config.get('UPLOAD_FOLDER')
    if upload_folder and not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    return app


def register_blueprints(app):
    """
    Register all application blueprints.

    Args:
        app: Flask application instance
    """
    from routes.auth import auth_bp
    from routes.producer import producer_bp
    from routes.curator import curator_bp
    from routes.admin import admin_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(producer_bp)
    app.register_blueprint(curator_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Root route - redirect to login
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))


def register_error_handlers(app):
    """
    Register error handlers for common HTTP errors.

    Args:
        app: Flask application instance
    """
    from flask import render_template

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_context_processors(app):
    """
    Register template context processors.

    Args:
        app: Flask application instance
    """
    from flask_login import current_user

    @app.context_processor
    def utility_processor():
        """Make utility functions available in templates."""
        return {
            'current_user': current_user,
        }


# Create application instance
app = create_app()


if __name__ == '__main__':
    # Run development server (localhost only for security)
    app.run(host='127.0.0.1', port=5000, debug=True)
