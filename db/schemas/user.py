# Esto es para transformar el json que recibimos del find_one en un objeto de tipo User
def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]}


# Esta función es para devolver todos los usuarios (aprovechando la funcion anterior, devolvemos cada user tipo User)
def users_schema(users) -> list:
    return [user_schema(user) for user in users]
