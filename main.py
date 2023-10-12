import uuid
from fastapi import FastAPI, Body, status, Query
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()


class Spot(BaseModel):
    name: str
    price: str
    id: str(uuid.uuid4())


class User(BaseModel):
    name: str
    contact: str
    id: str(uuid.uuid4())


class New(BaseModel):
    name: str
    description: str
    id: str(uuid.uuid4())


# условная база данных - набор объектов Spots, Users
spots = [Spot["TomArt", 380], Spot["BobArt", 420], Spot["SamArt", 280]]
users = [User("Tom", 4), User("Bob", 5), User("Sam", 5)]
news = [New("new", "about new")]


def find_spot(id):
    for spot in spots:
        if spot.id == id:
            return spot
    return None


@app.get("/spots")
async def read_spots():
    return spots


@app.get("/spots/{spot_id}")
async def read_spots(spot_id: str, name: str, price: str):
    spot = {"spot_id": spot_id,
            "name": name,
            "price": price}
    return spot
# на вызов контактов будет дергатся данный рест, на фронт отображаться только - контакты

@app.post("/spots/")
async def create_spot(spot: Spot):
    return spot


@app.put("/spots/{spot_id}", response_model=Spot)
async def update_spot(spot_id: str, spot: Spot):
    update_spot_encoded = jsonable_encoder(spot)
    spots[spot_id] = update_spot_encoded
    return update_spot_encoded


@app.get("/users")
async def read_users():
    return users


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/search")
async def read_users():
    return users
# медод search(поиска) должен работать по словам из названия, описания, ключевым словам(??), городу

@app.get("/author")
async def root():
    return {"message": "about us"}


@app.get("/news")
async def read_new(new_id: str):
    return news


@app.get("/news/{new_id}")
async def read_new(new_id: str, name: str, description: str):
    new = {"new_id": new_id,
           "name": name,
           "description": description}
    return new
