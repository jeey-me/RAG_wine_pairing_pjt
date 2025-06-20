from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite DB 연결
DATABASE_URL = "sqlite:///./wine_recommend.db"  # 로컬 파일로 DB 저장됨
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 테이블 정의
class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(500))
    dish_flavor = Column(Text)
    recommended_wine = Column(String(255))
    reason = Column(Text)

# 테이블 생성
Base.metadata.create_all(bind=engine)