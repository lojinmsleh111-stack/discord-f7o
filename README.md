# Roblox Discord Activation Bot

بوت Discord مكتوب بـ Python باستخدام discord.py.

## الوظيفة

عندما يكتب العضو اسم Roblox في الروم المحدد:

1. يحذف رسالة العضو.
2. ينشئ ID عشوائي من 4 أرقام.
3. يغيّر اسم العضو إلى:
   `WE | اسم Roblox | 1234`
4. يعطيه الرتبة المحددة.
5. يشيل منه الرتبة القديمة.
6. يرسل سجل في روم الهويات.
7. يرسل للعضو رسالة خاصة فيها:
   - اسم Roblox
   - الإيدي
   - الاسم الجديد
8. يحاول حذف رسائل الروم بعد التفعيل.

## التشغيل

ثبت المكتبات:

```bash
pip install -r requirements.txt
```

أنشئ ملف اسمه `.env` وانسخ داخله:

```env
DISCORD_TOKEN=توكن_البوت
```

ثم شغل:

```bash
python main.py
```

## صلاحيات البوت

يحتاج البوت على الأقل إلى:

- Manage Nicknames
- Manage Roles
- Manage Messages
- Read Message History
- Send Messages
- Embed Links

ويجب أن تكون **رتبة البوت أعلى من الرتبة التي سيعطيها/يزيلها**.

## مهم جداً

فعّل من Discord Developer Portal:

**Message Content Intent**

وكذلك:

**Server Members Intent**

ولا تضع توكن البوت داخل GitHub.
