import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

vertexai.init(project="assistantgpt-383803", location="us-central1")
chat_model = ChatModel.from_pretrained("chat-bison@001")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 256,
    "top_p": 0.8,
    "top_k": 40
}
chat = chat_model.start_chat(
    context="""Your name is Lyla, you are a 33 year old Arab who helps visitors to the Middle East have the best experience. You are an AI Travel Assistant providing access to accommodation, transportation and experiences in the middle east""",
)
response = chat.send_message("""Hello, what\'s your name?""", **parameters)
print(f"Response from Model: {response.text}")
response = chat.send_message("""I want to go to Cairo, what should I take into consideration?""", **parameters)
print(f"Response from Model: {response.text}")
response = chat.send_message("""Can you help me book an accommodation in Cairo?""", **parameters)
print(f"Response from Model: {response.text}")