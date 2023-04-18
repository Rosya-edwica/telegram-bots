from aiogram.dispatcher.filters.state import State, StatesGroup

import os
import json
from datetime import datetime
from typing import NamedTuple,Literal
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


def add_user_action(actionName: Literal["yes", "no", "cancel"], userId: int, userName: str):
    filename = f"logs/actions/{userId}.json"
    
    if os.path.exists(filename):
        data = json.load(open(filename, "r"))
        data[actionName] += 1
        data["last_updated"] = str(datetime.now())
    else:
        os.makedirs("logs/actions", exist_ok=True)
        data = {
            "name": userName,
            "yes": 0,
            "no": 0,
            "cancel": 0,
            "last_updated": str(datetime.now())
        }
        data[actionName] += 1
    
    with open(filename, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)