from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from db_config import SessionLocal
import model

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PersonBase(BaseModel):
    firstname: str
    lastname: str
    isMale: bool

class PersonCreate(PersonBase):
    pass

class PersonResponse(PersonBase):
    id: int

class PersonUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    isMale: bool | None = None

@app.get("/", response_model=List[PersonResponse], status_code=status.HTTP_200_OK)
def get_all_persons(db: Session = Depends(get_db)):
    return db.query(model.Person).all()

@app.get("/person/{person_id}", response_model=PersonResponse, status_code=status.HTTP_200_OK)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(model.Person).filter(model.Person.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person

@app.post("/addperson", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
def add_person(person: PersonCreate, db: Session = Depends(get_db)):
    new_person = model.Person(**person.dict())
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

@app.put("/updateperson/{person_id}", response_model=PersonResponse, status_code=status.HTTP_200_OK)
def update_person(person_id: int, person: PersonUpdate, db: Session = Depends(get_db)):
    existing_person = db.query(model.Person).filter(model.Person.id == person_id).first()
    if existing_person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    
    for key, value in person.model_dump().items():
        setattr(existing_person, key, value)

    db.commit()
    db.refresh(existing_person)
    return existing_person

@app.delete("/deleteperson/{person_id}", response_model=dict)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    existing_person = db.query(model.Person).filter(model.Person.id == person_id).first()
    if existing_person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    
    db.delete(existing_person)
    db.commit()
    return {"message": "Person deleted"}
