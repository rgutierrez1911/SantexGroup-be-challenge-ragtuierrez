from typing import Tuple

from core.general.schemas import DbUser
from core.extensions import Session

UserSession = Tuple[DbUser, Session] 


