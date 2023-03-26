import os
import openai
import discord
from discord import app_commands, Intents, Client, Interaction
from dotenv import load_dotenv

# Configura tus tokens de API
load_dotenv()
TOKEN_DISCORD = os.getenv('TOKEN_DISCORD')
TOKEN_OPENAI = os.getenv('TOKEN_OPENAI')

# Define los intents necesarios
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

class ArbusGPTBot(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        openai.api_key = TOKEN_OPENAI
        self.conversaciones = {}

    async def on_ready(self):
        print(f'{bot.user} se ha conectado a Discord!')
        await self.tree.sync(guild=None)

    async def es_administrador(self, miembro):
        return miembro.guild_permissions.administrator

    async def chat_with_gpt3(self, interaction: Interaction, mensaje: str):
        model_engine = "text-davinci-002"
        user_id = interaction.user.id
        miembro = interaction.guild.get_member(user_id)

        if "comando_administrador" in mensaje.lower():
            if not await self.es_administrador(miembro):
                await interaction.response.send_message("No tienes permisos de administrador para ejecutar este comando.")
                return

        if user_id not in self.conversaciones:
            self.conversaciones[user_id] = []

        self.conversaciones[user_id].append(f'Usuario: {mensaje}')

        prompt = 'Conversación en Español:\n\n'
        prompt += '\n'.join(self.conversaciones[user_id]) + '\nIA:'

        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=1.0,
        )

        answer = response.choices[0].text.strip()
        self.conversaciones[user_id].append(f'IA: {answer}')
        await interaction.response.send_message(answer)

bot = ArbusGPTBot(intents=intents)

@bot.tree.command()
async def arbus(interaction: Interaction, mensaje: str):
    await bot.chat_with_gpt3(interaction, mensaje)

bot.run(TOKEN_DISCORD)
