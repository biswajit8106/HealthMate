from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class PushSubscription(Base):
    __tablename__ = 'push_subscriptions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    subscription_info = Column(String, nullable=False)  # JSON string of subscription object

    user = relationship("User", back_populates="push_subscriptions")
