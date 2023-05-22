from typing import Literal
from redis import Redis
import time

from rich.progress import track
from fuzzywuzzy import fuzz
import db
import logging

logging.basicConfig(filemode="w", filename="info.log", format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s", level=logging.DEBUG, datefmt="%H:%M:%S")

TABLENAME_CORRECT_SKILLS = 'correct_skill'
TABLENAME_UNCORRECT_SKILLS = 'minus_skill'

def main():
    logging.info("Запуск программы...")
    while True:
        check_skills(TABLENAME_CORRECT_SKILLS)
        check_skills(TABLENAME_UNCORRECT_SKILLS)
        
        logging.info("Все множества redis обработаны\nЗасыпаем на 60 сек...")
        time.sleep(1)


def check_skills(type_skills: Literal["minus_skill", "correct_skill"]):
    red = Redis("127.0.0.1", 6379)
    skills = [skill.decode("utf-8") for skill in red.smembers(type_skills)]
    logging.info(f"Проверяем навыки '{type_skills}' в количестве {len(skills)}")
    for skill in skills:
        duplicates = find_duplicates(skill)
        if duplicates:
            db.save_all_skills_to_postgres(duplicates, type_skills)
            db.delete_duplicates_skills_in_mysql(duplicates)
        red.srem(type_skills, skill)
        logging.info(f"Удалили навык {skill} из множества {type_skills}")

def find_duplicates(skill: str) -> list[str]:
    duplicates: list[str] = []
    skills = db.get_none_checked_skills()

    for item in track(range(len(skills))):
        similarity = fuzz.WRatio(skill, skills[item])
        if similarity > 90:
            duplicates.append(skills[item])
    
    logging.info(f"Для навыка '{skill} найдено {len(duplicates)} повторений: {[i for i in duplicates]}'")
    return duplicates


if __name__ == "__main__":
    main()