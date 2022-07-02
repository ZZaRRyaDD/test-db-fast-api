import requests
import factories
import json

USERS_COUNT = 100
PORT_SERVER_MYSQL = 8080
PORT_SERVER_POSTGRESQL = 8000


def generate_results(info: dict) -> None:
    """Calculate times and query to db and build graphics."""
    print(info)


def set_results(
    info: dict,
    db: str,
    response: requests.Response,
    action: str,
) -> None:
    """Take results and set values."""
    response = json.loads(response._content)
    info[db][action]["queries"].append(response["query"])
    info[db][action]["timings"].append(response["time"])


def check_dublicate(users) -> bool:
    """Check users for unique."""
    phones = [user.phone for user in users]
    emails = [user.email for user in users]
    passport_ids = [user.passport_id for user in users]
    passport_seriess = [user.passport_series for user in users]
    return all(
        [
            len(set(phones)) == USERS_COUNT,
            len(set(emails)) == USERS_COUNT,
            len(set(passport_ids)) == USERS_COUNT,
            len(set(passport_seriess)) == USERS_COUNT,
        ]
    )


def generate_data() -> list[factories.UserFactory]:
    """Generate unique users."""
    users = factories.UserFactory.create_batch(USERS_COUNT)
    while not check_dublicate(users):
        users = factories.UserFactory.create_batch(USERS_COUNT)
    return users


def main() -> None:
    """Script for send requests to server."""
    users = generate_data()
    info = {
        "mysql": {
            "port": PORT_SERVER_MYSQL,
            "create_item": {
                "queries": [],
                "timings": [],
                "results": {
                    "query": "",
                    "average_time": 0,
                }
            },
            "get_item": {
                "queries": [],
                "timings": [],
                "results": {
                    "query": "",
                    "average_time": 0,
                }
            },
            "get_items": {
                "queries": [],
                "timings": [],
                "results": {
                    "query": "",
                    "average_time": 0,
                }
            },
            "update_item": {
                "queries": [],
                "timings": [],
                "results": {
                    "query": "",
                    "average_time": 0,
                }
            },
            "delete_item": {
                "queries": [],
                "timings": [],
                "results": {
                    "query": "",
                    "average_time": 0,
                }
            },
        },
        "postgresql": {
            "port": PORT_SERVER_POSTGRESQL,
            "create_item": {
                "queries": [],
                "timings": [],
                "results": {
                    "query": "",
                    "average_time": 0,
                }
            },
            "get_item": {
                "queries": [],
                "timings": [],
                "results": {
                    "query": "",
                    "average_time": 0,
                }
            },
            "get_items": {
                "queries": [],
                "timings": [],
                "results": {
                    "query": "",
                    "average_time": 0,
                }
            },
            "update_item": {
                "queries": [],
                "timings": [],
                "results": {
                    "query": "",
                    "average_time": 0,
                }
            },
            "delete_item": {
                "queries": [],
                "timings": [],
                "results": {
                    "query": "",
                    "average_time": 0,
                }
            },
        }
    }
    for db in info:
        url = f"http://0.0.0.0:{info[db]['port']}/users/"
        for user in users:
            user.passport_id = str(user.passport_id)
            user.passport_series = str(user.passport_series)
            user.phone = str(user.phone)
            response = requests.post(
                url,
                data=json.dumps(user.__dict__),
            )
            set_results(
                info,
                db,
                response,
                "create_item",
            )
        for i in range(USERS_COUNT):
            response = requests.get(
                url + f"{i + 1}/",
            )
            set_results(
                info,
                db,
                response,
                "get_item",
            )
        for i in range(USERS_COUNT):
            response = requests.get(
                url,
            )
            set_results(
                info,
                db,
                response,
                "get_items",
            )
        for i in range(USERS_COUNT):
            new_user = users[i]
            new_user.name += "_new"
            new_user.surname += "_new"
            response = requests.put(
                url + f"{i + 1}/",
                data=json.dumps(new_user.__dict__),
            )
            set_results(
                info,
                db,
                response,
                "update_item",
            )
        for i in range(USERS_COUNT):
            response = requests.delete(
                url + f"{i + 1}/",
            )
            set_results(
                info,
                db,
                response,
                "delete_item",
            )
    generate_results(info)


if __name__ == "__main__":
    main()
