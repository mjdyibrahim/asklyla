from dotenv import find_dotenv, load_dotenv
import replicate

load_dotenv(find_dotenv())


DEFAULT_SYSTEM_PROMPT = """\
Your name is Lyla, you are a 33 years old Arab female with 3 kids, you are an AI Travel Helper for those visiting Arabia. You are a helpful and friendly assistant 
who provides the best recommendations to travelers for their best flight, accommodations and experiences in Arabia"""


output = replicate.run(
    "replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
    input={"system": DEFAULT_SYSTEM_PROMPT, "prompt": 
           
           """\
                [INST] Hi! [/INST]
                Hello! How are you?
                [INST] What is your name? [/INST]
            
                """
            
           }
)
# The replicate/llama-2-70b-chat model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
for item in output:
    # https://replicate.com/replicate/llama-2-70b-chat/versions/2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1/api#output-schema
    print(item)