import pymysql
from pymysql.connections import Connection

from config import Skill, MYSQL


def connect_to_db() -> Connection:
    try:
        connection = pymysql.connect(
                host=MYSQL.HOST.value,
                port=MYSQL.PORT.value,
                database=MYSQL.DB.value,
                user=MYSQL.USER.value,
                password=MYSQL.PASSWORD.value,
            )
        return connection

    except Exception as ex:
        exit(f"Error by connection: {ex}")


def get_skill_from_database() -> Skill:
    """Возвращает самую первую пару навыков, у которой значение is_duplicate является None. 
    Таким образом, мы понимаем, что с этой парой еще не работали"""
    
    connection = connect_to_db()
    with connection.cursor() as cursor:
        query_get_null_couple = f"SELECT id, name, is_displayed FROM {MYSQL.TABLE.value}  WHERE is_displayed IS NULL LIMIT 1"

        cursor.execute(query_get_null_couple)
        skill = cursor.fetchone()
        connection.close()
        if skill:return Skill(*skill)
        else:return

def confirm_skill(id: int, confirm: bool = True) -> None:
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            if confirm:
                cursor.execute(f"UPDATE {MYSQL.TABLE.value} SET is_displayed=1 WHERE id={id}")
            else:
                cursor.execute(f"UPDATE {MYSQL.TABLE.value} SET is_displayed=0 WHERE id={id}")

            connection.commit()
    finally:
        connection.close()


def refute_skill(id: int) -> None: # Опровергнуть сходство
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE {MYSQL.TABLE.value} SET is_displayed=null WHERE id={id}")
            connection.commit()

    finally:
        connection.close()

def get_previos_skill(current_id: int) -> Skill | None:
    connection = connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT id, name, is_displayed FROM {MYSQL.TABLE.value} WHERE id = {current_id-1}""")
        skill = cursor.fetchone()

        try:res = Skill(*skill)
        except: res = None 

        if res is None: return
        refute_skill(id=res.iD) # Делаем это для того, чтобы мы могли несколько раз подряд нажимать кнопку назад 
        connection.close()
        return res

def show_the_rest() -> tuple[int, int]:
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {MYSQL.TABLE.value}")
            count_all_values = cursor.fetchone()

            cursor.execute(f"SELECT COUNT(*) FROM {MYSQL.TABLE.value} WHERE is_displayed IS NULL")
            count_null_values = cursor.fetchone()
            return count_all_values[0], count_null_values[0]
    except BaseException as err:
        exit(err)
    finally:
        connection.close()


