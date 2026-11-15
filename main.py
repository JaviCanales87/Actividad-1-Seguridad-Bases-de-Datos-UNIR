from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from elasticsearch import AsyncElasticsearch
import os

# --- CONFIGURACIÓN DE CONEXIONES ---
# MongoDB: Con usuario autenticado (readWrite) creado tras activar --auth
MONGO_URL = os.getenv("MONGO_URL", "mongodb://app_user:password_segura@mongodb:27017/tienda_db")

# Elasticsearch: Conectado a través de la red interna de Docker (sin exponer puertos fuera)
ES_URL = os.getenv("ES_URL", "http://elasticsearch:9200")

db_client = None
es_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar conexiones al arrancar la app
    global db_client, es_client
    db_client = AsyncIOMotorClient(MONGO_URL)
    es_client = AsyncElasticsearch(ES_URL)
    yield
    # Cerrar conexiones al apagar la app
    db_client.close()
    await es_client.close()

app = FastAPI(
    title="API Segura NoSQL",
    description="Práctica de Seguridad en MongoDB y Elasticsearch",
    version="2.0",
    lifespan=lifespan
)

# ==========================================
# MODELOS PYDANTIC (Validación y Blindaje)
# ==========================================

class LoginRequest(BaseModel):
    # Forzar que sean strings puros evita inyecciones NoSQL donde el atacante envía un objeto {"$ne": None}
    usuario: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

class SearchQuery(BaseModel):
    termino: str = Field(..., min_length=1, max_length=50)
    pagina: int = Field(1, ge=1)
    tamanio_pagina: int = Field(10, ge=1, le=50) # Límite estricto para prevenir abusos de recursos


# ==========================================
# RUTAS / ENDPOINTS SEGUROS
# ==========================================

@app.get("/")
def read_root():
    return {"estado": "Servicio activo y blindado"}


@app.post("/login_mongo")
async def login_mongo(credentials: LoginRequest):
    """
    Endpoint de login seguro en MongoDB.
    Defensa contra NoSQLi: Pydantic valida que los campos sean strings estrictos,
    impidiendo la inyección de operadores lógicos de MongoDB.
    """
    try:
        db = db_client.get_database("tienda_db")
        
        # Búsqueda segura acotada a los tipos validados
        user = await db.usuarios.find_one({
            "usuario": credentials.usuario,
            "password": credentials.password  # En entorno real usar hashing (ej. bcrypt)
        })
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Credenciales incorrectas"
            )
            
        return {
            "mensaje": "Autenticación exitosa",
            "usuario": user["usuario"],
            "rol": user.get("rol", "usuario")
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error interno en la base de datos: {str(e)}"
        )


@app.post("/articulos/buscar")
async def buscar_articulos(query: SearchQuery):
    """
    Endpoint de búsqueda seguro en Elasticsearch.
    Defensas aplicadas:
    - Uso de consultas estructuradas 'match' en lugar de query strings libres.
    - Paginación obligatoria (from / size) para evitar extracciones masivas o DoS.
    """
    # Cálculo de desplazamiento para la paginación
    from_offset = (query.pagina - 1) * query.tamanio_pagina
    
    # Construcción de la consulta DSL segura
    body = {
        "from": from_offset,
        "size": query.tamanio_pagina,
        "query": {
            "match": {
                "contenido": query.termino
            }
        }
    }
    
    try:
        response = await es_client.search(index="articulos", body=body)
        
        # Extracción segura de los resultados
        hits = [hit["_source"] for hit in response["hits"]["hits"]]
        total_resultados = response["hits"]["total"]["value"]
        
        return {
            "pagina_actual": query.pagina,
            "resultados_por_pagina": query.tamanio_pagina,
            "total_encontrados": total_resultados,
            "resultados": hits
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error al consultar Elasticsearch: {str(e)}"
        )
