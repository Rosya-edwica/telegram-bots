import db
import logging

def get_none_checked_skills() -> list[str]:
    skills: list[str] = []
    connection = db.connect_to_mysql()
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT name FROM demand WHERE is_displayed is NULL")
        skills = [skill[0] for skill in cursor.fetchall()]
    except BaseException as err:
        logging.fatal(f"Ошибка при получении навыков: {err}")
    finally:
        connection.close()
        return skills
