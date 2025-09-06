import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")  # secret will be set in Render

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

mimic_enabled = False
mimic_user_id = None

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def mimic(ctx, member: discord.Member):
    global mimic_user_id
    mimic_user_id = member.id
    await ctx.send(f"Now set to mimic {member.display_name}.")

@bot.command()
async def mimic_on(ctx):
    global mimic_enabled
    mimic_enabled = True
    await ctx.send("Mimic mode is now ON.")

@bot.command()
async def mimic_off(ctx):
    global mimic_enabled
    mimic_enabled = False
    await ctx.send("Mimic mode is now OFF.")

@bot.event
async def on_message(message):
    global mimic_enabled, mimic_user_id
    if message.author == bot.user:
        return
    if mimic_enabled and mimic_user_id and message.author.id == mimic_user_id:
        await message.channel.send(message.content)
    await bot.process_commands(message)

if TOKEN is None:
    print("❌ ERROR: DISCORD_TOKEN not set in environment variables.")
else:
    bot.run(TOKEN)
