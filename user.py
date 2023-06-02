import mysql.connector
from configparser import ConfigParser
# from torch import _fake_quantize_per_tensor_affine_cachemask_tensor_qparams
CNX: mysql.connector.connect = None

configs = {
    'host': 'mysql',
    'user': 'root',
    'password': 'root',
    'database': 'streamlit',
    'port': 3306
}


def login(userName: str, password: str) -> bool:
    if (userName is None):
        return False
    args = [userName, password, 0]
    # result_args = execute_sql_query("CheckUser", args)
    # return (result_args[2] == 1)
    return 1


def execute_sql_query(query, args):
    CNX = mysql.connector.connect(**configs)

    with CNX.cursor() as cur:
        return cur.callproc(query, args)
