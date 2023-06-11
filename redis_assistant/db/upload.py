import db
import logging


def delete_duplicates_skills_in_mysql(parent_skill: str, duplicates: list[str]):
    connection = db.connect_to_mysql()
    cursor = connection.cursor()
    try:
        query_parent_id = f"SELECT id FROM demand WHERE name = '{parent_skill}' LIMIT 1;"
        cursor.execute(query_parent_id)
        parent_id = cursor.fetchone()[0]
        cursor.execute(f"""DELETE FROM demand WHERE name in ({','.join(("'"+skill+"'" for skill in duplicates))}) AND id != {parent_id}""")
    except BaseException as err:
        logging.fatal(f"Error during deletion: {err}")
    else:
        connection.commit()
        logging.info(f"Successufull cleaning mysql.demand from {len(duplicates)} duplicates")
    finally:
        connection.close()

def s():
    connection = db.connect_to_mysql()
    cursor = connection.cursor()
    query_parent_id = f"SELECT id FROM demand WHERE name ='Гра' LIMIT 1;"
    cursor.execute(query_parent_id)
    parent_id = cursor.fetchone()[0]
    print(parent_id)
    connection.close()

def save_all_skills_to_postgres(wordList: list[str], tableName: str) -> bool:
    connection = db.connect_to_postgres()
    cursor = connection.cursor()
    try:
        for index in range(0, len(wordList), 1000):
            query = f"INSERT INTO {tableName}(name) VALUES {create_insert_query(wordList[index:index+1000])} ON CONFLICT (name) DO NOTHING;"
            cursor.execute(query)
    except BaseException as err:
        logging.fatal(f"Error during saving skills: {err}")
        connection.close()
    else:
        connection.commit()
        logging.info(f"Successufull saving in table postgres.{tableName} {len(wordList)} skills")
    finally:
        connection.close()

def create_insert_query(values: list[str]) -> str:
    query = ",".join((f"""('{i.replace("'", '`')}')""" for i in values))
    return query
