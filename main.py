import os
from telegram.ext import ApplicationBuilder, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))

async def start_hello_world(app):
    await app.bot.send_message(chat_id=GROUP_CHAT_ID, text="👋 Hello World from your bot!")

async def main():
    print("🚀 Bot is starting...", flush=True)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    await app.initialize()
    await app.start()
    await start_hello_world(app)
    print("✅ Message sent to group!", flush=True)
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
