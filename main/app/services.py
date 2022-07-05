from database import engine


def sql_query(query, literal_binds=True) -> str:
    """Return sql query."""
    return query.compile(
        engine,
        compile_kwargs={"literal_binds": literal_binds},
    ).string
