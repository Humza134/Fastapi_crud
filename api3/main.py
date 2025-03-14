from fastapi import FastAPI,Depends,HTTPException,Query
from sqlmodel import SQLModel, Field,create_engine,Session,select
from os import getenv
from dotenv import find_dotenv,load_dotenv
from typing import Annotated
from model import Hero, HeroCreate, HeroResponse, HeroResponseWithTeam, HeroUpdate, Team, TeamCreate, TeamResponse, TeamUpdate

_:bool = load_dotenv(find_dotenv())


DB_KEY = getenv("POSTGRESS_URL", "")
engine = create_engine(DB_KEY, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

app : FastAPI = FastAPI()

#DB dependency injection

def get_db():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
async def root():
    return {"message:" "Hello World"}

# get all heroes

@app.get("/heroes", response_model=list[Hero])
def get_heroes(session:Annotated[Session, Depends(get_db)], offset:int = Query(default=0, le=4), limit:int = Query(default=2, le=4)):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes
    
# create heroes
    
@app.post("/heroes", response_model=HeroResponse)
def create_hero(hero:HeroCreate, db:Annotated[Session, Depends(get_db)]):
    # print("data from client", hero)
    hero_to_insert = Hero.model_validate(hero)
    # print("Data after validation", hero_to_insert)
    db.add(hero_to_insert)
    db.commit()
    db.refresh(hero_to_insert)
    return hero_to_insert

# get hero by id

@app.get("/heroes/{hero_id}", response_model=HeroResponseWithTeam)
def get_hero_by_id(hero_id:int, db:Annotated[Session, Depends(get_db)]):
    hero = db.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    print(hero.team)
    return hero

# update hero

@app.patch("/heroes{hero_id}", response_model=HeroResponse)
def update_hero(hero_id:int, hero_data:HeroUpdate, db:Annotated[Session, Depends(get_db)]):
    # get hero
    hero = db.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    print("HERO IN DB", hero)
    print("DATA FROM CLIENT", hero_data)

    hero_dict_data = hero_data.model_dump(exclude_unset=True)
    print("HERO_DICT_DATA", hero_dict_data)

    for key,value in hero_dict_data.items():
        setattr(hero, key, value)

    print("AFTER UPDATE", hero)

    db.add(hero)
    db.commit()
    db.refresh(hero)
    return hero

# delete hero

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, db:Annotated[Session, Depends(get_db)]):
    #get hero
    hero = db.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    db.delete(hero)
    db.commit()
    return {"message": "Hero Deleted Successfully"} 

# Get all teams

@app.get("/teams", response_model=list[Team])
def get_teams(db:Annotated[Session, Depends(get_db)], offset:int = Query(default=0, le=4), limit:int = Query(default=2, le=4)):
    teams = db.exec(select(Team).offset(offset).limit(limit)).all()
    return teams

# Get single team

@app.get("/teams/{team_id}", response_model=TeamResponse)
def get_team_by_id(team_id:int, db:Annotated[Session, Depends(get_db)]):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# Create Team

@app.post("/teams", response_model=TeamResponse)
def create_team(team:TeamCreate, db:Annotated[Session, Depends(get_db)]):
    team_to_insert = Team.model_validate(team)
    db.add(team_to_insert)
    db.commit()
    db.refresh(team_to_insert)
    return team_to_insert

# Update Team

@app.patch("/teams/{team_id}", response_model=TeamResponse)
def update_team(team_id:int, team_data:TeamUpdate, db:Annotated[Session, Depends(get_db)]):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_dict_data = team_data.model_dump(exclude_unset=True)
    for key,value in team_dict_data.items():
        setattr(team, key, value)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team

# Delete Team

@app.delete("/teams/{team_id}")
def delete_team(team_id: int, session:Annotated[Session, Depends(get_db)]):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"message": "Team Deleted Successfully"}