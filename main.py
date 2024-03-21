
"""
FastAPI:

FastAPI aconseja utilizar Type Hints para un mejor funcionamiento.

Guía de instalación, consejos, etc:
https://fastapi.tiangolo.com/

# Documentación oficial: https://fastapi.tiangolo.com/es/
# Instala FastAPI: pip install "fastapi[all]"

# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C
para levantar el servidor y que se recargue automaticamente
(donde dice main se pone el nombre del archivo, en este mismo fichero seria main, en el 
segundo del curso seria users, etc)

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc

Generamos peticiones desde Thunder Client (como extensión en VSCode)
"""

from fastapi import FastAPI
from routers import products, users

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"¡Hola FastAPI"}

@app.get("/url")
async def url():
    return { "url_curso":"https://mouredev.com/python" }
