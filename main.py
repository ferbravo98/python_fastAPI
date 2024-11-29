#API REST: Interfaz de programacion de aplicaciones para compartir recursos

from typing import List,Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#Inicializamos una variable que tendra las caracteristicas de una API REST
app= FastAPI()

#DEFINICION DEL MODELO
class Curso(BaseModel):
    id: Optional[str]= None
    nombre: str
    descripcion: Optional[str]= None
    nivel: str
    duracion: int 
    
#Simulacion de base de datos
cursos_db = []

#CRUD : Read (lectura) GET ALL: Se van a leer todos los cursos que hay en la base de datos 
@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return cursos_db

#CRUD : Create (escribir) GET ALL: Se van a leer todos los cursos que hay en la base de datos 
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id= str(uuid.uuid4()) #Usamos UUID para generar ID unico e irrepetible
    cursos_db.append(curso)
    return curso
    
#CRUD: Read (lectura) GET(individual): Leeremos el curso que coincide con el ID que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso= next((curso for curso in cursos_db if curso.id == curso_id), None) # Con NEXT tomamos la primera coincidencia del array devuelto
    if curso is None :
        raise HTTPException(status_code=404, detail= "Curso no encontrado")
    return curso

#CRUD: Update (actualizar/modificar) PUT: Modificamos un recurso que coincida con el ID que mandamos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso= next((curso for curso in cursos_db if curso.id == curso_id), None) # Con NEXT tomamos la primera coincidencia del array devuelto
    if curso is None :
        raise HTTPException(status_code=404, detail= "Curso no encontrado")
    curso_actualizado.id= curso_id
    index= cursos_db.index(curso) #Buscamos el indice exacto donde esta el curso en nuestra lista
    cursos_db[index]=curso_actualizado
    return curso_actualizado

#CRUD: Delete (borrado/baja) DELETE: Eliminaremos un recurso que coincida por la ID
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso= next((curso for curso in cursos_db if curso.id == curso_id), None) # Con NEXT tomamos la primera coincidencia del array devuelto
    if curso is None :
        raise HTTPException(status_code=404, detail= "Curso no encontrado")
    cursos_db.remove(curso)
    return curso