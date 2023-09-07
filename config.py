"""
    config.py
    ~~~~~~~~~
    app的配置信息，硬编码，不从环境变量中读取
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0

"""
"""
list of requirements:

JWT_SECRET_KEY
EMAIL_USERNAME
EMAIL_PASSWORD
DB_HOST
DB_USER
DB_PASSWORD
DB_PORT
DB_NAME
APP_ENCRYPT_SECRET
APP_INIT_SECRET
"""

from pydantic import BaseSettings
from typing import List
import os


class Config(BaseSettings):
    # 调试信息
    DEBUG = True
    # 跨域请求
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # Jwt
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60

    MYSQL_TABLE_AUTOGEN = True

    # Email server
    ENV_EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
    ENV_EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    EMAIL_USERNAME: str = ENV_EMAIL_USERNAME
    EMAIL_PASSWORD: str = ENV_EMAIL_PASSWORD
    EMAIL_HOST_SERVER: str = "smtp.163.com"

    DB_ORM_CONFIG: dict = {
        "connections": {
            "base": {
                'engine': 'tortoise.backends.mysql',
                "credentials": {
                    'host': os.environ.get("DB_HOST"),
                    'user': os.environ.get("DB_USER"),
                    'password': os.environ.get("DB_PASSWORD"),
                    'port': os.environ.get("DB_PORT"),
                    'database': os.environ.get("DB_NAME"),  # 数据库名称
                }
            },
        },
        "apps": {
            "base": {
                "models": [  # 列表应该包含所有的ORM映射文件
                    "model.File",
                    "model.User",
                    "model.Moral",
                    "model.Student",
                    "model.Info"
                ],
                "default_connection": "base"  # 链接的数据源
            },
        },
        'use_tz': False,
        'timezone': 'Asia/Shanghai'
    }

    # -----------------Redis-----------
    CACHE_CONFIG: dict = {
        "CACHE_HOST": os.environ.get("CACHE_HOST"),  # Redis连接
        "CACHE_PORT": os.environ.get("CACHE_PORT"),  # Redis端口
        "CACHE_CP": "utf-8",  # Redis CodePage （编码）
        "CACHE_decode_responses": True  # 与Redis的连接编码，True会将结果返回为字符串
    }
    CACHE_URL: str = f"redis://{CACHE_CONFIG['CACHE_HOST']}:{CACHE_CONFIG['CACHE_PORT']}"
    CACHE_DB_IDX: dict = {
        "system": 0,
        "code": 1,
        "log": 2,
        "access": 3,
        "info": 4,
        "doc": 5
    }

    SINGLE_FILE_STORAGE_PATH: List = [".", "storage", "single"]
    META_FILE_STORAGE_PATH: List = [".", "storage", "meta"]
    APP_ENCRYPT_SECRET: str = os.environ.get("APP_ENCRYPT_SECRET")
    APP_INIT_SECRET: str = os.environ.get("APP_INIT_SECRET")




config = Config()
