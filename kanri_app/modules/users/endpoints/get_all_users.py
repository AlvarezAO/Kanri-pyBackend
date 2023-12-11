from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from kanri_app.modules.users.model.user import User
from kanri_app.database.session import get_db
from kanri_app.utils.constantes.generales import EstadoUsuario
from kanri_app.utils.database import filtros, lista_blanca
from kanri_app.modules.users.schemas.response import GetAllUsersResponse
from sqlalchemy.exc import SQLAlchemyError
from kanri_app.utils.logger import get_logger
from kanri_app.modules.auth.endpoints.get_token import get_current_active_user

logger = get_logger(__name__)

router = APIRouter()

@router.get(
    path="/users",
    summary="Listar Usuarios Registrados",
    description="Obtiene un listado de todos los usuarios registrados y habilitados, con su información.",
    response_model=GetAllUsersResponse
    )
async def get_users(
    db = Depends(get_db), 
    current_user: User = Depends(get_current_active_user), 
    filters: Optional[str] = Query(None, example="nombre:John,correo:john@example.com", description="Filtros en formato 'campo1:valor1,campo2:valor2,...'."), 
    itemsByPage: Optional[int] = Query(10, gt=0, example=10, description="Cantidad de elementos que se quieran listar por página."),
    page: Optional[int] = Query(1, gt=0, example=1, description="Número de la página que se mostrará de los resultados."),
    order: Optional[str] = Query(None, example="nombre,asc", description="Indica el tipo de orden. Valores permitidos: 'asc', 'desc'.")
    ):
    try: 
        query = db.query(User).filter(User.estado_usuario == EstadoUsuario.HABILITADO.value)
        allowed_fields = lista_blanca.ALLOWED_FILTER_FIELDS.get('User', [])
        query = filtros.apply_filters(query, User, filters, allowed_fields)
        query = filtros.apply_order(query, User, order, allowed_fields)
        total_items = query.count()
        if itemsByPage and page:
            query = filtros.apply_pagination(query, page, itemsByPage)

        users = query.all()
        response = GetAllUsersResponse(
            usuarios=users,
            pagina=page,
            totalElementos=total_items,
            totalPaginas=filtros.calcular_total_paginas(total_items, itemsByPage),
            mensaje="Usuarios listados correctamente."
        )       
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuarios: {e}")
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error interno al procesar la solicitud."
        )

    return response
