from fastapi import APIRouter, Depends
from app.api.v1.football.schema import LeagueFilter, LeaguePlayersList, TeamFilter, TeamPlayerFilter, TeamsDataOut, TeamsPlayersOut
from core.general.schemas import Success, SuccessCreated
from dependencies.user_dependencies import UserAccess, user_db_permitions
from app.api.v1.football.bussiness import (get_players_given_league_code_bs,
                                           get_team_data_given_name_bs,
                                           import_competition_by_league_bs,
                                           get_player_data_given_name_bs)

router = APIRouter()

tags = ["football"]
router.tags = tags


@router.get("/status", response_model=Success)
def get_status():
  return Success()


@router.post("/import-league/{league_code}" , response_model=SuccessCreated)
async def import_league(
    league_code: str,
    user_access: UserAccess = user_db_permitions(permitions=["ADMIN"]),

):
  competition_id =await import_competition_by_league_bs(
    db=user_access.db,
    league=league_code)


  return SuccessCreated(id = competition_id)


@router.get("/league/players" , response_model=LeaguePlayersList)
def get_players_given_league_code(
  args: LeagueFilter = Depends(),
  user_access: UserAccess = user_db_permitions(permitions=[]),
):
  league_players=get_players_given_league_code_bs(db=user_access.db,
                                   league_code=args.league_code, team_name=args.team_name)
  
  return {"data" : league_players}
  

@router.get("/league/team", response_model=TeamsDataOut)
def get_team(
    args: TeamFilter = Depends(),
    user_access: UserAccess = user_db_permitions(permitions=[]),
):
  team_data, players, coaches = get_team_data_given_name_bs(db=user_access.db,
                                                            team_name=args.team_name,
                                                            include_players=args.include_players)

  return TeamsDataOut(
      id=team_data.id,
      name=team_data.name,
      area_name=team_data.area_name,
      tla=team_data.tla,
      short_name=team_data.short_name,
      address=team_data.address,
      players=players,
      coaches=coaches,
  )


@router.get("/league/players-of-a-team", response_model=TeamsPlayersOut)
def get_team_players(
    args: TeamPlayerFilter = Depends(),
    user_access: UserAccess = user_db_permitions(permitions=[]),
):
  players, coaches = get_player_data_given_name_bs(db=user_access.db,
                                                   team_name=args.team_name)

  return TeamsPlayersOut(

      players=players,
      coaches=coaches,
  )
