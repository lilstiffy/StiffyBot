import json

# Load cringe words
with open('cringewords.json', 'r') as file:
    cringeData = json.load(file)

 # Function returning a boolean in case cringe has been posted
    def has_posted_cringe(input_string, string_array):
        return any(element in input_string for element in string_array)

class EventHandler():
    def __init__(self, client):
        self.client = client
        
    # -- EVENTS --
    async def m_on_message(self, message):
        if message.author == self.client.user:
            return
        
        if has_posted_cringe(input_string=message.content, string_array=cringeData):
            await message.channel.send(content=':rotating_light: Du postade precis cringe :rotating_light:', mention_author=True)

    async def m_on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Välkommen {member.name} till servern!!'
        )
        