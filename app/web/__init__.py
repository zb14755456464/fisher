from flask import Blueprint, url_for, render_template

__author__ = '七月'

web = Blueprint('web', __name__, template_folder='templates')



@web.app_errorhandler(404)
def error_code_404(e):
    return render_template('404.html')


from app.web import auth
from app.web import main
from app.web import book
from app.web import wish
from app.web import gift
from app.web import drift
