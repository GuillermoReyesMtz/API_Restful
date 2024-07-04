# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 19:00:42 2023

@author: memo_
"""
from fastapi import Request,HTTPException
from functions_jwt import validate_token
from fastapi.routing import APIRoute


class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            token = request.headers.get("Authorization", "").split(" ")[1]

            validation_response = validate_token(token, output=False)

            if validation_response is None:
                return await original_route(request)
            else:
                raise HTTPException(status_code=401, detail="Unauthorized")

        return verify_token_middleware