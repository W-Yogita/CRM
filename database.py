from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Database URL - Creates a file named crm.db in your root directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./crm.db"

# 2. Engine configuration
# 'check_same_thread: False' is required ONLY for SQLite because FastAPI handles requests across multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Session factory to create unique DB sessions for each API request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class that our models (tables) will inherit from
Base = declarative_base()


# 5. Dependency generator to get database session per request and close it automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()