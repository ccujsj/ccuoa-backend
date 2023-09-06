# -*- coding:utf-8 -*-
"""
    core.exceptions.py
    ~~~~~~~~~
    统一错误收集
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Union
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from tortoise.exceptions import OperationalError, DoesNotExist, IntegrityError, ValidationError as MysqlValidationError
from core.logger import logger

async def mysql_validation_error(_: Request, exc: MysqlValidationError) -> JSONResponse:
    """
    数据库字段验证错误
    :param _:
    :param exc:
    :return:
    """
    print("ValidationError", exc)
    return JSONResponse({
        "code": -1,
        "message": exc.__str__(),
        "data": []
    }, status_code=422)


async def mysql_integrity_error(_: Request, exc: IntegrityError) -> JSONResponse:
    """
    完整性错误
    :param _:
    :param exc:
    :return:
    """
    print("IntegrityError", exc)
    return JSONResponse({
        "code": -1,
        "message": exc.__str__(),
        "data": []
    }, status_code=422)


async def mysql_does_not_exist(_: Request, exc: DoesNotExist) -> JSONResponse:
    """
    mysql 查询对象不存在异常处理
    :param _:
    :param exc:
    :return:
    """
    print("DoesNotExist", exc)
    return JSONResponse({
        "code": -1,
        "message": "发出的请求针对的是不存在的记录，服务器没有进行操作。",
        "data": []
    }, status_code=404)


async def mysql_operational_error(_: Request, exc: OperationalError) -> JSONResponse:
    """
    mysql 数据库异常错误处理
    :param _:
    :param exc:
    :return:
    """
    print("OperationalError", exc)
    return JSONResponse({
        "code": -1,
        "message": "数据操作失败",
        "data": []
    }, status_code=500)


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """
    http异常处理
    :param _:
    :param exc:
    :return:
    """
    if exc.status_code == 401:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

    return JSONResponse({
        "code": exc.status_code,
        "message": exc.detail,
        "data": exc.detail
    }, status_code=exc.status_code, headers=exc.headers)


class UnicornException(Exception):

    def __init__(self, code, errmsg, data=None):
        """
        失败返回格式
        :param code:
        :param errmsg:
        """
        if data is None:
            data = {}
        self.code = code
        self.errmsg = errmsg
        self.data = data


async def unicorn_exception_handler(_: Request, exc: UnicornException) -> JSONResponse:
    """
    unicorn 异常处理
    :param _:
    :param exc:
    :return:
    """
    return JSONResponse({
        "code": exc.code,
        "message": exc.errmsg,
        "data": exc.data,
    })


async def http422_error_handler(_: Request, exc: Union[RequestValidationError, ValidationError],) -> JSONResponse:
    """
    参数校验错误处理
    :param _:
    :param exc:
    :return:
    """
    print("[422]", exc.errors())
    return JSONResponse(
        {
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": f"数据校验错误 {exc.errors()}",
            "data": exc.errors(),
        },
        status_code=422,
    )
