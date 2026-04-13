# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# engine = create_engine("sqlite:///./expenses.db", connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(bind=engine)
# Base = declarative_base()

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    month TEXT NOT NULL,
    limit_amount REAL NOT NULL,
    spent REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    data TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);