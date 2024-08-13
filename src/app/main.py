from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud, auth, database
from app.database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login/")
def login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = auth.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/password-reset/", response_model=schemas.PasswordResetResponse)
def reset_password(token: str, new_password: str, db: Session = Depends(database.get_db)):
    email = auth.verify_reset_token(token)
    if email is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = auth.pwd_context.hash(new_password)
    user.hashed_password = hashed_password
    db.commit()
    return {"msg": "Password has been reset successfully"}

@app.post("/create-magazines/", response_model=schemas.MagazineBase)
def create_magazine(magazine: schemas.MagazineBase, db: Session = Depends(database.get_db)):
    # Create the magazine
    return crud.create_magazine(db, magazine)

@app.post("/create-subcriptionplan/", response_model=schemas.SubscriptionPlanBase)
def create_subcriptionplan(subcriptionplan: schemas.SubscriptionPlanBase, db: Session = Depends(database.get_db)):
    # Create the magazine
    return crud.create_subcriptionplan(db, subcriptionplan)

@app.get("/magazines/", response_model=List[schemas.Magazine])
def list_magazines(db: Session = Depends(database.get_db)):
    return crud.get_magazines(db=db)

@app.get("/magazines/{magazine_id}/plans/", response_model=List[schemas.SubscriptionPlan])
def list_plans(magazine_id: int, db: Session = Depends(database.get_db)):
    return crud.get_plans_for_magazine(db=db, magazine_id=magazine_id)

@app.post("/subscriptions/", response_model=schemas.Subscription)
def create_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.create_subscription(db=db, subscription=subscription, user_id=current_user.id)

@app.get("/subscriptions/", response_model=List[schemas.Subscription])
def list_subscriptions(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.get_subscriptions(db=db, user_id=current_user.id)
