from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    user = relationship("User", backref="favorites")
    item = relationship("Item", backref="favorited_by")

    __table_args__ = (UniqueConstraint("user_id", "item_id", name="unique_user_item"),)
