import os
from typing import Optional, List
<<<<<<< HEAD

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
=======
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import ConfigDict, BaseModel, Field
>>>>>>> master
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from bson import ObjectId
<<<<<<< HEAD
import asyncio
from pymongo import AsyncMongoClient
from pymongo import ReturnDocument
=======
from pymongo import MongoClient, ReturnDocument
>>>>>>> master

# ------------------------------------------------------------------------ #
#                         Inicialització de l'aplicació                    #
# ------------------------------------------------------------------------ #
<<<<<<< HEAD
# Creació de la instància FastAPI amb informació bàsica de l'API
app = FastAPI(
    title="Student Course API",
    summary="Exemple d'API REST amb FastAPI i MongoDB per gestionar informació d'estudiants",
=======
app = FastAPI(
    title="Gestor de Tasques API - Ionut Antonio Ardelean",
    summary="API REST amb FastAPI i MongoDB (PyMongo) per gestionar tasques",
>>>>>>> master
)

# ------------------------------------------------------------------------ #
#                   Configuració de la connexió amb MongoDB                #
# ------------------------------------------------------------------------ #
<<<<<<< HEAD
# Creem el client de MongoDB utilitzant la URL de connexió emmagatzemada
# a les variables d'entorn. Això evita incloure credencials dins del codi.
client = AsyncMongoClient(os.environ["MONGODB_URL"])

# Selecció de la base de dades i de la col·lecció
db = client.college
student_collection = db.get_collection("students")

# Els documents de MongoDB tenen `_id` de tipus ObjectId.
# Aquí definim PyObjectId com un string serialitzable per JSON,
# que serà utilitzat als models Pydantic.
=======
MONGO_URL = "mongodb+srv://ionutantonioardelean:YqHSQRab6VbSeUjD@cluster0.6tlofo9.mongodb.net/"
client = MongoClient(MONGO_URL)
db = client['Sprint4']
task_collection = db.get_collection("GestorDeTasques")

# Tipus per gestionar el format d'ObjectId
>>>>>>> master
PyObjectId = Annotated[str, BeforeValidator(str)]

# ------------------------------------------------------------------------ #
#                            Definició dels models                         #
# ------------------------------------------------------------------------ #
<<<<<<< HEAD
class StudentModel(BaseModel):
    """
    Model que representa un estudiant.
    Conté tots els camps obligatoris i opcional `_id`.
    """
    # Clau primària de l'estudiant. 
    # MongoDB utilitza `_id`, però l'API exposa aquest camp com `id`.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    # Camps obligatoris de l'estudiant
    name: str = Field(...)
    email: EmailStr = Field(...)
    course: str = Field(...)
    gpa: float = Field(..., le=4.0)

    # Configuració addicional del model Pydantic
    model_config = ConfigDict(
        populate_by_name=True,  # Permet utilitzar alias al serialitzar/deserialitzar
        arbitrary_types_allowed=True,  # Permet tipus personalitzats com ObjectId
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": 3.0,
            }
        },
    )
=======

class TaskModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titol: str = Field(...)
    descripcio: str = Field(...)
    estat: str = Field(default="pendent") # Canviat de List a str
    prioritat: str = Field(...)
    categoria: str = Field(...)
    persona_assignada: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "titol": "Configurar servidor web",
                "descripcio": "Instal·lar Nginx i configurar el domini principal.",
                "estat": "pendent",
                "prioritat": "alta",
                "categoria": "Sistemes",
                "persona_assignada": "Marc Rovira"
            }
        },
    )

class UpdateTaskModel(BaseModel):
    titol: Optional[str] = None
    descripcio: Optional[str] = None
    estat: Optional[str] = None
    prioritat: Optional[str] = None
    categoria: Optional[str] = None
    persona_assignada: Optional[str] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

# ------------------------------------------------------------------------ #
#                               ENDPOINTS                                  #
# ------------------------------------------------------------------------ #

# SERVIR HTML: Accés des del directori frontend
@app.get("/ver", include_in_schema=False)
def ver_pagina_web():
    # Estructura: backend/app.py -> frontend/index.html
    ruta_html = os.path.join(os.getcwd(), "..", "frontend", "index.html")
    if os.path.exists(ruta_html):
        return FileResponse(ruta_html)
    return {"error": f"Fitxer index.html no trobat a: {ruta_html}"}

@app.get("/")
def inicio():
    return {"status": "API Online", "web": "/ver", "docs": "/docs"}

# LLISTAR: Totes les tasques
@app.get("/tasques", response_model=List[TaskModel])
def llistar_tasques():
    # En PyMongo síncron, convertim el cursor a list()
    cursor = task_collection.find().limit(100)
    return list(cursor)

# BUSCAR PER TÍTOL: (Find amb Regex)
@app.get("/buscar/{titol}", response_model=List[TaskModel])
def buscar_per_titol(titol: str):
    query = {"titol": {"$regex": titol, "$options": "i"}}
    resultados = list(task_collection.find(query).limit(10))
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No s'ha trobat cap tasca amb: {titol}")
    return resultados

# BUSCAR PER ID: (Find One)
@app.get("/buscar_id/{id_tasca}", response_model=TaskModel)
def buscar_per_id(id_tasca: str):
    if not ObjectId.is_valid(id_tasca):
        raise HTTPException(status_code=400, detail="ID no vàlid")
    
    resultado = task_collection.find_one({"_id": ObjectId(id_tasca)})
    if not resultado:
        raise HTTPException(status_code=404, detail="La tasca no existeix")
    return resultado

# CREAR: Nova tasca (POST)
@app.post("/crear", status_code=status.HTTP_201_CREATED, response_model=TaskModel)
def crear_tasca(datos: TaskModel = Body(...)):
    # model_dump substitueix a .dict() a Pydantic v2
    doc = datos.model_dump(by_alias=True, exclude=["id"])
    res = task_collection.insert_one(doc)
    
    nou_doc = task_collection.find_one({"_id": res.inserted_id})
    return nou_doc

# ACTUALITZAR: Editar camps (PUT)
@app.put("/actualizar/{id_tasca}", response_model=TaskModel)
def actualizar_tasca(id_tasca: str, datos: UpdateTaskModel = Body(...)):
    if not ObjectId.is_valid(id_tasca):
        raise HTTPException(status_code=400, detail="ID no vàlid")

    # Filtrem només els camps que no són None
    actualitzacio = {k: v for k, v in datos.model_dump().items() if v is not None}

    if len(actualitzacio) >= 1:
        res = task_collection.find_one_and_update(
            {"_id": ObjectId(id_tasca)},
            {"$set": actualitzacio},
            return_document=ReturnDocument.AFTER
        )
        if res:
            return res

    raise HTTPException(status_code=404, detail="Tasca no trobada per actualitzar")

# BORRAR: Eliminar (DELETE)
@app.delete("/borrar/{id_tasca}")
def borrar_tasca(id_tasca: str):
    if not ObjectId.is_valid(id_tasca):
        raise HTTPException(status_code=400, detail="ID no vàlid")

    res = task_collection.delete_one({"_id": ObjectId(id_tasca)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="ID no trobat")

    return {"mensaje": "Tasca eliminada amb èxit"}
>>>>>>> master
