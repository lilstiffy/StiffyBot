from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

# Initialise OpenAI
load_dotenv()
openAiClient = AsyncOpenAI(api_key=os.getenv('OPEN_AI_TOKEN'))

MODEL = "gpt-3.5-turbo"


async def chat_with_gpt(input_text):
    try:
        response = await openAiClient.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": input_text}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Ett fel inträffade: {str(e)}"