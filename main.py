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

    # Cargar comandos como /start, /check, /why
    setup_handlers(app)

    # Activar job scheduler para señales cada hora
    app.job_queue.run_repeating(
        periodic_job,
        interval=3600,
        first=10,
        job_kwargs={"max_instances": 1, "coalesce": True}
    )

    # Inicializar y lanzar bot
    await app.initialize()
    await app.start()
    print("✅ Bot is running...", flush=True)

    # Necesario para que lea comandos tipo /start, /check
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
