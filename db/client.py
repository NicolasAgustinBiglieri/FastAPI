
# Módulo conexión MongoDB: pip install pymongo
# Conexión: mongodb://localhost

from pymongo import MongoClient

# Conexión para base de datos local
# db_client = MongoClient()

# Conexión para base de datos remota
# db_client = MongoClient("mongodb+srv://biglieriagustin:aqui_la_contraseña@cluster0.uyybbuu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test

# Creamos las siguientes funciones para realizar la conexion
# pero ocultando la linea que contiene la contraseña de logueo de la db
# Para lo cual creamos un archivo json con dicha linea y la llamamos desde acá
import json

def obtener_configuracion():
    with open('db/config.json') as archivo_config:
        configuracion = json.load(archivo_config)
    return configuracion

def conectar_mongodb():
    configuracion = obtener_configuracion()
    uri = configuracion['mongodb_uri']
    db_client = MongoClient(uri).test
    return db_client
