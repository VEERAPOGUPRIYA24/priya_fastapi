from sqlalchemy import Column, Integer, String, Float
from database import Base


# ================= MOBILE TABLE =================

class Mobile(Base):
    __tablename__ = "mobiles"

    id = Column(Integer, primary_key=True, index=True)

    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)

    ram = Column((String(20)), nullable=False)
    storage = Column((String(20)), nullable=False)

    price = Column(Float, nullable=False)



# ================= USER TABLE =================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), nullable=False)

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    # bcrypt hashed password will be stored here
    hashed_password = Column(
        String(255),
        nullable=False
    )

    # admin / dev / intern
    role = Column(
        String(20),
        nullable=False
    )