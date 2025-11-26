"""
Routes package initialization.
Register all blueprints here.
"""
from routes.auth import auth_bp

__all__ = ['auth_bp']
