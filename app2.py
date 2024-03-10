from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import replicate
import os

app = Flask(__name__)

load_dotenv()

REPLICATE_API_TOKEN="r8_WqG4Y528qeKhXbVUcYeSvE41qqkkkn618Say4"

app.secret_key = os.environ.get("SECRET_KEY")

# Replicate Credentials
replicate_api = os.environ.get("REPLICATE_API_TOKEN")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def get_bot_response():
    # Get user message and store it in user_response
    user_response = request.json['message']

    # Initialize conversation history list in session
    if "conversation" not in session:
        session["conversation"] = []

    conversation = session["conversation"]

    ai_response = get_ai_response(user_response)

    # Append user and assistant messages to conversation history
    conversation.append({"role": "user", "content": user_response})
    conversation.append({"role": "assistant", "content": ai_response})

    return jsonify({"message": ai_response})

def get_ai_response(user_response):
    string_dialogue = """You are Lyla, a 33 Arab female Travel Assistant with the mission to help user to find their optimal travel flights, 
                            accommodations and experiences in the Arab world\\n"""
    for message in session["conversation"]:
        if message["role"] == "user":
            string_dialogue += "User: " + message["content"] + "\\n\\n"
        else:
            string_dialogue += "Assistant: " + message["content"] + "\\n\\n"
    llm_response = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                           input={"prompt": f"{string_dialogue} {user_response} Assistant: ",
                                  "temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1})
    
    save_llm_response_to_file(llm_response)

    full_llm_response = ""
    for message in llm_response:
        full_llm_response += message

    output = full_llm_response

    save_output_response_to_file(output)
    return output

def save_llm_response_to_file(llm_response):
    with open("llm_response.txt", "a") as file:
        file.write(llm_response)

def save_output_response_to_file(output):
    with open("output_list.txt", "a") as file:
        file.write(output)

if __name__ == "__main__":
    app.run()
