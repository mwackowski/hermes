import datetime
import os
import sqlite3
import sys
from uuid import uuid4
from typing import List, Dict

import pandas as pd
import psycopg2

sys.path.append("..")

from app.config.config_reader import config, DB_PARENT_DIR
from config.logger_config import set_logger


logger = set_logger()


def get_conn():
    return sqlite3.connect(os.path.join(DB_PARENT_DIR, "knowledge_db.sqlite"))


def get_postgres_conn(db_name: str = 'aidevs'):
    params = config()
    params['database'] = db_name
    return psycopg2.connect(**params)


def insert_into_knowledge_simple(content):
    conn = get_postgres_conn()
    cur = conn.cursor()
    today = datetime.date.today()
    uuid = str(uuid4())
    sql = 'insert into knowledge_simple(uuid, insert_date, content) values (%s, %s, %s)'
    try:
        cur.execute(sql, (uuid, today, content))
        conn.commit()
        logger.info('Inserted successfully')
    except Exception as e:
        logger.error(e)
    finally:
        conn.close()


def create_database_from_json(data: Dict, database_name: str):
    df = pd.DataFrame(data)
    df["uuid"] = df.apply(lambda row: str(uuid4()), axis=1)
    df["collection_name"] = database_name.upper()
    with get_conn() as conn:
        df.to_sql(database_name, conn, if_exists="append", index=False)


def read_table(table_name: str, conn = None) -> pd.DataFrame:
    if not conn:
        conn = get_conn()
    return pd.read_sql_query(f"select * from {table_name}", conn)


def query_table_by_uuid(table_name: str, uuid: str, conn = None) -> pd.DataFrame:
    if not conn:
        conn = get_conn()
    return pd.read_sql_query(f"select * from {table_name} where uuid = '{uuid}'", conn)

