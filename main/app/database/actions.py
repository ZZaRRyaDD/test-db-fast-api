from sqlalchemy import delete, desc, insert, orm, sql, update

from . import models, schemas


class UserAction:
    """Class with actions with user."""

    @staticmethod
    def get_user(db: orm.Session, id: int) -> orm.Query:
        """Get query of user with current id."""
        return db.query(models.User).filter(models.User.id == id)

    @staticmethod
    def get_last_user(db: orm.Session) -> models.User:
        """Get last created user."""
        return db.query(models.User).order_by(desc(models.User.id)).first()

    @staticmethod
    def get_users(db: orm.Session) -> orm.Query:
        """Get query of all users."""
        return db.query(models.User)

    @staticmethod
    def create_user(user: schemas.UserCreate) -> sql.dml.Insert:
        """Generate query for create user."""
        return insert(models.User).values(**user.dict())

    @staticmethod
    def update_user(user: schemas.UserCreate, id: int) -> sql.dml.Update:
        """Generate query for update user."""
        return update(models.User).where(
            models.User.id == id,
        ).values(**user.dict())

    @staticmethod
    def delete_user(id: int) -> sql.dml.Delete:
        """Generate query for delete user."""
        return delete(models.User).where(models.User.id == id)
