from pydantic import BaseModel


# ---------------- MOBILE SCHEMAS ----------------

class MobileCreate(BaseModel):
    brand: str
    model: str
    ram: str
    storage: str
    price: float


class MobileResponse(MobileCreate):
    id: int

    class Config:
        from_attributes = True


# ---------------- USER SCHEMAS ----------------

class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str
    role: str      # admin / dev / intern


class UserLogin(BaseModel):
    email: str
    hashed_password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True