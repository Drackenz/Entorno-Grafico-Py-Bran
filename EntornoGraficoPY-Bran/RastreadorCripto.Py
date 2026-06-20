import customtkinter as ctk
from datetime import datetime
import threading
import requests

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class RastreadorCripto(ctk.CTk):

    API = "https://api.coingecko.com/api/v3/simple/price"

    MONEDAS = {
        "Bitcoin": "bitcoin",
        "Ethereum": "ethereum",
        "Solana": "solana",
        "Cardano": "cardano",
        "Dogecoin": "dogecoin"
    }

    def __init__(self):
        super().__init__()

        self.title("₿ Rastreador de Criptomonedas")
        self.geometry("500x560")

        # Reto extra
        self.historial = []

        ctk.CTkLabel(
            self,
            text="₿ Precios en Tiempo Real",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=20)

        self.selector = ctk.CTkComboBox(
            self,
            values=list(self.MONEDAS),
            width=300,
            height=40,
            command=lambda _: self.consultar()
        )
        self.selector.set("Bitcoin")
        self.selector.pack(pady=10)

        self.precio = ctk.CTkLabel(
            self,
            text="$ ---",
            font=ctk.CTkFont(size=46, weight="bold"),
            text_color="#4ade80"
        )
        self.precio.pack(pady=20)

        self.cambio = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=18)
        )
        self.cambio.pack(pady=5)

        self.hora = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.hora.pack(pady=5)

        ctk.CTkButton(
            self,
            text="🔄 Actualizar",
            width=200,
            height=40,
            command=self.consultar
        ).pack(pady=20)

        # Canvas para el historial (reto extra)
        self.grafica = ctk.CTkCanvas(
            self,
            width=420,
            height=150,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.grafica.pack(pady=10)

        self.consultar()

        # Reto extra:
        # actualización automática cada 30 segundos
        self.after(30000, self.actualizacion_automatica)

    def consultar(self):
        self.precio.configure(text="Cargando...")
        threading.Thread(
            target=self._descargar,
            daemon=True
        ).start()

    def actualizacion_automatica(self):
        self.consultar()
        self.after(30000, self.actualizacion_automatica)

    def _descargar(self):

        moneda = self.MONEDAS[self.selector.get()]

        parametros = {
            "ids": moneda,
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }

        try:
            datos = requests.get(
                self.API,
                params=parametros,
                timeout=10
            ).json()

            precio = datos[moneda]["usd"]
            cambio = datos[moneda]["usd_24h_change"]

            self.after(
                0,
                lambda: self._mostrar(precio, cambio)
            )

        except Exception:
            self.after(0, self._error)

    def _mostrar(self, precio, cambio):

        # El Salvador usa USD
        self.precio.configure(
            text=f"US$ {precio:,.2f}"
        )

        if cambio >= 0:
            self.cambio.configure(
                text=f"▲ +{cambio:.2f}% (24h)",
                text_color="#4ade80"
            )
        else:
            self.cambio.configure(
                text=f"▼ {cambio:.2f}% (24h)",
                text_color="#ff2d78"
            )

        self.hora.configure(
            text=f"Actualizado: {datetime.now():%H:%M:%S}"
        )

        # Reto extra:
        # guardar historial de precios

        self.historial.append(precio)

        if len(self.historial) > 20:
            self.historial.pop(0)

        self.dibujar_historial()

    def dibujar_historial(self):

        self.grafica.delete("all")

        if len(self.historial) < 2:
            return

        ancho = 420
        alto = 150

        minimo = min(self.historial)
        maximo = max(self.historial)

        if minimo == maximo:
            maximo += 1

        paso_x = ancho / (len(self.historial) - 1)

        puntos = []

        for i, valor in enumerate(self.historial):

            x = i * paso_x

            y = alto - (
                (valor - minimo) /
                (maximo - minimo)
            ) * (alto - 20)

            puntos.extend([x, y])

        self.grafica.create_line(
            puntos,
            fill="#4ade80",
            width=3,
            smooth=True
        )

    def _error(self):
        self.precio.configure(text="Error ❌")

        self.cambio.configure(
            text="Revisa tu conexión a internet",
            text_color="#ff2d78"
        )


if __name__ == "__main__":
    RastreadorCripto().mainloop()