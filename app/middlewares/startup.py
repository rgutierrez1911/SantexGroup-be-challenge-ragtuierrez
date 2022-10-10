import subprocess as sp
import time 
import random
from core.config import WAIT

ARGS = ["alembic" , "upgrade" , "head"]
ALEMBIC_VERSION = "ba82b45d8177"


def startup():
    
    if WAIT == "TRUE":

        delay = random.randint(5, 10)
        time.sleep(5 + delay)
    alembic_process = sp.Popen(ARGS, stdout=sp.PIPE, stderr=sp.PIPE)

    response, error = alembic_process.communicate()
    print(response.decode())
    print(error.decode())
