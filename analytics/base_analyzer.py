from abc import ABC, abstractmethod
import pandas as pd

class BaseAnalyzer(ABC):
    def __init__(self, pair: str, data: pd.DataFrame):
        self.pair = pair
        self.data = data

    @abstractmethod
    def calculate_indicators(self):
        """Calcula los indicadores técnicos."""
        pass

    @abstractmethod
    def generate_signal(self):
        """Genera la señal de compra/venta."""
        pass

    @abstractmethod
    def plot_chart(self):
        """Genera el gráfico de análisis."""
        pass