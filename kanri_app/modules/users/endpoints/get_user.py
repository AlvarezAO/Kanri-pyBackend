from fastapi import Path
from fastapi import APIRouter, Depends, HTTPException
from kanri_app.modules.users.model.user import User
from kanri_app.database.session import get_db
from kanri_app.modules.users.schemas.response import CreateGetOrUpdateUserResponse
from kanri_app.modules.auth.endpoints.get_token import get_current_active_user
from sqlalchemy.exc import SQLAlchemyError
from kanri_app.utils.logger import get_logger

logger = get_logger(__name__)


router = APIRouter()

@router.get(path="/users/{user_id}", 
            summary="Obtiene Usuario", 
            description="Obtiene información del usuario indicado por su ID.",
            response_model=CreateGetOrUpdateUserResponse
            )
async def get_users(user_id: str = Path(..., description="ID del usuario a buscar."), 
                    db = Depends(get_db), 
                    current_user: User = Depends(get_current_active_user)):
    
    try:
        user = db.query(User).filter(User.usuario_id == user_id).first()
        if not user:
            return CreateGetOrUpdateUserResponse(mensaje="Usuario no existe en nuestros registros",
                                                estado="Error",
                                                codigo=404)            
        else:
            return CreateGetOrUpdateUserResponse(mensaje="Usuario ha sido encontrado con éxito",
                                                usuario= user)
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener usuario: {e}")
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error interno al procesar la solicitud."
        )
