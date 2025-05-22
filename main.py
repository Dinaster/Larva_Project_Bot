import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from telegram.ext import ContextTypes

import Config
import telegram_handler
from setup_handlers import setup_handlers
from telegram_handler import periodic_analysis

async def periodic_job(context: ContextTypes.DEFAULT_TYPE):
    await periodic_analysis(context.application)


async def main():
    print("🚀 Alpha Break Pro 777 bot is starting...")
    app = ApplicationBuilder().token(Config.BOT_TOKEN).build()
    print("🚀 Alpha Break Pro 777 bot token verification passed successfully...")
    app.add_handler(CommandHandler("start", telegram_handler.start))

    setup_handlers(app)
    print("🚀 Alpha Break Pro 777 bot handlers setted successfully...")

    await app.initialize()
    await app.start()

    # Enviar mensaje de inicio al grupo
    try:
        await app.bot.send_message(
            Config.GROUP_CHAT_ID,
            "👋 Alpha Break Pro 777 is online and watching the market!"
        )
    except Exception as e:
        print(f"⚠️ Error sending startup message: {e}")

    print("✅ Bot is running...")
    try:
        await app.updater.start_polling()
        while True:
            await asyncio.sleep(3600)  # Mantener vivo el bucle
    except (asyncio.CancelledError, KeyboardInterrupt):
        print("\n🔴 Deteniendo bot...")
        await app.stop()


async def start(update: Update, context: CallbackContext):
    print(f"Received /start command in chat: {update.message.chat.id}")  # Debug print
    await update.message.reply_text("¡Hola! Soy 🚀 Alpha Break Pro 777 bot.")


if __name__ == "__main__":
    asyncio.run(main())


