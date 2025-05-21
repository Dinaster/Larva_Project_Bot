import os
import asyncio
from telegram.ext import ApplicationBuilder, ContextTypes
from setup_handlers import setup_handlers
from telegram_handler import periodic_analysis

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def periodic_job(context: ContextTypes.DEFAULT_TYPE):
    app = context.application
    await periodic_analysis(app)

async def main():
    print("🚀 Alpha Break Pro 777 bot is starting...", flush=True)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    setup_handlers(app)
    app.job_queue.run_repeating(
        periodic_job,
        interval=3600,
        first=10,
        job_kwargs={"max_instances": 1, "coalesce": True}
    )

    await app.initialize()
    await app.start()
    
    # 👋 Mensaje de vida en el grupo
    await app.bot.send_message(chat_id=int(os.getenv("GROUP_CHAT_ID")), text="👋 Alpha Break Pro 777 is online and watching the market!")

    print("✅ Bot is running...", flush=True)
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
