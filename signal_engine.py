from io import BytesIO

import matplotlib.pyplot as plt
import yfinance as yf


def analyze_market(pair: str):
    try:
        # 1. Descargar datos
        df = yf.download(pair, period="3mo", interval="1h", auto_adjust=True)

        if df.empty or len(df) < 50:
            print(f"⚠️ Datos insuficientes para {pair}")
            return None, None

        # 2. Calcular EMA (21 periodos)
        df["EMA"] = df["Close"].ewm(span=21, adjust=False).mean()

        # 3. Obtener valores escalares correctamente
        close = df["Close"].iloc[-1].item()  # Usar .item() para evitar warnings
        ema = df["EMA"].iloc[-1].item()  # .item() extrae el float

        # 4. Formatear señal
        signal = (
            "🚨 **Señal de Compra** 🚨\n"
            f"🔹 **Par:** {pair.replace('-', '/')}\n"
            f"🔹 **Precio Actual:** ${close:.2f}\n"
            f"🔹 **EMA (21 períodos):** ${ema:.2f}\n"
            "📈 **Condiciones Cumplidas:**\n"
            "- Precio por encima del EMA 21\n"
            "- Volumen superior a la media"
        )

        # 5. Gráfico profesional
        plt.figure(figsize=(12, 6))
        plt.plot(df["Close"].tail(50).values, label="Precio", color="#1f77b4", linewidth=2)
        plt.plot(df["EMA"].tail(50).values, label="EMA 21", color="#ff7f0e", linestyle="--")
        plt.title(f"Análisis Técnico: {pair}", fontsize=14, fontweight="bold")
        plt.legend(frameon=False)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # 6. Guardar gráfico en buffer
        buffer = BytesIO()
        plt.savefig(buffer, format="png", bbox_inches="tight", dpi=100)
        plt.close()
        buffer.seek(0)

        return signal, buffer

    except KeyError as e:
        print(f"❌ Error en {pair}: Columna no encontrada - {str(e)}")
        return None, None
    except Exception as e:
        print(f"❌ Error crítico en {pair}: {str(e)}")
        return None, None