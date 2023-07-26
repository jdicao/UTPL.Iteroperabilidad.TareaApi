from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import spotipy
import pymongo


sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(
    client_id='445c231e6c904ac6a4c338301b9b2ca2',
    client_secret='277c6fb54b6f43a9be9c680ab2df1e4f'
))

description = """
Utpl tnteroperabilidad API ayuda a describir las capacidades de un directorio. 🚀

## Vehiculos
 
Se puede: **Crear, listar y eliminar Vehiculos**.

## Artisitas

Se puede: **Obtener informacion de una pista, Obtener informacion de un artista**.

"""
tags_metadata = [
    {
        "name":"Vehiculos",
        "description": "Permite realizar un crud completo de una Vehiculo (listar)"
    }
]

#app = FastAPI()
app = FastAPI(
    title="Utpl Interoperabilidad APP",
    description = description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Jefferson Dicao C.",
        "url": "http://x-force.example.com/contact/",
        "email": "jpdicao@utpl.edu.ec",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags = tags_metadata

)

#configuracion de mongo

cliente = pymongo.MongoClient("mongodb+srv://utplapi:b3wUGM7SlqvYIIRC@cluster01jdc.dixpkq6.mongodb.net/?retryWrites=true&w=majority")
database = client["concesionario"]
colecion = database["vehiculo"]

class VehiculoRepositorio (BaseModel):
    id: str
    tipo: str
    marca: str
    modelo: str
    anio: int
    descripcion: Optional[str] = None

class VehiculoEntrada (BaseModel):
    tipo: str
    marca: str
    modelo: str
    anio: int
    descripcion: Optional[str] = None

vehiculoList = []

@app.post("/vehiculos", response_model=VehiculoEntrada, tags = ["Vehiculos"])
def crear_vehiculo(vehiculo: VehiculoEntrada):
    vehiculoList.append(vehiculo)
    return vehiculo

@app.get("/vehiculos", response_model=List[VehiculoRepositorio], tags = ["Vehiculos"])
def get_vehiculos():
    return vehiculoList

@app.get("/vehiculos/{vehiculo_id}", response_model=VehiculoRepositorio, tags = ["Vehiculos"])
def obtener_vehiculo (vehiculo_id: int):
    for vehiculo in vehiculoList:
        if vehiculo.id == vehiculo_id:
            return vehiculo
    raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

@app.delete("/vehiculos/{vehiculo_id}", response_model=List[Vehiculo], tags = ["Vehiculos"])
def eliminar_vehiculo (vehiculo_id: int):
    for vehiculo in vehiculoList:
        if vehiculo.id == vehiculo_id:
            vehiculoList.remove(vehiculo)
            return vehiculoList
    raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

@app.get("/pista/{track_id}")
async def obenter_pista(track_id: str):
    pista = sp.track(track_id)
    return pista

@app.get("/artistas/{artista_id}")
async def get_artista(artista_id: str):
    artista = sp.artist(artista_id)
    return artista

@app.get("/")
def read_root():
    return {"Tarea Interoperabilidad": "Tercer cambio para prueba de despliegue"}
