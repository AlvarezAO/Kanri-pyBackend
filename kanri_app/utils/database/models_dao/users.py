from kanri_app.modules.users.model.user import User
from fastapi import Depends


def busca_usuario_por_rut(rut: str, db):
    user: User = db.query(User).filter(User.rut == rut).first()
    return user


def busca_usuario_por_id(id: str, db= Depends()):
    user: User = db.query(User).filter(User.usuario_id == id).first()
    return user