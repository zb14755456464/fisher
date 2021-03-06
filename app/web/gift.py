from app.libs.enums import PendingStatus
from app.models.drift import Drift
from flask import render_template, flash, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from sqlalchemy import desc, func

from . import web
from app.spider.yushu_book import YuShuBook
from app.view_models.gift import MyGifts

from app.models import db
from app.models.gift import Gift

@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
        desc(Gift.create_time)).all()
    wishes_count = Gift.get_wish_counts(gifts) # [(数量，isbn编号)，(数量，isbn编号)]
    view_model = MyGifts(gifts, wishes_count).package()
    return render_template('my_gifts.html', gifts=view_model)



@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    # gifting = Gift.query.filter_by(uid=current_user.id, isbn=isbn, status=1,
    #                                launched=False).first()
    # wishing = Wish.query.filter_by(uid=current_user.id, isbn=isbn, status=1,
    #                                launched=False).first()
    if current_user.can_save_to_list(isbn):
        # 既不在赠送清单，也不在心愿清单才能添加
        with db.auto_commit():
            gift = Gift()
            gift.uid = current_user.id
            gift.isbn = isbn
            # gift.book_id = yushu_book.data.id
            db.session.add(gift)
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass



