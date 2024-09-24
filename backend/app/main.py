from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_login import LoginManager
from dotenv import load_dotenv
from gtts import gTTS
import os
import tempfile
import base64
from supabase import create_client, Client
from pydantic import BaseModel
from openai import OpenAI
import json

load_dotenv()

# Use environment variables
api_key = os.getenv('AIML_API_KEY')
base_url = os.getenv('AIML_ENDPOINT')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Login manager setup
login_manager = LoginManager(SECRET_KEY, token_url='/api/auth/login')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic models
class Message(BaseModel):
    message: str

class AuthData(BaseModel):
    email: str
    password: str

client = OpenAI(api_key=api_key, base_url=base_url)

# Routes
@app.post("/api/chat")
async def get_bot_response(message: Message):
    try:
        user_response = message.message
        # Use OpenAI to generate a response
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Lyla..."},
                {"role": "user", "content": user_response}
            ],
            temperature=0.7,
            max_tokens=300
        )
        ai_response = response.choices[0].message.content.strip()

        # Store the conversation in Supabase
        supabase.table('conversations').insert({
            'user_message': user_response,
            'ai_response': ai_response
        }).execute()

        # Convert the text response to voice
        tts = gTTS(ai_response, lang='en')
        with tempfile.NamedTemporaryFile() as fp:
            tts.save(fp.name)
            with open(fp.name, "rb") as audio_file:
                encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')

        return {"message": ai_response}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "An internal error occurred"})

@app.post('/api/auth/signup')
async def signup(data: AuthData):
    try:
        response = supabase.auth.sign_up({"email": data.email, "password": data.password})
        return {"success": True, "user": response.user}
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

@app.post('/api/auth/login')
async def login(data: AuthData):
    try:
        response = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
        return {"success": True, "user": response.user, "session": response.session}
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

@app.post('/api/auth/logout')
async def logout():
    try:
        supabase.auth.sign_out()
        return {"success": True}
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

@app.get('/api/dashboard')
async def dashboard():
    return {"message": "Please log in"}

@app.get('/api/account')
async def account():
    return {"message": "Please log in"}

@app.get('/api/settings')
async def settings():
    return {"message": "Please log in"}

@app.get('/api/cityguide')
async def city_guide(city: str):
    cities_file_path = os.path.join(os.path.dirname(__file__), 'cities.json')
    if city:
        with open(cities_file_path, 'r') as json_file:
            cities_data = json.load(json_file)
        city_data = next((c for c in cities_data if c['name'].lower() == city.lower()), None)
        if city_data:
            return city_data
        else:
            raise HTTPException(status_code=404, detail="City not found")
    raise HTTPException(status_code=400, detail="No city specified")

@app.get('/api/cairo.json')
async def cairo_data():
    cairo_file_path = os.path.join(os.path.dirname(__file__), 'cairo.json')
    with open(cairo_file_path, 'r') as json_file:
        cairo_data = json.load(json_file)
    return cairo_data