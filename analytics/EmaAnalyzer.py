# analytics/ema_analyzer.py
import matplotlib.pyplot as plt
from io import BytesIO

import pandas as pd

from .base_analyzer import BaseAnalyzer


class EMAAnalyzer(BaseAnalyzer):
    def __init__(self, pair: str, data: pd.DataFrame):
        if data is None or data.empty:
            raise ValueError("⚠️ Datos no disponibles para análisis")
        super().__init__(pair, data)

    def calculate_indicators(self):
        self.data['EMA_21'] = self.data['Close'].ewm(span=21, adjust=False).mean()
        return self.data

    def generate_signal(self):
        macd_value = self.data['MACD'].iloc[-1].item()  # Convertir a float
        signal_value = self.data['Signal'].iloc[-1].item()
        return "BUY" if macd_value > signal_value else "HOLD"

    def plot_chart(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data['Close'].tail(50), label='Precio', color='blue')
        plt.plot(self.data['EMA_21'].tail(50), label='EMA 21', color='orange', linestyle='--')
        plt.title(f"Análisis EMA - {self.pair}")
        plt.legend()

        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        plt.close()
        buffer.seek(0)
        return buffer