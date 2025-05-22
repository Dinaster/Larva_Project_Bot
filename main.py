import asyncio

from telegram.ext import ApplicationBuilder

import Config
from setup_handlers import setup_handlers


async def main():
    print("🚀 Iniciando bot...")

    app = ApplicationBuilder().token(Config.BOT_TOKEN).build()
    setup_handlers(app)

    try:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        print("✅ Bot en ejecución")
        await asyncio.Future()  # Mantiene el bot activo indefinidamente

    except KeyboardInterrupt:
        print("\n🔴 Deteniendo bot...")
        await app.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🔴 Bot detenido manualmente")


