from flask_login import current_user

from app.libs.email import send_email
from app.libs.enums import PendingStatus
from sqlalchemy import Column, String, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from app.view_models.book import BookViewModel


class Drift(Base):
    """
        一次具体的交易信息
    """
    __tablename__ = 'drift'

    def __init__(self):
        self.pending = PendingStatus.waiting
        super(Drift, self).__init__()

    id = Column(Integer, primary_key=True)
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))
    _pending = Column('pending', SmallInteger, default=1)
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')

    @classmethod
    def save_a_drift(cls, drift_form, current_gift):
        with db.auto_commit():
            book = BookViewModel(current_gift.book.first)

            drift = Drift()
            drift_form.populate_obj(drift)
            drift.gift_id = current_gift.id
            drift.requester_id = current_user.id
            drift.requester_nickname = current_user.nickname
            drift.gifter_nickname = current_gift.user.nickname
            drift.gifter_id = current_gift.user.id
            drift.book_title = book.title
            drift.book_author = book.author
            drift.book_img = book.image
            drift.isbn = book.isbn
            # 当请求生成时，不需要让这个礼物处于锁定状态
            # 这样赠送者是可以收到多个索取请求的，由赠送者选择送给谁
            # current_gift.launched = True
            # 请求者鱼豆-1
            current_user.beans -= 1
            # 但是赠送者鱼豆不会立刻+1
            # current_gift.user.beans += 1
            db.session.add(drift)
        send_email(current_gift.user.email, '有人想要一本书', 'email/get_gift',
                   wisher=current_user,
                   gift=current_gift)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value
