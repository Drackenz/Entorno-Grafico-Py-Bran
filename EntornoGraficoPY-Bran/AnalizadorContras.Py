import customtkinter as ctk
import string
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class AnalizadorContrasenas(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🔓 Analizador de Seguridad")
        self.geometry("480x600")

        ctk.CTkLabel(
            self,
            text="Analizador de Contraseñas",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

        self.entrada = ctk.CTkEntry(
            self,
            placeholder_text="Escribe tu contraseña...",
            width=320,
            height=42,
            show="•"
        )
        self.entrada.pack(pady=10)
        self.entrada.bind("<KeyRelease>", self.analizar)

        self.mostrar = ctk.CTkCheckBox(
            self,
            text="Mostrar contraseña",
            command=self.toggle_mostrar
        )
        self.mostrar.pack(pady=5)

        self.barra = ctk.CTkProgressBar(self, width=320)
        self.barra.pack(pady=15)
        self.barra.set(0)

        self.nivel = ctk.CTkLabel(
            self,
            text="Esperando...",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.nivel.pack(pady=5)

        self.tiempo = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.tiempo.pack(pady=5)

        self.tips = ctk.CTkLabel(
            self,
            text="",
            justify="left",
            font=ctk.CTkFont(size=13)
        )
        self.tips.pack(pady=10)

    def toggle_mostrar(self):
        self.entrada.configure(show="" if self.mostrar.get() else "•")

    def calcular_entropia(self, clave):
        alfabeto = 0

        if any(c in string.ascii_lowercase for c in clave):
            alfabeto += 26

        if any(c in string.ascii_uppercase for c in clave):
            alfabeto += 26

        if any(c in string.digits for c in clave):
            alfabeto += 10

        if any(c in string.punctuation for c in clave):
            alfabeto += 32

        if alfabeto == 0:
            return 0

        return len(clave) * math.log2(alfabeto)

    def formatear_tiempo(self, segundos):
        if segundos < 1:
            return "instantáneo ⚡"

        unidades = [
            ("siglos", 3153600000),
            ("años", 31536000),
            ("días", 86400),
            ("horas", 3600),
            ("minutos", 60),
            ("segundos", 1)
        ]

        for nombre, valor in unidades:
            if segundos >= valor:
                cantidad = segundos / valor

                if cantidad > 1000000:
                    return f"{cantidad:.1e} {nombre}"

                return f"{cantidad:,.1f} {nombre}"

        return "instantáneo"

    def analizar(self, evento=None):
        clave = self.entrada.get()

        if not clave:
            self.barra.set(0)
            self.nivel.configure(text="Esperando...")
            self.tiempo.configure(text="")
            self.tips.configure(text="")
            return

        # RETO EXTRA
        comunes = [
            "123456",
            "123456789",
            "password",
            "qwerty",
            "abc123",
            "admin",
            "111111"
        ]

        if clave.lower() in comunes:
            self.barra.set(0.05)
            self.barra.configure(progress_color="red")

            self.nivel.configure(
                text="🚨 ¡Esta clave está en las listas de hackers!",
                text_color="red"
            )

            self.tiempo.configure(
                text="⏱️ Tiempo estimado: instantáneo ⚡"
            )

            self.tips.configure(
                text="• Esta contraseña es muy común\n"
                     "• Usa una contraseña diferente"
            )

            return

        entropia = self.calcular_entropia(clave)

        segundos = (2 ** entropia) / 10000000000

        if entropia < 28:
            nivel = "Muy Débil 💀"
            color = "#ff2d78"
            valor = 0.20

        elif entropia < 36:
            nivel = "Débil ⚠️"
            color = "#ff8c42"
            valor = 0.40

        elif entropia < 60:
            nivel = "Aceptable 👍"
            color = "#fbbf24"
            valor = 0.65

        elif entropia < 128:
            nivel = "Fuerte 💪"
            color = "#4ade80"
            valor = 0.85

        else:
            nivel = "Impenetrable 🛡️"
            color = "#22d3ee"
            valor = 1.0

        self.barra.set(valor)
        self.barra.configure(progress_color=color)

        self.nivel.configure(
            text=nivel,
            text_color=color
        )

        self.tiempo.configure(
            text=f"⏱️ Crackearla tomaría: {self.formatear_tiempo(segundos)}"
        )

        consejos = []

        if len(clave) < 12:
            consejos.append("• Usa al menos 12 caracteres")

        if not any(c in string.ascii_uppercase for c in clave):
            consejos.append("• Agrega MAYÚSCULAS")

        if not any(c in string.digits for c in clave):
            consejos.append("• Agrega números")

        if not any(c in string.punctuation for c in clave):
            consejos.append("• Agrega símbolos (! @ # $)")

        self.tips.configure(
            text="\n".join(consejos) or "¡Excelente contraseña! ✅"
        )


if __name__ == "__main__":
    AnalizadorContrasenas().mainloop()