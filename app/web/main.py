from flask import render_template
from sqlalchemy import desc

from app.models.gift import Gift
from app.view_models.book import BookViewModel
from . import web


__author__ = '七月'


@web.route('/')
def index():
    gift_list = Gift.recent()
    books = [BookViewModel(gift.book.first) for gift in gift_list]

    return render_template('index.html',recent=books)



@web.route('/personal')
def personal_center():
    pass
