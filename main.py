from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

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


@app.get("/")
def read_root():
    return {"Tarea": "Interoperabilidad Empresarial - Cloud Deployment"}
