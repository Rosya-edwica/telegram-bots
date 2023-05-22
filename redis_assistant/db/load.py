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
        logging.fatal(f"Error during getting skills from demand table: {err}")
    finally:
        connection.close()
        return skills
    

def get_skills(skill_type: str) -> list[str]:
    if skill_type == "minus_skill":
        is_displayed = 0
    else: 
        is_displayed = 1
        
    skills: list[str] = []
    connection = db.connect_to_mysql()
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT name FROM demand WHERE is_displayed = {is_displayed}")
        skills = [skill[0] for skill in cursor.fetchall()]
    except BaseException as err:
        logging.fatal(f"Error during getting skills from demand table: {err}")
    finally:
        connection.close()
        return skills