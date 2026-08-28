import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import INPUT_CHANNEL_ID, LOG_CHANNEL_ID, ADD_ROLE_ID, REMOVE_ROLE_ID
from utils import generate_id, build_nickname

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN غير موجود في ملف .env")

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
    # تجاهل رسائل البوتات
    if message.author.bot:
        return

    # النظام يعمل فقط في الروم المحدد
    if message.channel.id != INPUT_CHANNEL_ID:
        return

    roblox_name = message.content.strip()

    if not roblox_name:
        await message.delete()
        return

    # حذف رسالة المستخدم
    try:
        await message.delete()
    except discord.HTTPException:
        pass

    member = message.author
    guild = message.guild

    if guild is None:
        return

    # التأكد من أن الاسم ليس طويلاً جداً
    if len(roblox_name) > 20:
        try:
            await member.send(
                "❌ اسم Roblox طويل جداً. أرسل اسم Roblox بحد أقصى 20 حرفاً."
            )
        except discord.Forbidden:
            pass
        return

    random_id = generate_id()
    new_nickname = build_nickname(roblox_name, random_id)

    # تغيير الاسم
    try:
        await member.edit(nick=new_nickname, reason="تفعيل حساب Roblox")
    except discord.Forbidden:
        try:
            await member.send(
                "❌ لم أستطع تغيير اسمك. تأكد أن رتبة البوت أعلى من رتبتك وأن لديه صلاحية Manage Nicknames."
            )
        except discord.Forbidden:
            pass
        return
    except discord.HTTPException:
        try:
            await member.send("❌ حدث خطأ أثناء تغيير اسمك، حاول مرة أخرى.")
        except discord.Forbidden:
            pass
        return

    add_role = guild.get_role(ADD_ROLE_ID)
    remove_role = guild.get_role(REMOVE_ROLE_ID)

    # إعطاء الرتبة المطلوبة
    if add_role:
        try:
            await member.add_roles(add_role, reason="تفعيل حساب Roblox")
        except discord.Forbidden:
            pass

    # إزالة الرتبة القديمة
    if remove_role:
        try:
            await member.remove_roles(remove_role, reason="تفعيل حساب Roblox")
        except discord.Forbidden:
            pass

    # إرسال آخر هوية إلى روم السجل
    log_channel = guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="تفعيل هوية Roblox",
            description=f"تم تفعيل {member.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="اسم Roblox", value=roblox_name, inline=False)
        embed.add_field(name="الهوية الجديدة", value=new_nickname, inline=False)
        embed.add_field(name="العضو", value=f"{member} (`{member.id}`)", inline=False)
        await log_channel.send(embed=embed)

    # رسالة خاصة للعضو
    try:
        await member.send(
            f"✅ **تم تفعيلك بنجاح!**\n\n"
            f"🎮 **اسم Roblox:** `{roblox_name}`\n"
            f"🆔 **الإيدي:** `{random_id}`\n"
            f"🏷️ **اسمك الجديد:** `{new_nickname}`\n\n"
            f"تم إعطاؤك الرتبة المطلوبة وإزالة الرتبة القديمة."
        )
    except discord.Forbidden:
        # الخاص مغلق، فلا نوقف عملية التفعيل
        pass

    # حذف بقية رسائل الروم بعد المعالجة.
    # يحتاج البوت Manage Messages، وللرسائل الأقدم من 14 يوماً
    # Discord لا يسمح بالـ bulk delete، لذلك نحذفها واحدة واحدة.
    try:
        await message.channel.purge(limit=100)
    except discord.Forbidden:
        pass
    except discord.HTTPException:
        pass

    await bot.process_commands(message)


bot.run(TOKEN)
