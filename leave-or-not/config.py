from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

import os
import requests
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


def add_user_action(actionName: Literal["yes", "no", "cancel"], message: Message):
    filename = f"logs/actions/{message.from_user.id}.json"
    
    if os.path.exists(filename):
        data = json.load(open(filename, "r"))
        data[actionName] += 1
        data["last_updated"] = str(datetime.now())
        data["fullname"] = message.from_user.full_name
    else:
        os.makedirs("logs/actions", exist_ok=True)
        data = {
            "name": message.from_user.username,
            "fullname": message.from_user.full_name,
            "yes": 0,
            "no": 0,
            "cancel": 0,
            "last_updated": str(datetime.now())
        }
        data[actionName] += 1
    
    with open(filename, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    


def create_notify():
    answer = input("Отправить уведомление об обновлении всем пользователям? [Отправить/Нет]\n>>> ")
    if answer != "Отправить": return
    
    users = get_user_ids_for_notification()
    for user in users:
        send_notify(user)

def send_notify(userId: int):
    message = "Бот обновился и готов к работе! Для начала можешь отправить мне /start"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        "chat_id": userId,
        "text": message
    }
    response = requests.post(url, params=params, headers={"Content-Type": "application/json"})

def get_user_ids_for_notification() -> list[int]:
    ids = []
    for file in os.listdir("logs/actions"):
        ids.append(int(file.replace(".json", "")))
    return ids

def get_my_statistics(userId: int) -> str:
    for file in os.listdir("logs/actions"):
        if str(userId) != file.replace(".json", ""): continue
        data = json.load(open(f"logs/actions/{file}", "r"))
        text = "\n".join(("📊 Статистика ответов:", 
                          f"✅ Ответили 'Да' {data['yes']} раз/раза", 
                          f"🚫 Ответили 'Нет' {data['no']} раз/раза", 
                          f"↩️ Ответили 'Назад' {data['cancel']} раз/раза"))
        return text