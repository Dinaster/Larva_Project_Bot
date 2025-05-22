# utils/data_fetcher.py
import yfinance as yf
import pandas as pd
import asyncio
from typing import Optional


async def get_market_data(
        pair: str,
        period: str = "3mo",
        interval: str = "1h",
        auto_adjust: bool = True
) -> Optional[pd.DataFrame]:
    """
    Obtiene datos históricos de Yahoo Finance de forma asíncrona.

    Args:
        pair (str): Par de trading (ej: 'BTC-USD')
        period (str): Período histórico ('1d', '1mo', '1y', etc)
        interval (str): Intervalo entre datos ('1h', '1d', etc)
        auto_adjust (bool): Ajustar precios automáticamente

    Returns:
        pd.DataFrame | None: DataFrame con datos OHLCV o None si hay error
    """
    try:
        # Ejecutar yfinance en un hilo separado (evita bloquear el event loop)
        return await asyncio.to_thread(
            yf.download,
            tickers=pair,
            period=period,
            interval=interval,
            auto_adjust=auto_adjust,
            progress=False,
            threads=False  # Evita conflictos con asyncio
        )
    except Exception as e:
        print(f"⚠️ Error obteniendo datos para {pair}: {str(e)[:200]}")
        return None