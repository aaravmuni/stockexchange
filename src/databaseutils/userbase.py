import database
from mysql.connector import Error

def getid(username:str) -> int:
    conn = None
    cursor = None
    result = None
    try:
        conn = database.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username = %s",(username,)
        )
        result = cursor.fetchone()[0]
    except Error:
        return -1
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    
    if result is None:
        return -1
    
    return result