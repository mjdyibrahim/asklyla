import replicate
from dotenv import load_dotenv

load_dotenv()

user_question = input("What do you want to ask the API? ")

output_generator = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                           input={"prompt": f"{user_question}",
                                  "temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1}
                        )

# Convert the generator output to a list
output_list = list(output_generator)

# Join the strings in the list to create a paragraph
output_paragraph = ''.join(output_list)

# Print the paragraph
print(output_paragraph)