from .database import SessionLocal


def get_db() -> SessionLocal:
    """Return connect db."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
