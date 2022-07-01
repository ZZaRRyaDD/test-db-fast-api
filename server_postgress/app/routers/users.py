from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db, User, UserCreate, UserAction, engine
from app.services import sql_query

router = APIRouter(prefix="/users", tags=["users"])

SUCCESS_CREATED_CODE = 201
OK_CODE = 200


@router.get("/{id}/")
def read_user(id: int, db: Session = Depends(get_db)) -> User:
    """View-controller for return user with current id."""
    user = UserAction.get_user(db, id)
    if user:
        return {
            "response": user.first(),
            "query": sql_query(user),
        }
    raise HTTPException(
        status_code=404,
        detail="User with this id don't exists",
    )


@router.get("/")
def read_users(db: Session = Depends(get_db)) -> User:
    """View-controller for return all users."""
    users = UserAction.get_users(db)
    if users:
        return {
            "response": users.all(),
            "query": sql_query(users),
        }
    raise HTTPException(
        status_code=404,
        detail="Users don't exist",
    )

@router.post("/")
def create_users(user: UserCreate) -> JSONResponse:
    """View-controller for create user."""
    query = UserAction.create_user(user)
    engine.execute(query)
    return JSONResponse(
        status_code=SUCCESS_CREATED_CODE,
        content={
            "reponse": "User created",
            "query": sql_query(query),
        },
    )
    

@router.put("/{id}/")
def update_users(id: int, user: UserCreate) -> JSONResponse:
    """View-controller for update user with current id."""
    query = UserAction.update_user(user, id)
    engine.execute(query)
    return JSONResponse(
        status_code=OK_CODE,
        content={
            "response": "User updated",
            "query": sql_query(query),
        },
    )


@router.delete("/{id}/")
def delete_users(id: int) -> JSONResponse:
    """View-controller for delete user with current id."""
    query = UserAction.delete_user(id)
    engine.execute(query)
    return JSONResponse(
        status_code=OK_CODE,
        content={
            "detail": "User deleted",
            "query": sql_query(query),
        },
    )
