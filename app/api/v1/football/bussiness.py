

from fastapi import HTTPException
from app.api.v1.football.services import competitions_by_league , teams_by_league
import asyncio
from .schema import CompetitionParser, CompetitionTeams
from sqlalchemy.orm import Session
from .storages import find_player_data_given_name_db, find_players_given_league_code, find_team_data_given_name_db, save_new_competition
from commons.clients.football_client import async_client
async def import_competition_by_league_bs(
  db : Session,
  league:str,
):
  to_execute = [competitions_by_league(league=league),
                teams_by_league(league=league)]
  
  competitions , teams = await async_client.gather(*to_execute)
  
  parsed_competition=CompetitionParser(**competitions)
  parsed_teams = CompetitionTeams(**teams)

  competition_id = save_new_competition(db=db,
                       competition=parsed_competition,
                       teams=parsed_teams)
  db.commit()
  return competition_id
  
  
def get_players_given_league_code_bs(
  db:Session,
  league_code :str,
  team_name:str = None
):
  
  league_players=find_players_given_league_code(db=db , league_code=league_code , team_name=team_name)
  
  if len(league_players)==0:
    raise HTTPException(status_code=404 , detail=f"The league code {league_code} doesn't exist")
  return league_players

def get_team_data_given_name_bs(
  db:Session,
  team_name:str,
  include_players:bool=False,
):
  team_data , players , coaches=find_team_data_given_name_db(
    db=db,
    team_name=team_name,
    include_players=include_players
  )
  
  return team_data , players , coaches


def get_player_data_given_name_bs(
    db: Session,
    team_name: str,
):
    players, coaches = find_player_data_given_name_db(
        db=db,
        team_name=team_name,
    )
    return players, coaches
