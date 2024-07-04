# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 15:09:10 2023

@author: memo_
"""
from jwt import encode, decode
from datetime import datetime, timedelta
from os import getenv
from jwt import exceptions
from fastapi.responses import JSONResponse

def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date

def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(2) },
                   key=getenv("SECRET"), algorithm="HS256")
    return token

def validate_token(token, output='False'):
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms= ["HS256"])
        decode(token, key=getenv("SECRET"), algorithms= ["HS256"])
    except exceptions.DecodeError:
        return JSONResponse(content={"message": "Invalid Token"},
                            status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expired"},
                            status_code=401)
