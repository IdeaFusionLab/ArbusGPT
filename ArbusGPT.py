import os
import openai
import discord
from discord import app_commands, Intents, Client, Interaction

# Configura tus tokens de API
TOKEN_DISCORD = os.environ['TOKEN_DISCORD']
TOKEN_OPENAI = os.environ['TOKEN_OPENAI']

# Define los intents necesarios
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

class ArbusGPTBot(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        openai.api_key = TOKEN_OPENAI

    async def on_ready(self):
        print(f'{bot.user} se ha conectado a Discord!')
        await self.tree.sync(guild=None)

    async def chat_with_gpt3(self, interaction: Interaction, mensaje: str):
        model_engine = "text-davinci-002"
        prompt = f'Conversación en Español:\n\nUsuario: {mensaje}\nIA:'

        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        answer = response.choices[0].text.strip()
        await interaction.response.send_message(answer)

bot = ArbusGPTBot(intents=intents)

@bot.tree.command()
async def arbus(interaction: Interaction, mensaje: str):
    await bot.chat_with_gpt3(interaction, mensaje)

bot.run(TOKEN_DISCORD)
