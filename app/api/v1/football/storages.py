from typing import List
from core.dbsetup import Competition,Teams,Players,Coachs , TeamsCompetition
from .schema import CoachParser, CompetitionParser, CompetitionTeams, PlayerParser, TeamParser 
from sqlalchemy.orm import Session
from sqlalchemy import func

def save_new_team(
  db:Session,
  team :TeamParser,
)->Teams:
  new_team= Teams(
    name = team.name,
    area_name = team.area.area_name,
    tla = team.tla,
    short_name = team.short_name,
    address = team.address,
  )
  db.add(new_team)
  db.flush()
  return new_team

def save_new_player(
  db:Session,
  player :PlayerParser,
  id_team:int,
)->Players:
  
  new_player = Players(
    name = player.name,
    position =player.position ,
    date_of_birth = player.date_of_birth,
    nationality = player.nationality,
    id_team = id_team,
  )
  db.add(new_player)
  db.flush()
  
  return new_player


def save_new_coach(
    db: Session,
    coach: CoachParser,
    id_team: int,
):
  new_coach = Coachs(
      name=coach.name,
      date_of_birth=coach.date_of_birth,
      nationality=coach.nationality,
      id_team=id_team,
  )
  db.add(new_coach)
  db.flush()
  return new_coach


def validate_teams_competition(
  db :Session,
  teams :List[TeamParser],
  competition_id:int,
):
  
  team_names = [team.name for team in teams]
  
  db_teams:List[Teams]=db.query(
    Teams
  ).filter(
    Teams.active == True ,
    Teams.name.in_(team_names)
  ).all()

  finded_teams = set([db_team.name for db_team in db_teams])
  propsed_teams =set(team_names)
  diff_new_teams=list (propsed_teams - finded_teams)
  new_teams = [tm for tm in teams if tm.name in diff_new_teams]
  
  db_teams_competiton:List[Teams]=db.query(
    Teams
  ).join(
    TeamsCompetition,
    TeamsCompetition.id_team == Teams.id,
  ).filter(
    Teams.active == True ,
    TeamsCompetition.id_competition == competition_id,
    Teams.name.in_(team_names),
  ).with_entities(
    Teams.id,
    Teams.name
  ).all()
  
  teams_competion=[db_team_competition.name for db_team_competition in  db_teams_competiton]
  
  new_competitions_teams_names=set(teams_competion)-finded_teams
  new_competitions_teams = [db_team for db_team in db_teams if db_team.name in new_competitions_teams_names]
  return new_teams , new_competitions_teams
  
def save_team_competition(
  db : Session,
  id_team :int ,
  id_competition :int,
  
):
  new_team_competition=TeamsCompetition(
      id_competition=id_competition,
      id_team=id_team,
  )
  db.add(new_team_competition)
  db.flush()
  
  return new_team_competition


def save_new_competition(
    db: Session,
    competition: CompetitionParser,
    teams: CompetitionTeams
):
  
  new_competition = db.query(
    Competition
  ).filter(
    Competition.name == competition.name
  ).first()
  
  if not new_competition:
    
    new_competition = Competition(
        name=competition.name,
        area_name=competition.area.area_name,
        code=competition.code
    )
    db.add(new_competition)
    db.flush()

  new_teams, finded_teams = validate_teams_competition(db=db,
                                                       teams=teams.teams,
                                                       competition_id = new_competition.id)

  for finded_team in finded_teams:
    save_team_competition(
        db=db,
        id_team=finded_team.id,
        id_competition=new_competition.id
    )

  for team in new_teams:
    new_team = save_new_team(db=db,
                             team=team)

    save_team_competition(
        db=db,
        id_team=new_team.id,
        id_competition=new_competition.id
    )

    new_coach = save_new_coach(db=db,
                               coach=team.coach,
                               id_team=new_team.id)
    for player in team.squad:
      new_player = save_new_player(db=db,
                                   player=player,
                                   id_team=new_team.id)

  return new_competition.id



def find_players_given_league_code(
  db:Session,
  league_code:str,
  team_name:str = None,
  partial_name:str = None
)->List[Players]:
  players_league_db = db.query(
    Competition
  ).join(
    TeamsCompetition,
    TeamsCompetition.id_competition == Competition.id
  ).join(
    Teams,
    Teams.id == TeamsCompetition.id_team
  ).join(
    Players,
    Players.id_team == Teams.id
  ).filter(
    Competition.code == league_code,
  )
  
  if team_name:
    players_league_db = players_league_db.filter(
      Teams.name == team_name
    )
  
  if partial_name:
    players_league_db = players_league_db.filter(
      func.lower(Players.name).ilike(f"%{partial_name.lower()}%")

    )
    
  players_league_db:List[Players] = players_league_db.with_entities(
    Players.id,
    Players.name,
    Players.position,
    Players.date_of_birth,
    Players.nationality,
  ).all()
  return players_league_db
  

def find_team_data_given_name_db(
    db: Session,
    team_name: str = None,
    include_players: bool = False,
):
  teams_query :Teams= db.query(
    Teams
  ).filter(
    Teams.name == team_name
  ).first()
  
  players = []
  coaches = []
  if include_players:
    players=db.query(
      Players
    ).filter(
      Players.id_team ==  teams_query.id
    ).all()
    
    
    if len(players) == 0:
      coaches = db.query(
        Coachs
      ).filter(
        Coachs.id_team == teams_query.id
      ).all()
      
  return teams_query , players , coaches
      
def find_player_data_given_name_db(
    db: Session,
    team_name: str ,
    
):
  teams_query :Teams= db.query(
    Teams
  ).filter(
    Teams.name == team_name
  ).first()
  
  players = []
  coaches = []
  
  players=db.query(
    Players
  ).filter(
    Players.id_team ==  teams_query.id
  ).all()
  
  
  if len(players) == 0:
    coaches = db.query(
      Coachs
    ).filter(
      Coachs.id_team == teams_query.id
    ).all()
      
  return  players , coaches
      
    