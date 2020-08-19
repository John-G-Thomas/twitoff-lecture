"""Entry point for Twitoff."""
# from twitoff import app
from .app import create_app

APP = create_app()
