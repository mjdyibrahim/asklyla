from openai import OpenAI
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_login import LoginManager, current_user, login_required
from dotenv import load_dotenv
from gtts import gTTS
import os
import tempfile
import base64
from supabase import create_client, Client
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder='../../frontend/.output/public')
    CORS(app)  # Add this line to enable CORS
    
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        # This function should return a user object or None
        # Implement this based on your user model and database
        pass
    # Load environment variables
    load_dotenv()

    # Initialize the OpenAI client
    client = OpenAI(
        api_key=os.getenv("AIML_API_KEY"),
        base_url="https://api.aimlapi.com",
    )

    # Initialize Supabase client
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )

    # List to store previous responses
    previous_responses = []

    # Home page route
    @app.route("/")
    def home():
        return render_template("splash.html")

    # Bot response route
    @app.route("/api/chat", methods=["POST"])
    def get_bot_response():
        try:
            user_response = request.json['message']
            
            # Use OpenAI to generate a response
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itinerary based on their preferences and personality, objectives and current life circumstances and help them book all the services they need."},
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
            
            return jsonify({"message": ai_response, "voice": encoded_string})
        
        except Exception as e:
            app.logger.error(f"An error occurred: {str(e)}")
            return jsonify({"error": "An internal error occurred"}), 500

    # New authentication routes
    @app.route('/auth/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            return jsonify({"success": True, "user": response.user})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/auth/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            return jsonify({"success": True, "user": response.user, "session": response.session})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route('/auth/logout', methods=['POST'])
    def logout():
        try:
            supabase.auth.sign_out()
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/account')
    @login_required
    def account():
        return render_template('account.html')
    
    @app.route('/settings')
    @login_required
    def settings():
        return render_template('settings.html')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path.startswith('api/'):
            # This is an API call, so we should return a 404 if it's not found
            return jsonify({"error": "Not found"}), 404
        else:
            # For all other routes, serve the Nuxt.js app
            return send_from_directory(app.static_folder, 'index.html')

    return app

# Keep this if you're using it to run the app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)