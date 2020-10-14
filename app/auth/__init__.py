from flask import Blueprint

bp = Blueprint("auth", __name__)
# ei je eikhane auth register korlam blueprint e and then ei register kora jaigar sob theke import file re niche import korlam

from app.auth import routes

