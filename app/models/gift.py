from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, desc, func
from sqlalchemy.orm import relationship
from app.models.base import Base
from flask import current_app

from app.view_models.book import BookViewModel
from app.models import db


class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self, uid):
        if self.uid == uid:
            return True

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book

        # @classmethod
        # @cache.memoize(timeout=600)
        # def recent(cls):
        #     gift_list = cls.query.filter_by(launched=False).order_by(
        #         desc(Gift.create_time)).group_by(Gift.book_id).limit(
        #         current_app.config['RECENT_BOOK_PER_PAGE']).distinck().all()
        #     view_model = GiftsViewModel.recent(gift_list)
        #     return view_model

    @staticmethod
    def recent():
        gift_list = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_PER_PAGE']).distinct().all()

        return gift_list

    @staticmethod
    def get_wish_counts(gifts):
        book_isbn_list = [gift.isbn for gift in gifts]
        count_list = db.session.query(func.count(Wish.id), Wish.isbn). \
            filter(Wish.launched == False, Wish.isbn.in_(book_isbn_list),
                   Wish.status == 1).group_by(Wish.isbn).all()

        return count_list
