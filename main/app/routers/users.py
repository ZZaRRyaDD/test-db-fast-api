import time

from database import User, UserAction, UserCreate, engine
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from services import sql_query

router = APIRouter(prefix="/users", tags=["users"])

SUCCESS_CREATED_CODE = 201
OK_CODE = 200


@router.get("/{id}/")
def read_user(id: int) -> User:
    """View-controller for return user with current id."""
    query = UserAction.get_user(id)
    start_time = time.time()
    user = engine.execute(query)
    end_time = time.time() - start_time
    return {
        "response": user.mappings().first(),
        "query": sql_query(query),
        "clean_query": sql_query(query, literal_binds=False),
        "time": end_time,
    }


@router.get("/")
def read_users() -> User:
    """View-controller for return all users."""
    query = UserAction.get_users()
    start_time = time.time()
    users = engine.execute(query)
    end_time = time.time() - start_time
    return {
        "response": users.mappings().all(),
        "query": sql_query(query),
        "clean_query": sql_query(query, literal_binds=False),
        "time": end_time,
    }


@router.post("/")
def create_users(user: UserCreate) -> JSONResponse:
    """View-controller for create user."""
    query = UserAction.create_user(user)
    start_time = time.time()
    engine.execute(query)
    end_time = time.time() - start_time
    return JSONResponse(
        status_code=SUCCESS_CREATED_CODE,
        content={
            "response": jsonable_encoder(
                engine.execute(UserAction.get_last_user()).mappings().first()
            ),
            "query": sql_query(query),
            "clean_query": sql_query(query, literal_binds=False),
            "time": end_time,
        },
    )


@router.put("/{id}/")
def update_users(id: int, user: UserCreate) -> JSONResponse:
    """View-controller for update user with current id."""
    query = UserAction.update_user(user, id)
    start_time = time.time()
    engine.execute(query)
    end_time = time.time() - start_time
    return JSONResponse(
        status_code=OK_CODE,
        content={
            "response": jsonable_encoder(
                engine.execute(UserAction.get_user(id)).mappings().first()
            ),
            "query": sql_query(query),
            "clean_query": sql_query(query, literal_binds=False),
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
            "response": "User deleted",
            "query": sql_query(query),
            "clean_query": sql_query(query, literal_binds=False),
            "time": end_time,
        },
    )
