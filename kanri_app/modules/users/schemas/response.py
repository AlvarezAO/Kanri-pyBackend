from typing import List
from kanri_app.modules.base_response import StandardResponse
from kanri_app.modules.users.schemas.base import UserRead

class GetAllUsersResponse(StandardResponse):
    usuarios: List[UserRead] = []
    pagina: int = 1
    totalElementos: int = 10
    totalPaginas: int = 1
    
class CreateGetOrUpdateUserResponse(StandardResponse):
    usuario: UserRead = {}
