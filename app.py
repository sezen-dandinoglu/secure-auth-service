from fastapi import FastAPI, HTTPException, status, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from security import hash_password, verify_password
from database import create_users_table, insert_user, get_user_by_email, get_user_by_id
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from models import Base

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

create_users_table()

app = FastAPI()

bearer_scheme = HTTPBearer()

@app.post("/register", response_model=UserResponse)
def register(user : UserCreate):
    email = user.email
    password = user.password
    select_user_result_dict= get_user_by_email(email)
    
    if select_user_result_dict is None:
        hashed_password = hash_password(password)
        
        insert_user(email, hashed_password)

        return get_user_by_email(email)
    else:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "This user is already registered."
        )


@app.post("/login", response_model=TokenResponse)
def user_login(login : UserLogin):
    email = login.email
    password= login.password
    select_user_result_dict= get_user_by_email(email)

    if select_user_result_dict is not None:
        stored_hash = select_user_result_dict["hashed_password"]

        is_user_exist = verify_password(password, stored_hash)

        if is_user_exist:
            user_id = select_user_result_dict["id"]
            token_data = {"sub": str(user_id)} 
            access_token = create_access_token(token_data)
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        else:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid email or password."
            )
    else:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid email or password."
            )


@app.get("/me", response_model=UserResponse)
def get_me(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials

    verify_data = verify_token(token)

    if verify_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )

    user_dict = get_user_by_id(int(verify_data["sub"]))

    if user_dict is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )

    return user_dict


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError as e:
        return None

