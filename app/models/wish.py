from app.spider.yushu_book import YuShuBook
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from app.models.base import Base, db


class Wish(Base):
    __tablename__ = 'wish'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book

    @classmethod
    def get_gifts_count(cls, wish_list):
        from app.models.gift import Gift

        book_isbn_list = [wish.isbn for wish in wish_list]
        count_list = db.session.query(func.count(Gift.id), Gift.isbn). \
            filter(Gift.launched == False, Gift.isbn.in_(book_isbn_list), Gift.status == 1).group_by(Gift.isbn).all()
        print(count_list)
        return count_list

