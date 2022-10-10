import httpx
import os


def get_container_name()->str:
    hostname = os.getenv("HOSTNAME")
    
