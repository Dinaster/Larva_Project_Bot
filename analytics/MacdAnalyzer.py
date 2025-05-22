# analytics/macd_analyzer.py
import matplotlib.pyplot as plt
from io import BytesIO

import pandas as pd

from .base_analyzer import BaseAnalyzer


class MACDAnalyzer(BaseAnalyzer):
    def __init__(self, pair: str, data: pd.DataFrame):
        if data is None or data.empty:
            raise ValueError("⚠️ Datos no disponibles para análisis")
        super().__init__(pair, data)

    def calculate_indicators(self):
        try:
            # Cálculos con verificación de datos
            if 'Close' not in self.data.columns:
                raise ValueError("Columna 'Close' no encontrada")

            self.data['EMA_12'] = self.data['Close'].ewm(span=12, adjust=False).mean()
            self.data['EMA_26'] = self.data['Close'].ewm(span=26, adjust=False).mean()
            self.data['MACD'] = self.data['EMA_12'] - self.data['EMA_26']
            self.data['Signal'] = self.data['MACD'].ewm(span=9, adjust=False).mean()

            return self.data
        except KeyError as e:
            print(f"❌ Error en MACDAnalyzer: {str(e)}")
            raise

    def generate_signal(self):
        try:
            # Extraer valores como floats
            macd = self.data['MACD'].iloc[-1].item()
            signal = self.data['Signal'].iloc[-1].item()

            # Generar señal segura
            if macd > signal:
                return "🚨 COMPRAR"
            elif macd < signal:
                return "🔻 VENDER"
            else:
                return "🟡 NEUTRAL"

        except IndexError:
            return "📭 DATOS INSUFICIENTES"

    def plot_chart(self):
        # Gráfico específico para MACD
        plt.figure(figsize=(12, 6))
        plt.plot(self.data['MACD'].tail(50), label='MACD', color='blue')
        plt.plot(self.data['Signal'].tail(50), label='Signal', color='red')
        plt.title(f"Análisis MACD - {self.pair}")
        plt.legend()

        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        plt.close()
        buffer.seek(0)
        return buffer