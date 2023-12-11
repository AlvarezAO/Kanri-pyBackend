from fastapi import APIRouter, Depends, HTTPException, Path
from kanri_app.modules.users.schemas.base import UserUpdate, UserRead
from kanri_app.modules.users.schemas.response import CreateGetOrUpdateUserResponse
from kanri_app.modules.auth.endpoints.get_token import get_current_active_user
from kanri_app.modules.users.model.user import User
from kanri_app.modules.auth.services import hash_password, verify_password
from kanri_app.database.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from kanri_app.utils.logger import get_logger

logger = get_logger(__name__)


router = APIRouter()

@router.put(path="/users/{user_id}", 
            summary="Actualizar Usuario", 
            description="Actualiza los datos del usuario",
            response_model=CreateGetOrUpdateUserResponse)
async def put_user(user: UserUpdate,user_id: str= Path(..., description="ID del usuario a buscar."), 
                db = Depends(get_db), 
                current_user: User = Depends(get_current_active_user)) -> UserRead:
    db_user = update_user(db, user_id, user)
    
    if not db_user:
        return CreateGetOrUpdateUserResponse(mensaje="Usuario no existe en nuestros registros.",
                                            estado="Error",
                                            codigo=404)
    else:
        return CreateGetOrUpdateUserResponse(mensaje="Usuario se ha actualizado correctamente.",
                                            usuario=db_user)


def update_user(db: Session, user_id: str, user: UserUpdate) -> CreateGetOrUpdateUserResponse:
    try:
        # Buscar el usuario en la base de datos por el user_id
        db_user = db.query(User).filter(User.usuario_id == user_id).first()
        if not db_user:
            return 

        # Actualizar los campos del usuario
        if user.nombre: db_user.nombre = user.nombre
        if user.alias: db_user.alias = user.alias
        if user.rut: db_user.rut = user.rut
        if user.correo: db_user.correo = user.correo
        if user.avatar: db_user.avatar = user.avatar
        if user.departamento: db_user.departamento = user.departamento
        if user.acceso_web: db_user.acceso_web = user.acceso_web
        if user.clave and not verify_password(db_user.clave, user.clave):
            # Solo actualiza la contraseña si es diferente a la actual
            db_user.clave = hash_password(user.clave)

        # Guardar los cambios en la base de datos
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error interno al actualizar usuario {e}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar el usuario")
