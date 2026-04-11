# backend/models.py (Expense part)
from sqlalchemy import Column, Integer, String, Float, Date
from backend.database import Base

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)