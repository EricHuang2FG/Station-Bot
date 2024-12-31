import os, orbital_track, discord

async def send_message(message, user_message):
    try:
        response = orbital_track.handleResponse(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)

def runDiscordBot():
    TOKEN = os.environ['TOKEN']
    intents = discord.Intents.all()
    client = discord.Client(intents = intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
    
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"\n{username} said: '{user_message}' in {channel}")
        
        await send_message(message, user_message)
    
    client.run(TOKEN)
