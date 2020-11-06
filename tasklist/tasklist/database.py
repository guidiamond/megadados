# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import json
import uuid

from functools import lru_cache

import mysql.connector as conn

from fastapi import Depends

from utils.utils import get_config_filename, get_app_secrets_filename
from utils.is_uuid import is_valid_uuid

from .models import Task, User


class DBSession:
    def __init__(self, connection: conn.MySQLConnection):
        self.connection = connection

    ## User Queries
    def create_new_user(self, name: str):
        user_id = uuid.uuid4()

        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users VALUES (UUID_TO_BIN(%s), %s)",
                (str(user_id), name),
            )
        self.connection.commit()

        return user_id

    def remove_user(self, uuid_: str):
        if not self.__user_exists(uuid_):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM users WHERE owner_id=UUID_TO_BIN(%s)",
                (str(uuid_),),
            )
        self.connection.commit()

    def read_user_tasks(self, owner_id: str, completed: bool = None):
        if not self.__user_exists(owner_id):
            raise KeyError()
        query = "SELECT BIN_TO_UUID(uuid), description, completed FROM tasks WHERE owner_id=UUID_TO_BIN(%s)"
        if completed is not None:
            query += " AND completed = "
            if completed:
                query += "True"
            else:
                query += "False"

        with self.connection.cursor() as cursor:
            cursor.execute(query, (str(owner_id),))
            db_results = cursor.fetchall()
        return {
            uuid_: Task(
                owner=str(owner_id),
                description=field_description,
                completed=bool(field_completed),
            )
            for uuid_, field_description, field_completed in db_results
        }

    def get_user_info(self, user_id: str):
        if not self.__user_exists(user_id):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT name
                FROM users
                WHERE owner_id = UUID_TO_BIN(%s)
                """,
                (str(user_id),),
            )
            result = cursor.fetchone()
        return User(name=result[0])

    def update_user_info(self, user_id: str, name: str):
        if not self.__user_exists(user_id):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET name = %s
                WHERE owner_id = UUID_TO_BIN(%s)
                """,
                (
                    name,
                    str(user_id),
                ),
            )
        self.connection.commit()

    ## Task Queries
    def read_tasks(self, completed: bool = None):
        query = "SELECT BIN_TO_UUID(uuid), description,BIN_TO_UUID(owner_id), completed FROM tasks"
        if completed is not None:
            query += " WHERE completed = "
            if completed:
                query += "True"
            else:
                query += "False"

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            db_results = cursor.fetchall()

        return {
            uuid_: Task(
                owner=owner_id,
                description=field_description,
                completed=bool(field_completed),
            )
            for uuid_, field_description, owner_id, field_completed in db_results
        }

    def create_task(self, item: Task):
        if not self.__user_exists(item.owner):
            raise KeyError()

        uuid_ = uuid.uuid4()
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tasks VALUES (UUID_TO_BIN(%s), UUID_TO_BIN(%s), %s, %s)",
                (str(uuid_), str(item.owner), item.description, item.completed),
            )
        self.connection.commit()

        return uuid_

    def read_task(self, uuid_: uuid.UUID):
        if not self.__task_exists(uuid_):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT description, completed, BIN_TO_UUID(owner_id)
                FROM tasks
                WHERE uuid = UUID_TO_BIN(%s)
                """,
                (str(uuid_),),
            )
            result = cursor.fetchone()

        return Task(description=result[0], completed=bool(result[1]), owner=result[2])

    def replace_task(self, uuid_, item):
        if not self.__task_exists(uuid_):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks SET description=%s, completed=%s, owner_id=UUID_TO_BIN(%s)
                WHERE uuid=UUID_TO_BIN(%s)
                """,
                (item.description, item.completed, str(item.owner), str(uuid_)),
            )
        self.connection.commit()

    def remove_task(self, uuid_):
        if not self.__task_exists(uuid_):
            raise KeyError()

        with self.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM tasks WHERE uuid=UUID_TO_BIN(%s)",
                (str(uuid_),),
            )
        self.connection.commit()

    def remove_all_tasks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM tasks")
        self.connection.commit()

    def __user_exists(self, uuid_: uuid.UUID):
        if not is_valid_uuid(uuid_):
            raise KeyError()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT EXISTS(
                    SELECT 1 FROM users WHERE owner_id=UUID_TO_BIN(%s)
                )
                """,
                (str(uuid_),),
            )
            results = cursor.fetchone()
            found = bool(results[0])

        return found

    def __task_exists(self, uuid_: uuid.UUID):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT EXISTS(
                    SELECT 1 FROM tasks WHERE uuid=UUID_TO_BIN(%s)
                )
                """,
                (str(uuid_),),
            )
            results = cursor.fetchone()
            found = bool(results[0])

        return found


@lru_cache
def get_credentials(
    config_file_name: str = Depends(get_config_filename),
    secrets_file_name: str = Depends(get_app_secrets_filename),
):
    with open(config_file_name, "r") as file:
        config = json.load(file)
    with open(secrets_file_name, "r") as file:
        secrets = json.load(file)
    return {
        "user": secrets["user"],
        "password": secrets["password"],
        "host": config["db_host"],
        "database": config["database"],
    }


def get_db(credentials: dict = Depends(get_credentials)):
    try:
        connection = conn.connect(**credentials)
        yield DBSession(connection)
    finally:
        connection.close()
