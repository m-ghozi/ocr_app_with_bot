import discord
from discord.ext import commands

# GANTI DENGAN TOKEN KAMU
TOKEN = "token"

# GANTI DENGAN CHANNEL ID KAMU
CHANNEL_ID = 123  # Ganti dengan ID channel kamu

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot login sebagai {bot.user}")

    # Test kirim pesan
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("🤖 Bot OCR siap digunakan!")
        print(f"✅ Pesan terkirim ke channel: {channel.name}")
    else:
        print("❌ Channel tidak ditemukan! Cek CHANNEL_ID kamu")


bot.run(TOKEN)
