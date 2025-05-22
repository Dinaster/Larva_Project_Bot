import os
import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes, Application

import Config
from analytics.EmaAnalyzer import EMAAnalyzer
from analytics.MacdAnalyzer import MACDAnalyzer
from signal_engine import analyze_market
from io import BytesIO
from utils.data_fetcher import get_market_data  # Ejemplo de función para obtener datos

chat_ids = set()

if Config.GROUP_CHAT_ID:
    try:
        group_id = int(Config.GROUP_CHAT_ID)
        chat_ids.add(group_id)
        print(f"✅ Loaded GROUP_CHAT_ID from .env: {group_id}")
    except Exception as e:
        print(f"⚠️ Error loading GROUP_CHAT_ID: {e}")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Formato: /analyze <PAR> (Ej: BTC-USD)")
        return

    pair = context.args[0].upper().replace("/", "-")
    await update.message.reply_text(f"📥 Obteniendo datos para {pair}...")

    try:
        data = await get_market_data(pair)
        if data.empty:
            await update.message.reply_text("❌ Par no válido o sin datos")
            return

        # Análisis MACD (CORRECTO)
        macd_analyzer = MACDAnalyzer(pair, data)
        macd_analyzer.calculate_indicators()  # <--- ¡Añade esto!
        macd_signal = macd_analyzer.generate_signal()
        macd_chart = macd_analyzer.plot_chart()

        # Análisis EMA
        ema_analyzer = EMAAnalyzer(pair, data)
        ema_analyzer.calculate_indicators()
        ema_signal = ema_analyzer.generate_signal()
        ema_chart = ema_analyzer.plot_chart()

        # Mensaje mejorado
        response = (
            f"📊 **Análisis Completo - {pair}**\n"
            f"• EMA 21: {ema_signal}\n"
            f"• MACD: {macd_signal}\n"
            f"• Último cierre: {data['Close'].iloc[-1].item():.2f}"
        )
        await update.message.reply_photo(photo=ema_chart)
        await update.message.reply_photo(photo=macd_chart)

        await update.message.reply_text(response)

    except Exception as e:
        await update.message.reply_text(f"🔥 Error: {str(e)[:150]}")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != int(Config.GROUP_CHAT_ID):
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return
    await update.message.reply_text("✅ Alpha Break Pro 777 is online. Use /check BTC-USD")

# /check <PAIR>
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != int(Config.GROUP_CHAT_ID):
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
    if update.effective_chat.id != int(Config.GROUP_CHAT_ID):
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

