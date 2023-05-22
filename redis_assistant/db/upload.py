import db
import logging


def delete_duplicates_skills_in_mysql(duplicates: list[str]):
    connection = db.connect_to_mysql()
    cursor = connection.cursor()
    try:
        query = f"""DELETE FROM demand WHERE name in ({','.join(("'"+skill+"'" for skill in duplicates))})"""
        cursor.execute(query)
    except BaseException as err:
        logging.fatal(f"Произошла ошибка при удалении: {err}")
    else:
        connection.commit()
        logging.info(f"Успешно освободили таблицу mysql.demand от {len(duplicates)} повторений")
    finally:
        connection.close()

def save_all_skills_to_postgres(wordList: list[str], tableName: str) -> bool:
    connection = db.connect_to_postgres()
    cursor = connection.cursor()
    try:
        for index in range(0, len(wordList), 1000):
            query = f"INSERT INTO {tableName}(name) VALUES {create_insert_query(wordList[index:index+1000])} ON CONFLICT (name) DO NOTHING;"
            cursor.execute(query)
    except BaseException as err:
        logging.fatal(f"Произошла ошибка при сохранении стоп-слов: {err}")
        connection.close()
    else:
        connection.commit()
        logging.info(f"Успешно сохранили в таблицу postgres.{tableName} {len(wordList)} навыков")
    finally:
        connection.close()

def create_insert_query(values: list[str]) -> str:
    query = ",".join((f"""('{i.replace("'", '`')}')""" for i in values))
    return query
