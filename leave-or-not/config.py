from aiogram.dispatcher.filters.state import State, StatesGroup

import os
from typing import NamedTuple
from enum import Enum


TOKEN = os.getenv("TOKEN_SKILLS_LIKE_PROFESSIONS")
HOST = os.getenv("EDWICA_DB_HOST")
USER = os.getenv("EDWICA_DB_USER")
PASS = os.getenv("EDWICA_DB_PASS")

class MYSQL(Enum):
    HOST = HOST
    USER = USER
    PASSWORD = PASS
    PORT = 3306
    DB = "edwica"
    TABLE = "demand"

class Skill(NamedTuple):
    iD: int
    title: str
    is_dislayed: bool | None


class States(StatesGroup):
    start_question = State()
    question = State()