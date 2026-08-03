from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi import Response
import crud
import schemas
import auth

from database import Base, engine, SessionLocal

# Create Tables
Base.metadata.create_all(bind=engine)
print("******** MY MAIN.PY IS RUNNING ********")

app = FastAPI(title="Mobile Management System")


# ================= DATABASE =================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= HOME =================

@app.get("/")
def home():
    return {"message": "Welcome to Mobile Management System"}


@app.get("/test")
def test():
    return {"message": "FastAPI Working Successfully"}


# ================= USER APIs =================

# Register
@app.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(user, db)


# Login
@app.post("/login")
def login(
    response: Response,
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    return crud.validate_user(user, db, response)


# ================= MOBILE APIs =================

# Get All Mobiles
# Admin + Dev + Intern
@app.get("/mobiles", response_model=list[schemas.MobileResponse])
def get_all_mobiles(
    db: Session = Depends(get_db),
    user=Depends(auth.authenticated_user)
):
    return crud.get_mobiles(db)


# Get Mobile By Id
# Admin + Dev + Intern
@app.get("/mobiles/{mobile_id}", response_model=schemas.MobileResponse)
def get_mobile(
    mobile_id: int,
    db: Session = Depends(get_db),
    user=Depends(auth.authenticated_user)
):

    mobile = crud.get_mobile(db, mobile_id)

    if not mobile:
        raise HTTPException(
            status_code=404,
            detail="Mobile not found"
        )

    return mobile


# Create Mobile
# Admin + Dev
@app.post("/mobiles", response_model=schemas.MobileResponse)
def create_mobile(
    mobile: schemas.MobileCreate,
    db: Session = Depends(get_db),
    user=Depends(auth.authenticated_user)
):

    if user["role"] not in ["admin", "dev"]:
        raise HTTPException(
            status_code=403,
            detail="Only Admin or Developer can create mobiles"
        )

    return crud.create_mobile(db, mobile)


# Update Mobile
# Admin + Dev
@app.put("/mobiles/{mobile_id}", response_model=schemas.MobileResponse)
def update_mobile(
    mobile_id: int,
    mobile: schemas.MobileCreate,
    db: Session = Depends(get_db),
    user=Depends(auth.authenticated_user)
):

    if user["role"] not in ["admin", "dev"]:
        raise HTTPException(
            status_code=403,
            detail="Only Admin or Developer can update mobiles"
        )

    updated = crud.update_mobile(db, mobile_id, mobile)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Mobile not found"
        )

    return updated


# Delete Mobile
# Admin Only
@app.delete("/mobiles/{mobile_id}")
def delete_mobile(
    mobile_id: int,
    db: Session = Depends(get_db),
    user=Depends(auth.authenticated_user)
):

    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can delete mobiles"
        )

    deleted = crud.delete_mobile(db, mobile_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Mobile not found"
        )

    return {
        "message": "Mobile deleted successfully"
    }
# ADD THESE LINES AT THE END OF THE FILE
print("Available Routes:")
for route in app.routes:
    print(route.path, route.methods)