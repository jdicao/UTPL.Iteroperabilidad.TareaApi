from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import spotipy
import pymongo
import uuid
from auth import *

from fastapi_versioning import VersionedFastAPI, version
from fastapi.security import HTTPBasic, HTTPBasicCredentials

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

#para manejar seguridad
security = HTTPBasic()

#cliente = pymongo.MongoClient("mongodb+srv://utplapi:1Xh41Mq3imkRCxbc@cluster01jdc.dixpkq6.mongodb.net/?retryWrites=true&w=majority")
cliente = pymongo.MongoClient("mongodb+srv://utplapi:VtFbaCLGheOU389I@cluster01jdc.dixpkq6.mongodb.net/")
database = cliente["concesionario"]
coleccion = database["vehiculo"]

class VehiculoRepositorio (BaseModel):
    id: str
    tipo: str
    marca: str
    modelo: str
    anio: int
    color: Optional[str] = None
    descripcion: Optional[str] = None

class VehiculoEntrada (BaseModel):
    tipo: str
    marca: str
    modelo: str
    anio: int
    descripcion: Optional[str] = None

class VehiculoEntradaV2 (BaseModel):
    tipo: str
    marca: str
    modelo: str
    anio: int
    color: str
    descripcion: Optional[str] = None

vehiculoList = []

@app.post("/vehiculos", response_model=VehiculoRepositorio, tags = ["Vehiculos"])
@version(1, 0)
async def crear_vehiculo(vehiculoE: VehiculoEntrada):
    #vehiculoList.append(vehiculo)
    itemVehiculo = VehiculoRepositorio(id = str(uuid.uuid4()), tipo = vehiculoE.tipo, marca = vehiculoE.marca, modelo = vehiculoE.modelo, anio = vehiculoE.anio, descripcion = vehiculoE.descripcion )
    resultadoDB =  coleccion.insert_one(itemVehiculo.dict())
    return itemVehiculo

@app.post("/vehiculos", response_model=VehiculoRepositorio, tags = ["Vehiculos"])
@version(2, 0)
async def crear_vehiculoV2(vehiculoE: VehiculoEntradaV2):
    #vehiculoList.append(vehiculo)
    itemVehiculo = VehiculoRepositorio(id = str(uuid.uuid4()), tipo = vehiculoE.tipo, marca = vehiculoE.marca, modelo = vehiculoE.modelo, anio = vehiculoE.anio, descripcion = vehiculoE.descripcion, color = vehiculoE.color )
    resultadoDB =  coleccion.insert_one(itemVehiculo.dict())
    return itemVehiculo    

@app.get("/vehiculos", response_model=List[VehiculoRepositorio], tags = ["Vehiculos"])
@version(1, 0)
def get_vehiculos():
    #authenticate(credentials)
    items = list(coleccion.find({}, {'_id': 0}))
    print (items)
    #vehiculoList.append(items)
    return items
    #vehiculoList

@app.get("/vehiculos/{vehiculo_id}", response_model=VehiculoRepositorio, tags = ["Vehiculos"])
@version(1, 0)
def obtener_vehiculo (vehiculo_id: str):
    item = coleccion.find_one({"id": vehiculo_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado !")    
    #for vehiculo in vehiculoList:
    #    if vehiculo.id == vehiculo_id:
    #        return vehiculo
    #raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

@app.delete("/vehiculos/{vehiculo_id}", tags = ["Vehiculos"])
@version(1, 0)
def eliminar_vehiculo (vehiculo_id: str):
    result = coleccion.delete_one({"id": vehiculo_id})
    if result.deleted_count == 1:
        return {"mensaje": "Vehiculo eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

    #for vehiculo in vehiculoList:
    #   if vehiculo.id == vehiculo_id:
    #       vehiculoList.remove(vehiculo)
    #       return vehiculoList
    #raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

@app.get("/pista/{track_id}")
@version(1, 0)
async def obenter_pista(track_id: str):
    pista = sp.track(track_id)
    return pista

@app.get("/artistas/{artista_id}")
@version(1, 0)
async def get_artista(artista_id: str):
    artista = sp.artist(artista_id)
    return artista

@app.get("/")
def read_root():
    return {"Tarea Interoperabilidad": "Tercer cambio para prueba de despliegue"}

app = VersionedFastAPI(app)
