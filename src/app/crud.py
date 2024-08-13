from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_magazine(db: Session, magazine: schemas.MagazineBase):
    db_magazine = models.Magazine(
        title=magazine.title,
        description=magazine.description,
    )
    db.add(db_magazine)
    db.commit()
    db.refresh(db_magazine)
    return db_magazine

def create_subcriptionplan(db: Session, subcriptionplan: schemas.SubscriptionPlanBase):
    db_subcriptionplan = models.SubscriptionPlan(
        magazine_id=subcriptionplan.magazine_id,
        duration_months=subcriptionplan.duration_months,
        price=subcriptionplan.price,
        discount_percentage=subcriptionplan.discount_percentage
    )
    db.add(db_subcriptionplan)
    db.commit()
    db.refresh(db_subcriptionplan)
    return db_subcriptionplan

def get_magazines(db: Session):
    return db.query(models.Magazine).all()

def get_plans_for_magazine(db: Session, magazine_id: int):
    return db.query(models.SubscriptionPlan).filter(models.SubscriptionPlan.magazine_id == magazine_id).all()

def create_subscription(db: Session, subscription: schemas.SubscriptionCreate, user_id: int):
    db_subscription = models.Subscription(**subscription.dict(), user_id=user_id)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def get_subscriptions(db: Session, user_id: int):
    return db.query(models.Subscription).filter(models.Subscription.user_id == user_id).all()
