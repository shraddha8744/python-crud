from pydantic import BaseModel

class userSchema(BaseModel):
    id:int
    title:str
    body:str

    class config():
        orm_mode=True