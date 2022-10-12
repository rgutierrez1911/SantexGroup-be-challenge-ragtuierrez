from typing import List
from core.exceptions.auth import PermitionException
from core.general.schemas import UserAccess


from core.security import get_current_active_user
from commons.storage import get_user_permitions
from fastapi import Depends


def user_token_data(
) -> UserAccess:
  dependency = Depends(dependency=get_current_active_user)
  return dependency


def user_db_permitions(
    permitions: List[str] = [],
):
  def get_permitions_dependency(dependency: UserAccess = Depends(dependency=get_current_active_user)):

    permitions_object = get_user_permitions(session=dependency.db,
                                            id_usuario=dependency.user.id)
    
    only_permitions = permitions_object["complete_permitions"]

    if not permitions:
      dependency.permitions = []
      dependency.selected_permition = None
      return dependency

    for permition in permitions:
      if permition in only_permitions:
        dependency.permitions = permitions
        dependency.selected_permition = permition
        return dependency
    raise PermitionException(status_code=401, permitions=permition)
    
  return Depends(get_permitions_dependency)

