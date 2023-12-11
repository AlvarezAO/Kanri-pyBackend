from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from kanri_app.modules.auth.schemas.base import TokenData, Token, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from kanri_app.modules.auth.services import verify_password
from kanri_app.database.session import get_db
from kanri_app.utils.constantes.generales import EstadoUsuario
from kanri_app.modules.users.model.user import User
from jose import JWTError, jwt
from kanri_app.utils.logger import get_logger
from datetime import datetime, timedelta
from typing import Union
from kanri_app.utils.constantes.generales import EstadoUsuario
from kanri_app.utils.database.models_dao.users import busca_usuario_por_rut, busca_usuario_por_id

logger = get_logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login", scopes={})

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db = Depends(get_db)) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Rut o contraseña incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.usuario_id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)


def authenticate_user(username: str, password: str, db = Depends(get_db)):
    user = busca_usuario_por_rut(username, db)
    if not user:
        return False
    if not verify_password(user.clave, password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    user = busca_usuario_por_id(id=token_data.id, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.estado_usuario == EstadoUsuario.DESHABILITADO.value:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
