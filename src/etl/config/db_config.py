import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 加载 .env 文件
load_dotenv()

# 源数据库连接字符串 (SQL Server)
SRC_CONN_STR = f"mssql+pyodbc://{os.getenv('SRC_DB_USER')}:{os.getenv('SRC_DB_PASSWORD')}@{os.getenv('SRC_DB_HOST')}:{os.getenv('SRC_DB_PORT')}/{os.getenv('SRC_DB_NAME')}?driver=SQL+Server"

# 目标数据库连接字符串 (SQL Server)
TGT_CONN_STR = f"mssql+pyodbc://{os.getenv('TGT_DB_USER')}:{os.getenv('TGT_DB_PASSWORD')}@{os.getenv('TGT_DB_HOST')}:{os.getenv('TGT_DB_PORT')}/{os.getenv('TGT_DB_NAME')}?driver=SQL+Server"

def get_src_engine():
    return create_engine(SRC_CONN_STR)

def get_tgt_engine():
    return create_engine(TGT_CONN_STR)
