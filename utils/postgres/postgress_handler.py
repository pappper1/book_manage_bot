import psycopg2
import psycopg2.extras
from data.config import DB_NAME, DB_HOST, DB_USER, DB_PASS


async def postgres_do_query(query, params=None):
    with psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    ) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(query, params)
            conn.commit()


async def postgres_select_one(query, params=None):
    with psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    ) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
            if result:
                result = dict(result)

            conn.commit()

            return result


async def postgres_select_all(query, params=None):
    with psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    ) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()
            if results:
                res = []
                for r in results:
                    res.append(dict(r))

                results = res

            conn.commit()

            return results
