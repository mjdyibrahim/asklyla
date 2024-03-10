from gradio_client import Client

client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")
result = client.predict(
				"Howdy!",	# str in 'Message' Textbox component
				api_name="/chat"
)
print(result)