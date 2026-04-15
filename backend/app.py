import os
from typing import Optional, List
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pymongo import MongoClient, ReturnDocument
from fastapi.staticfiles import StaticFiles

# ------------------------------------------------------------------------ #
#                         Inicialització de l'aplicació                    #
# ------------------------------------------------------------------------ #
app = FastAPI(
    title="Gestor de Tasques API - Ionut Antonio Ardean",
    summary="API REST amb FastAPI i MongoDB (PyMongo) per gestionar tasques",
)

# ------------------------------------------------------------------------ #
#                   Configuració de la connexió amb MongoDB                #
# ------------------------------------------------------------------------ #
MONGO_URL = "mongodb+srv://ionutantonioardelean:YqHSQRab6VbSeUjD@cluster0.6tlofo9.mongodb.net/"
client = MongoClient(MONGO_URL)
db = client['Sprint4']
task_collection = db.get_collection("GestorDeTasques")

# Tipus per gestionar el format d'ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

# ------------------------------------------------------------------------ #
#                            Definició dels models                         #
# ------------------------------------------------------------------------ #
class TaskModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titol: str = Field(...)
    descripcio: str = Field(...)
    estat: str = Field(default="pendent")
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

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/ver", include_in_schema=False)
def ver_pagina_web():
    # Aquesta part la deixem igual, és correcta
    ruta_html = os.path.join(os.getcwd(), "..", "frontend", "index.html")
    if os.path.exists(ruta_html):
        return FileResponse(ruta_html)
    return {"error": f"Fitxer no trobat"}


@app.get("/")
def inicio():
    return {"status": "API Online", "web": "/ver", "docs": "/docs"}

@app.get("/tasques", response_model=List[TaskModel])
def llistar_tasques():
    cursor = task_collection.find().limit(100)
    return list(cursor)

@app.get("/buscar/{titol}", response_model=List[TaskModel])
def buscar_per_titol(titol: str):
    query = {"titol": {"$regex": titol, "$options": "i"}}
    resultados = list(task_collection.find(query).limit(10))
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No s'ha trobat cap tasca amb: {titol}")
    return resultados

@app.get("/buscar_id/{id_tasca}", response_model=TaskModel)
def buscar_per_id(id_tasca: str):
    if not ObjectId.is_valid(id_tasca):
        raise HTTPException(status_code=400, detail="ID no vàlid")
    
    resultado = task_collection.find_one({"_id": ObjectId(id_tasca)})
    if not resultado:
        raise HTTPException(status_code=404, detail="La tasca no existeix")
    return resultado

@app.post("/crear", status_code=status.HTTP_201_CREATED, response_model=TaskModel)
def crear_tasca(datos: TaskModel = Body(...)):
    doc = datos.model_dump(by_alias=True, exclude=["id"])
    res = task_collection.insert_one(doc)
    nou_doc = task_collection.find_one({"_id": res.inserted_id})
    return nou_doc

@app.put("/actualizar/{id_tasca}", response_model=TaskModel)
def actualizar_tasca(id_tasca: str, datos: UpdateTaskModel = Body(...)):
    if not ObjectId.is_valid(id_tasca):
        raise HTTPException(status_code=400, detail="ID no vàlid")

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

@app.delete("/borrar/{id_tasca}")
def borrar_tasca(id_tasca: str):
    if not ObjectId.is_valid(id_tasca):
        raise HTTPException(status_code=400, detail="ID no vàlid")

    res = task_collection.delete_one({"_id": ObjectId(id_tasca)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="ID no trobat")

    return {"mensaje": "Tasca eliminada amb èxit"}
