from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Creamos el algoritmo de encriptación 
ALGORITHM = "HS256"
# Ponemos duración del access token para cuando el post devuelva el access token
ACCESS_TOKEN_DURATION = 1
# Creamos semilla para la encriptacion utilizando "openssl rand -hex 32" en una terminal
SECRET = "869e23704917f2cd959c6206ddc85c072f70ecb5c37f1eed8ae2842fa827b1f4"

# Creamos contexto de encriptación. Cuando verifiquemos la contraseña ingresada con la encriptada en la base de datos con crypt.verify usaremos este esquema
crypt = CryptContext(schemes="bcrypt")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "$2a$12$K6LK9wjDc/6FDmTwyUF1UuYFbxaR0DA06QjtTR1Lmzrb53hR/LFlK" # Encryptamos la contraseña para el ejemplo en bcrypt generator (pass:123456)
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "$2a$12$cL.K0TxKEJ11xaL/nz0houuryUhaNMZBPAuHbPJvTIiK.E.cP3Y2u" # Encryptamos la contraseña para el ejemplo en bcrypt generator (pass:654321)
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

@router.post("/login/jwt")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username) 
    if not user_db: 
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)     

    if not crypt.verify(form.password, user.password): # Verificamos la contraseña en el contexto de encriptación configurado
        raise HTTPException(status_code=400, detail="La contraseña es incorrecta")
    
    # Creamos variable para controlar el tiempo de expiración del token (hora actual + duración del token configurada)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)

    # Creamos el access token que va a contener el tiempo de expiración y el usuario
    access_token = {"sub": user.username, "exp": expire}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm = ALGORITHM), "token_type": "bearer"} 


# Ya hicimos autenticación, ahora implementamos una operación que nos dé datos de usuario
# con dependencia a si estamos autenticados pero, a diferencia de basic_auth_users, ahora hay que
# desencriptar el token


async def auth_user(token: str = Depends(oauth2)): 

    exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Credenciales de autenticación inválidas",
                    headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub") # Decodificamos el token encriptado y guardamos el nombre de usuario
        if username is None: # Descartamos la posibilidad de que esté vacío
            raise exception
    
    except JWTError:
        raise exception

    return search_user(username) # Devolvemos el username para chequear en current_user si está activo
    
async def current_user(user: User = Depends(auth_user)): # Verificamos si está activo, pero antes decodificamos el token con la dependencia en auth_user
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")

    return user

@router.get("/users/me/jwt")
async def me(user: User = Depends(current_user)):
    return user