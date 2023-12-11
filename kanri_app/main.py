from fastapi import FastAPI
from mangum import Mangum
from kanri_app.endpoints.v1.main_router import router as api_router


app = FastAPI(
    title="Kanri Project API",
    description="APIs para el proyecto **Kanri**, que permite a un servicio tecnico recibir equipos, y mantener su estado para los clientes",
    version="1.0v"
)
app.include_router(api_router, prefix="/v1")

handler = Mangum(app)
