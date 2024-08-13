from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    subscriptions = relationship("Subscription", back_populates="owner")

class Magazine(Base):
    __tablename__ = "magazines"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id = Column(Integer, primary_key=True, index=True)
    magazine_id = Column(Integer, ForeignKey("magazines.id"))
    duration_months = Column(Integer)
    price = Column(Integer)
    discount_percentage = Column(Integer, default=0)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"))
    
    owner = relationship("User", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan")
