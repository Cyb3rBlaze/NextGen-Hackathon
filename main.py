import discord

from openai_utils import generate_response


import requests


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!upload-receipt'):
        image_url = message.attachments[0].url
        await message.channel.send("Processing receipt + " + image_url + "...")

        # TODO
        ocr_url = "http://localhost:5000/genai_hackathon/image_to_text"
        data = {
            "link": message.attachments[0].url,
        }
        raw_data = requests.post(ocr_url, json=data)
        
        # print("Status Code", response.status_code)
        # print("JSON Response ", response.json())

        print(raw_data.json())

        text_info = extract_raw_text(raw_data.json())
        response = await send_to_gpt(text_info)

        await message.channel.send("Processed receipt: " + response + "!")

def extract_raw_text(raw_data):
    final_str = ""
    for i, block in enumerate(raw_data["data"]):
        final_str += block["text"]
        if i != len(raw_data["data"]):
            final_str += " "
    
    return final_str

async def send_to_gpt(text_info):
    prompt = f"""
        on a  receipt sent a character stream {text_info}
        Categorize the expenses among these categories: {'Individual Meals', 'Team Lunch', 'Air Travel', 'Taxi', 'Hotel'} 
        flag as anomaly if expense for the category individual meals, team lunch and hotel exceeds 5 dollars, 30 dollars and 100 dollars
        respectively. Output should be a JSON having transaction date, vendor, vendor type , total and category for the overall receipt. For individual items, list the items, amount, category and anomaly.  Come up with a vendor type based on your knowledge
        """
    
    return await generate_response(prompt)

client.run('')