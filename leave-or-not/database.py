import pymysql
from pymysql.connections import Connection
import aiomysql

from config import Skill, MYSQL


async def connect_to_db() -> Connection:
    try:
        connection = await aiomysql.connect(
                host=MYSQL.HOST.value,
                port=MYSQL.PORT.value,
                db=MYSQL.DB.value,
                user=MYSQL.USER.value,
                password=MYSQL.PASSWORD.value,
            )
        return connection

    except Exception as ex:
        exit(f"Error by connection: {ex}")


async def get_skill_from_database() -> Skill:
    """Возвращает самую первую пару навыков, у которой значение is_duplicate является None. 
    Таким образом, мы понимаем, что с этой парой еще не работали"""
    
    connection = await connect_to_db()
    async with connection.cursor() as cursor:
        query_get_null_couple = f"SELECT id, name, is_displayed FROM {MYSQL.TABLE.value}  WHERE is_displayed IS NULL LIMIT 1"

        await cursor.execute(query_get_null_couple)
        skill = await cursor.fetchone()
        connection.close()
        if skill:return Skill(*skill)
        else:return

async def confirm_skill(id: int, confirm: bool = True) -> None:
    connection = await connect_to_db()
    try:
        async with connection.cursor() as cursor:
            if confirm:
                await cursor.execute(f"UPDATE {MYSQL.TABLE.value} SET is_displayed=1 WHERE id={id}")
            else:
                await cursor.execute(f"UPDATE {MYSQL.TABLE.value} SET is_displayed=0 WHERE id={id}")

            await connection.commit()
    finally:
        connection.close()


async def refute_skill(id: int) -> None: # Опровергнуть сходство
    connection = await connect_to_db()
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(f"UPDATE {MYSQL.TABLE.value} SET is_displayed=null WHERE id={id}")
            await connection.commit()

    finally:
        connection.close()

async def get_previos_skill(current_id: int) -> Skill | None:
    connection = await connect_to_db()
    async with connection.cursor() as cursor:
        await cursor.execute(f"""SELECT id, name, is_displayed FROM {MYSQL.TABLE.value} WHERE id = {current_id-1}""")
        skill = await cursor.fetchone()

        try:res = Skill(*skill)
        except: res = None 

        if res is None: return
        await refute_skill(id=res.iD) # Делаем это для того, чтобы мы могли несколько раз подряд нажимать кнопку назад 
        connection.close()
        return res

async def show_the_rest() -> tuple[int, int]:
    connection = await connect_to_db()
    try:
        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT COUNT(*) FROM {MYSQL.TABLE.value}")
            count_all_values = await cursor.fetchone()

            await cursor.execute(f"SELECT COUNT(*) FROM {MYSQL.TABLE.value} WHERE is_displayed IS NULL")
            count_null_values = await cursor.fetchone()
            return count_all_values[0], count_null_values[0]
    except BaseException as err:
        exit(err)
    finally:
        connection.close()
