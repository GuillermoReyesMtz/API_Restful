# -*- coding: utf-8 -*-
from fastapi import FastAPI, Depends, status, HTTPException, APIRouter
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import random
import fasttext
import joblib
import sklearn
from sklearn.svm import SVC
import numpy as np
from typing import Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
from routes.auth import auth_routes
from middlewares.verify_token_route import VerifyTokenRoute


app = FastAPI(route_class=VerifyTokenRoute,
              title="API REST para la Identificación Automática de Enunciados con Diagnósticos",
              description="API REST especializada que se encargue de la fase de filtrado de enunciados, evaluando la presencia o ausencia de diagnósticos.",
              version="1.0.0",
              docs_url="/docs",
              redoc_url="/redoc",
              openapi_url="/openapi.json",)

app.include_router(auth_routes, prefix="/api")
load_dotenv()

# Cargar el modelo FastText
model = fasttext.load_model(r'C:\Users\memo_\Downloads\embeddings-m-model.bin')

# Cargar el modelo binario (clasificador)
classifier_model = joblib.load(r'C:\Users\memo_\Downloads\svm_trained.joblib')


@app.get('/',summary="Acerca de", description="Este endpoint es para describir la API REST en terminos generales")
async def root():
    return{'Titulo': 'Desarrollo de una API REST para la Identificación Automática de Enunciados con Diagnósticos',
           'Curso': 'Arquitecturas de Software', 'Alumno':'Guillermo Reyes Martínez', 'Maestro':'Jared Guerrero'}


@app.get('/vectorize/{ngram}',summary="Vectoriza n-grama de 5 tokens", description= "Este endpoint se emplea para devolver al usuario una representación de 100 dimensiones dado un ngrama formado por 5 tokens")
async def vectorize_ngram(ngram: str):
    try:
        # Tokenizar la cadena ngram
        tokens = ngram.split()

        # Vectorizar el ngram utilizando el modelo FastText
        vectors = [model[word] for word in tokens if word in model]

        if vectors:
            # Calcular el promedio de los vectores
            vector_mean = np.mean(vectors, axis=0)
            return {"vector": vector_mean.tolist()}
        else:
            raise HTTPException(status_code=404, detail="No se encontraron vectores para las palabras en el modelo.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al vectorizar ngram: {str(e)}")

@app.get('/classify_ngram/{ngram}',summary="Clasifica un n-grama de 5 tokens dependiendo si este contiene un diagnóstico o no", description="Este endpoint se emplea para clasificar un ngrama de 5 tokens mediante el modelo de SVM preentrenado")
async def classify_string(ngram: str):
    try:
        tokens = ngram.split()
        vectors = [model[word] for word in tokens if word in model]
        vector_mean = np.mean(vectors, axis=0)
        vector = np.array(vector_mean).reshape(1, -1)
        prediction = classifier_model.predict(vector)
        if prediction[0] == 1:
            return{"n-gram": "Contiene un diagnóstico"}
        else:
            return{"n-gram": "No contiene un diagnóstico"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al clasificar el ngram: {str(e)}")


"""
Created on Thu Nov 30 16:59:03 2023

@author: memo_
"""

