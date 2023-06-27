from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import spotipy


sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(
    client_id='445c231e6c904ac6a4c338301b9b2ca2',
    client_secret='277c6fb54b6f43a9be9c680ab2df1e4f'
))

app = FastAPI()

class Vehiculo (BaseModel):
    id: int
    tipo: str
    marca: str
    modelo: str
    anio: int
    descripcion: Optional[str] = None

vehiculoList = []

@app.post("/vehiculos", response_model=Vehiculo)
def crear_vehiculo(vehiculo: Vehiculo):
    vehiculoList.append(vehiculo)
    return vehiculo

@app.get("/vehiculos", response_model=List[Vehiculo])
def get_vehiculos():
    return vehiculoList

@app.get("/vehiculos/{vehiculo_id}", response_model=Vehiculo)
def obtener_vehiculo (vehiculo_id: int):
    for vehiculo in vehiculoList:
        if vehiculo.id == vehiculo_id:
            return vehiculo
    raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

@app.delete("/vehiculos/{vehiculo_id}", response_model=List[Vehiculo])
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
