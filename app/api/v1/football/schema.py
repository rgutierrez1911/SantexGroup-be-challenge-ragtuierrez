from typing import List
from fastapi import Query
from pydantic import Field
from core.general.schemas import OrmModel
from dataclasses import dataclass

class _areaParser(OrmModel):
    area_name:str = Field(... , alias="name")
  
  
class CompetitionParser(OrmModel):  
  name:str
  area:_areaParser
  code :str

    
class CoachParser(OrmModel):
  name:str =None
  date_of_birth:str = Field(None , alias="dateOfBirth")
  nationality:str = None
  
class PlayerParser(OrmModel):
  name:str
  position:str = None
  date_of_birth:str = Field(None , alias="dateOfBirth")
  nationality:str = None

class TeamParser(OrmModel):
  name :str 
  area:_areaParser
  tla:str = None
  short_name:str = Field(None , alias="shortName")
  address:str = None
  
  coach : CoachParser = None
  
  squad : List[PlayerParser] = []
  
class CompetitionTeams(OrmModel):
  teams:List[TeamParser] = []
  
  
@dataclass
class LeagueFilter:
  league_code : str = Query(...)
  team_name : str = Query(None)

class LeaguePlayer(OrmModel):
  id:int
  name : str
  position : str = None
  date_of_birth:str = None
  nationality:str = None
  
class LeagueCoaches(OrmModel):
  id:int = None
  name:str =None
  date_of_birth:str = None
  nationality:str = None
  
class LeaguePlayersList(OrmModel):
  data :List[LeaguePlayer] = []
  
  
@dataclass
class TeamFilter:
  team_name : str = Query(...)
  include_players : bool = Query(False)



class TeamsPlayersOut(OrmModel):
  
  players: List[LeaguePlayer] = []
  coaches : List[LeagueCoaches] = []

class TeamsDataOut(OrmModel):
  
  id:int
  name:str
  area_name:str = None
  tla:str = None
  short_name:str = None
  address:str = None
  
  players: List[LeaguePlayer] = []
  coaches : List[LeagueCoaches] = []
  
  

  
@dataclass
class TeamPlayerFilter:
  team_name : str = Query(...)

