from flask import Blueprint

admin = Blueprint('admin',__name__)

from record.views import index