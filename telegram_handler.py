import os
import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes, Application
from signal_engine import analyze_market
from io import BytesIO

chat_ids = set()

# Leer el ID del grupo desde el entorno
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
if GROUP_CHAT_ID:
    try:
        group_id = int(GROUP_CHAT_ID)
        chat_ids.add(group_id)
        print(f"✅ Loaded GROUP_CHAT_ID from .env: {group_id}")
    except Exception as e:
        print(f"⚠️ Error loading GROUP_CHAT_ID: {e}")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != int(GROUP_CHAT_ID):
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    await update.message.reply_text("✅ Alpha Break Pro 777 is online. Use /check BTC-USD")

# /check <PAIR>
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != int(GROUP_CHAT_ID):
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    if not context.args:
        await update.message.reply_text("⚠️ Please use the command like: /check BTC-USD")
        return

    pair = context.args[0].upper()
    signal, chart = analyze_market(pair)
    
    if signal:
        await update.message.reply_text(signal)
        if chart:
            await update.message.reply_photo(photo=chart)
    else:
        await update.message.reply_text(f"❌ No signal for {pair} right now.")

# /why
async def why(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != int(GROUP_CHAT_ID):
        return
    await update.message.reply_text("📊 This signal is based on:\n- EMA (21)\n- MACD\n- Volume confirmation\n- ATR-based SL/TP.")

# Análisis automático por job_queue
async def periodic_analysis(app: Application):
    pairs = ["BTC-USD", "ETH-USD", "XRP-USD", "SOL-USD"]
    for pair in pairs:
        try:
            signal, chart = analyze_market(pair)
            if signal:
                for cid in chat_ids:
                    await app.bot.send_message(cid, signal)
                    if chart:
                        await app.bot.send_photo(cid, photo=chart)
        except Exception as e:
            print(f"❌ Error sending signal for {pair}: {e}")

