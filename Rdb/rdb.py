import mysql.connector
from typing import Union
from mysql.connector import MySQLConnection, CMySQLConnection
from mysql.connector.cursor import CursorBase, MySQLCursor, MySQLCursorBuffered, MySQLCursorRaw, MySQLCursorBufferedRaw, \
    MySQLCursorDict, MySQLCursorBufferedDict, MySQLCursorNamedTuple, MySQLCursorBufferedNamedTuple, MySQLCursorPrepared
import config

TheMySQLConnection = Union[MySQLConnection, CMySQLConnection]
TheMySQLCursor = Union[
    CursorBase, MySQLCursor, MySQLCursorBuffered, MySQLCursorRaw, MySQLCursorBufferedRaw, MySQLCursorDict, MySQLCursorBufferedDict, MySQLCursorNamedTuple, MySQLCursorBufferedNamedTuple, MySQLCursorPrepared]

__conn: TheMySQLConnection = mysql.connector.connect(
    host=config.mysql_host,
    port=config.mysql_port,
    user=config.mysql_user,
    password=config.mysql_password,
    database=config.mysql_database,
    auth_plugin='mysql_native_password'
)


def conn() -> TheMySQLConnection:
    # @ref https://basicincome30.com/python3-mysql-connector
    # reconnect if needed
    __conn.ping(reconnect=True)
    return __conn


def cursor(*args, **kwargs) -> TheMySQLCursor:
    return conn().cursor(*args, **kwargs)


class Cursor:
    # @ref http://a-zumi.net/mysql-connector-python-wrapper/
    # cursor wrapper to support `with` statement
    def __init__(self, *args, **kwargs):
        self.cursor: TheMySQLCursor = cursor(*args, **kwargs)

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
