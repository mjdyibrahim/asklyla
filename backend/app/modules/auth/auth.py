from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from supabase import create_client, Client

app = FastAPI()

# Initialize Supabase client
url = "your_supabase_url"
key = "your_supabase_key"
supabase: Client = create_client(url, key)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str
    password: str

@app.post("/signup")
async def signup(user: User):
    # Create user in Supabase
    response = supabase.auth.sign_up(email=user.email, password=user.password)
    if response.get("error"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"]["message"])
    return {"message": "User created successfully"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate user with Supabase
    response = supabase.auth.sign_in(email=form_data.username, password=form_data.password)
    if response.get("error"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": response["access_token"], "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = supabase.auth.get_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    supabase.auth.sign_out(token)
    return {"message": "Logged out successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)