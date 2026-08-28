import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import INPUT_CHANNEL_ID, LOG_CHANNEL_ID, ADD_ROLE_ID, REMOVE_ROLE_ID
from utils import generate_id, build_nickname

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PORT = int(os.getenv("PORT", 10000))

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN غير موجود في Environment Variables")


# Web Server لـ Render
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is online!")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def log_message(self, format, *args):
        return


def run_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()


threading.Thread(target=run_server, daemon=True).start()


intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"تم تشغيل البوت: {bot.user} | ID: {bot.user.id}")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.channel.id != INPUT_CHANNEL_ID:
        return

    roblox_name = message.content.strip()

    if not roblox_name:
        return

    if len(roblox_name) > 20:
        try:
            await message.author.send(
                "❌ اسم Roblox طويل جداً. الحد الأقصى 20 حرف."
            )
        except discord.Forbidden:
            pass
        return

    # حذف رسالة العضو التي أرسلها للتفعيل فقط
    try:
        await message.delete()
    except discord.HTTPException:
        pass

    member = message.author
    guild = message.guild

    random_id = generate_id()
    new_nickname = build_nickname(roblox_name, random_id)

    # تغيير الاسم
    try:
        await member.edit(
            nick=new_nickname,
            reason="تفعيل حساب Roblox"
        )
    except discord.Forbidden:
        try:
            await member.send(
                "❌ لم أستطع تغيير اسمك. تأكد أن رتبة البوت أعلى من رتبتك."
            )
        except discord.Forbidden:
            pass
        return

    # الرتب
    add_role = guild.get_role(ADD_ROLE_ID)
    remove_role = guild.get_role(REMOVE_ROLE_ID)

    if add_role:
        try:
            await member.add_roles(
                add_role,
                reason="تفعيل حساب Roblox"
            )
        except discord.Forbidden:
            pass

    if remove_role:
        try:
            await member.remove_roles(
                remove_role,
                reason="تفعيل حساب Roblox"
            )
        except discord.Forbidden:
            pass

    # روم آخر هوية
    log_channel = guild.get_channel(LOG_CHANNEL_ID)

    if log_channel:
        await log_channel.send(
            f"**تم تفعيل هوية جديدة**\n"
            f"👤 العضو: {member.mention}\n"
            f"🎮 Roblox: `{roblox_name}`\n"
            f"🆔 ID: `{random_id}`\n"
            f"🏷️ الاسم الجديد: `{new_nickname}`"
        )

    # الخاص
    try:
        await member.send(
            f"✅ **تم تفعيلك بنجاح!**\n\n"
            f"🎮 **اسم Roblox:** `{roblox_name}`\n"
            f"🆔 **الإيدي:** `{random_id}`\n"
            f"🏷️ **اسمك الجديد:** `{new_nickname}`\n\n"
            f"تم إعطاؤك الرتبة وإزالة الرتبة القديمة."
        )
    except discord.Forbidden:
        pass


bot.run(TOKEN)
