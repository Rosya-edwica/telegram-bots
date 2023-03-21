from aiogram.dispatcher.filters.state import State, StatesGroup

import os
from typing import NamedTuple
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN_LEAVE_OR_NOT")
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
