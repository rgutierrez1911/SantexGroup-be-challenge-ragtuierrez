### Santex Back-end Developer Hiring Test ###
Rodrigo Gutierrez

Framework Used:
- FastApi : Due to be able to use a async FW with improved performance and extensability.Easy to use and easy to deploy using uvicorn
- SqlAlchemy : ORM used to communicate with the Database (Postgress) and it has improved documentation over other ORM
- Alembic : For versioning the Db models schemas and auto-generating the migrations.Easily extensible with some monkeypatching



to set current SSH key 
git config --local core.sshCommand "ssh -i /x/keys/id_rsa"

TO RUN THE PROJECT
Install docker locally 
Windows:
https://docs.docker.com/desktop/install/windows-install/
Ubuntu:
https://docs.docker.com/desktop/install/linux-install/

### Docker usage ###
### BUILD ####
docker-compose build
### BUILD ####

### RUN ###
docker-compose up -d
### RUN ###


default User : admin
default Password : admin

BASE DOCUMENTATION 
- http://localhost:8000/swagger/docs#/

PRODUCT DOCUMENTATION
- http://localhost:8000/football/swagger/docs#



