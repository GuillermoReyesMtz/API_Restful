# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 16:06:57 2023

@author: memo_
"""

from fastapi import APIRouter, Header
from pydantic import BaseModel, EmailStr
from functions_jwt import write_token, validate_token
from fastapi.responses import JSONResponse

auth_routes = APIRouter()

class User(BaseModel):
    username: str
    email: EmailStr

@auth_routes.post("/login", description="Este endpoint solicita las credenciales del usuario, si este usuario existe en la base de datos simulada, entonces devuelve un token cifrado mediante una variable de entorno")
def login(user: User):
    print(user.dict())
    if user.username == "Guillermo Reyes":
        return write_token(user.dict())
    else:
        return JSONResponse(content={"message": "Usuario no encontrado"}
                            , status_code=404)

@auth_routes.post("/verify/token", summary="Verifica si el token enviado es valido", description="Este endpoint valida si el token recibido corresponde a algun token generado mediante la autenticación de credenciales")
def verify_token(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    return validate_token(token, output=True)