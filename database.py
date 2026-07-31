from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/mobiles_db"
DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_-VkdD3d926_ZR6fzHhF@priya24-veerapogupriya-51fe.h.aivencloud.com:12834/defaultdb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
