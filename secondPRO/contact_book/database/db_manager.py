from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# آدرس دیتابیس SQLite (فایل contacts.db در کنار پروژه ساخته میشه)
DATABASE_URL = 'sqlite:///contacts.db'

# ساخت موتور ارتباط با دیتابیس
engine = create_engine(DATABASE_URL, echo=True)

# ساخت یک session برای خواندن و نوشتن اطلاعات
Session = sessionmaker(bind=engine)
session = Session()

# ساخت جدول‌ها در دیتابیس
def init_db():
    Base.metadata.create_all(engine)
