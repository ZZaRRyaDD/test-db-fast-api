import json
import random

import factories
import matplotlib.pyplot as plt
import numpy as np
import requests

USERS_COUNT = 100
DOMAIN_SERVER_MYSQL = "web_1:8080"
DOMAIN_SERVER_POSTGRESQL = "web_2:8000"


def generate_results(info: dict) -> None:
    """Calculate times and query to db and build graphics."""
    for db in info:
        print(f"Database: {db}")
        for key, value in info[db].items():
            timings = np.array(value["timings"])
            value["results"]["average_time"] = timings.mean()
            value["results"]["dispersion"] = np.var(timings)
            value["results"]["query"] = value["clean_queries"]
            value["results"]["example_query"] = value["queries"][
                random.randint(0, len(value["queries"]) - 1)
            ]
            print(f"{key}:")
            print(
                f"\tAverage time: {value['results']['average_time']:.8f} sec."
            )
            print(f"\tDispersion: {value['results']['dispersion']:.8f} sec.")
            print(f"\tTemplate query: {value['results']['query']}")
            print(f"\tExample query: {value['results']['example_query']}")
        print()
    postgresql = dict(
        [(key, value["results"]) for key, value in info["postgresql"].items()]
    )
    mysql = dict(
        [(key, value["results"]) for key, value in info["mysql"].items()]
    )
    for choise in ["average_time", "dispersion"]:
        postgresql_time = [value[choise] for _, value in postgresql.items()]
        mysql_time = [value[choise] for _, value in mysql.items()]
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        count_bars = np.arange(5)
        width = 0.5
        ax.bar(count_bars + 0.00, postgresql_time, width, color="r")
        ax.bar(count_bars + 0.25, mysql_time, width, color="b")
        title_choise = " ".join(choise.split("_"))
        title_graphic = (
            "Comparison speed of CRUD actions with MySQL and PostgreSQL by {}"
        )
        ax.set_ylabel("Time (sec)")
        ax.set_title(
            title_graphic.format(title_choise)
        )
        labels = [key for key, _ in postgresql.items()]
        ax.set_xticks(ticks=range(len(labels)), labels=labels)
        ax.legend(labels=["PostgreSQL", "MySQL"], loc="upper center")
        plt.savefig(f"results/results_{choise}.png", bbox_inches="tight")


def set_results(
    info: dict,
    db: str,
    response: requests.Response,
    action: str,
) -> None:
    """Take results and set values."""
    response = json.loads(response._content)
    info[db][action]["queries"].append(response["query"])
    info[db][action]["clean_queries"] = response["clean_query"]
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
            "create_item": {
                "queries": [],
                "clean_queries": "",
                "timings": [],
                "results": {
                    "query": "",
                    "example_query": "",
                    "average_time": 0,
                    "dispersion": 0,
                },
            },
            "get_item": {
                "queries": [],
                "clean_queries": "",
                "timings": [],
                "results": {
                    "query": "",
                    "example_query": "",
                    "average_time": 0,
                    "dispersion": 0,
                },
            },
            "get_items": {
                "queries": [],
                "clean_queries": "",
                "timings": [],
                "results": {
                    "query": "",
                    "example_query": "",
                    "average_time": 0,
                    "dispersion": 0,
                },
            },
            "update_item": {
                "queries": [],
                "clean_queries": "",
                "timings": [],
                "results": {
                    "query": "",
                    "example_query": "",
                    "average_time": 0,
                    "dispersion": 0,
                },
            },
            "delete_item": {
                "queries": [],
                "clean_queries": "",
                "timings": [],
                "results": {
                    "query": "",
                    "example_query": "",
                    "average_time": 0,
                    "dispersion": 0,
                },
            },
        },
        "postgresql": {
            "create_item": {
                "queries": [],
                "clean_queries": "",
                "timings": [],
                "results": {
                    "query": "",
                    "example_query": "",
                    "average_time": 0,
                    "dispersion": 0,
                },
            },
            "get_item": {
                "queries": [],
                "clean_queries": "",
                "timings": [],
                "results": {
                    "query": "",
                    "example_query": "",
                    "average_time": 0,
                    "dispersion": 0,
                },
            },
            "get_items": {
                "queries": [],
                "clean_queries": "",
                "timings": [],
                "results": {
                    "query": "",
                    "example_query": "",
                    "average_time": 0,
                    "dispersion": 0,
                },
            },
            "update_item": {
                "queries": [],
                "clean_queries": "",
                "timings": [],
                "results": {
                    "query": "",
                    "example_query": "",
                    "average_time": 0,
                    "dispersion": 0,
                },
            },
            "delete_item": {
                "queries": [],
                "clean_queries": "",
                "timings": [],
                "results": {
                    "query": "",
                    "example_query": "",
                    "average_time": 0,
                    "dispersion": 0,
                },
            },
        },
    }
    for db in info:
        domain = (
            DOMAIN_SERVER_MYSQL
            if db == 'mysql'
            else DOMAIN_SERVER_POSTGRESQL
        )
        url = f"http://{domain}/users/"
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
