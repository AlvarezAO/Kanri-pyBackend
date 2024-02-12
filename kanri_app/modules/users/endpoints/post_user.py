from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from kanri_app.modules.users.schemas.base import UserCreate, UserRead
from kanri_app.modules.users.model.user import User
from kanri_app.modules.auth.services import hash_password, generate_secure_password
from kanri_app.utils.constantes.generales import EstadoUsuario, EstadoYesOrNo
from kanri_app.database.session import get_db
from kanri_app.modules.users.schemas.response import CreateGetOrUpdateUserResponse
from kanri_app.modules.auth.endpoints.get_token import get_current_active_user
from sqlalchemy.exc import SQLAlchemyError
from kanri_app.utils.logger import get_logger
from sqlalchemy.orm import Session
from uuid import uuid4

logger = get_logger(__name__)

router = APIRouter()

@router.post(path="/users", 
            summary="Crear Usuario",
            description="Crea usuario en los registros del sistema",
            response_model=CreateGetOrUpdateUserResponse)
async def post_user(user: UserCreate, db = Depends(get_db), current_user: User = Depends(get_current_active_user)) -> UserRead:
    if not valida_existencia_usuario(user, db):
        db_user = create_user(db, user)        
        #TODO enviar un email al correo de usuario registrado, con la clave predeterminada para que la actualice
        # template armarlo con jinja, y ver como enviar correos y guardar registros de estos. 
        return CreateGetOrUpdateUserResponse(mensaje="Usuario ha sido creado exitosamente.",
                                            usuario=db_user)
    else:
        return CreateGetOrUpdateUserResponse(mensaje="Error al crear el usuario.",
                                            codigo=409,
                                            estado="Error")


def create_user(db: Session, user: UserCreate) -> UserRead:
    secure_password = generate_secure_password()
    logger.info(f"Contraseña creada: {secure_password}")
    hashed_password = hash_password(secure_password)
    try:
        db_user = User(
            usuario_id = str(uuid4()),
            nombre = user.nombre,
            alias = user.alias,
            rut = user.rut,
            correo = user.correo,
            avatar = user.avatar,
            departamento = user.departamento,
            cambiar_clave = EstadoYesOrNo.NO.value,  #Se deja en NO, por ahora hasta implementar correo y vista
            fecha_creacion = datetime.now(),
            ingresos_fallidos = 0,
            estado_usuario = EstadoUsuario.HABILITADO.value,
            acceso_web = EstadoYesOrNo.SI.value,
            clave = hashed_password          
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)   
        return db_user
    
    except SQLAlchemyError as e:
        logger.error(f"Error al crears usuario: {e}")
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error interno al procesar la solicitud."
        )
    
    
def valida_existencia_usuario(user: UserCreate, db: Session):
    rut_formateado = user.rut.replace(".", "")
    user = db.query(User).filter(User.rut == rut_formateado or User.correo == user.correo).first()
    exist = True if user else False
    return exist
    