import database
from decimal import Decimal
from mysql.connector import Error

def readbalance(userid:int) -> str:
    conn = None
    cursor = None
    result = None
    try:
        conn = database.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT balance FROM balances WHERE user_id = %s", (userid,)
        )
        result = str(cursor.fetchone()[0])
    except Error:
        return "database_error"
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    
    if result is None:
        return "user_notfound"
    
    return result

def recordtransaction(userid:int, amount:Decimal, type:str) -> str:
    types = ["deposit", "withdrawal", "buy", "sell"]
    if type not in types:
        return "incorrect_type"
    if not(Decimal("-9999999999999.99") <= amount <= Decimal("9999999999999.99")):
        return "invalid_amount"
    if (amount <= Decimal("0.0") and type in ["deposit","sell"]) or (amount >= Decimal("0.0") and type in ["withdrawal","buy"]):
        return "type_contradiction"
    conn = None
    cursor = None
    try:
        conn = database.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (user_id,amount,type) VALUES (%s,%s,%s)",(userid,amount,type)
        )
        cursor.execute(
            "UPDATE balances SET balance = balance + (%s) WHERE user_id = (%s)",(amount,userid)
        )
        conn.commit()
        return "ok"
    except Error:
        conn.rollback()
        return "database_error"
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    