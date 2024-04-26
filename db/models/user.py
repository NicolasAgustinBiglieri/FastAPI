from pydantic import BaseModel

class User(BaseModel):
    # El id en MongoDB es un string, y lo vamos a pasar sin id desde el post, por lo cual le decimos que el campo puede estar vacío u opcional
    id: str | None
    username: str
    email: str

