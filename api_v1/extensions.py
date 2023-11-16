"""
Este módulo registra as extensões do Flask utilizadas no projeto.
"""

from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_apscheduler import APScheduler

db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()
