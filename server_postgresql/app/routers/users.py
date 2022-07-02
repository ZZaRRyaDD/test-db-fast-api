import time
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.database import get_db, User, UserCreate, UserAction, engine
from app.services import sql_query

router = APIRouter(prefix="/users", tags=["users"])

SUCCESS_CREATED_CODE = 201
OK_CODE = 200


@router.get("/{id}/")
def read_user(id: int, db: Session = Depends(get_db)) -> User:
    """View-controller for return user with current id."""
    start_time = time.time()
    user = UserAction.get_user(db, id)
    end_time = time.time() - start_time
    if user:
        return {
            "response": user.first(),
            "query": sql_query(user),
            "time": end_time,
        }
    raise HTTPException(
        status_code=404,
        detail="User with this id don't exists",
    )


@router.get("/")
def read_users(db: Session = Depends(get_db)) -> User:
    """View-controller for return all users."""
    start_time = time.time()
    users = UserAction.get_users(db)
    end_time = time.time() - start_time
    if users.count():
        return {
            "response": users.all(),
            "query": sql_query(users),
            "time": end_time,
        }
    raise HTTPException(
        status_code=404,
        detail="Users don't exist",
    )

@router.post("/")
def create_users(
    user: UserCreate,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """View-controller for create user."""
    query = UserAction.create_user(user)
    start_time = time.time()
    engine.execute(query)
    end_time = time.time() - start_time
    return JSONResponse(
        status_code=SUCCESS_CREATED_CODE,
        content={
            "reponse": jsonable_encoder(UserAction.get_last_user(db)),
            "query": sql_query(query),
            "time": end_time,
        },
    )


@router.put("/{id}/")
def update_users(
    id: int,
    user: UserCreate,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """View-controller for update user with current id."""
    query = UserAction.update_user(user, id)
    start_time = time.time()
    engine.execute(query)
    end_time = time.time() - start_time
    return JSONResponse(
        status_code=OK_CODE,
        content={
            "reponse": jsonable_encoder(UserAction.get_user(db, id).first()),
            "query": sql_query(query),
            "time": end_time,
        },
    )


@router.delete("/{id}/")
def delete_users(id: int) -> JSONResponse:
    """View-controller for delete user with current id."""
    query = UserAction.delete_user(id)
    start_time = time.time()
    engine.execute(query)
    end_time = time.time() - start_time
    return JSONResponse(
        status_code=OK_CODE,
        content={
            "detail": "User deleted",
            "query": sql_query(query),
            "time": end_time,
        },
    )
