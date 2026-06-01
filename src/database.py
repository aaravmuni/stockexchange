import config
import mysql.connector
from mysql.connector import pooling

pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="sqlpool",
    pool_size=5,
    host="localhost",
    user="exchangedbuser",
    password=config.DB_USER_PASSWORD,
    database="exchangelogin"
)