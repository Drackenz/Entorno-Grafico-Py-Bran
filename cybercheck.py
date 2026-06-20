import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class CyberCheck(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CyberCheck")
        self.geometry("520x720")

        self.preguntas = [
            {
                "texto": "Uso la misma contraseña en varias cuentas",
                "riesgo": 20,
                "consejo": "No uses la misma contraseña en todas tus cuentas."
            },
            {
                "texto": "Tengo activada la verificación en dos pasos",
                "riesgo": -20,
                "consejo": "Muy bien, la verificación en dos pasos ayuda bastante."
            },
            {
                "texto": "Descargo archivos de páginas que no conozco",
                "riesgo": 20,
                "consejo": "Evita descargar archivos de sitios desconocidos."
            },
            {
                "texto": "Comparto datos personales en redes sociales",
                "riesgo": 15,
                "consejo": "Ten cuidado con la información personal que publicas."
            },
            {
                "texto": "Reviso si un enlace parece sospechoso antes de abrirlo",
                "riesgo": -15,
                "consejo": "Buen hábito, revisar enlaces puede evitar engaños."
            },
            {
                "texto": "Cierro sesión cuando uso computadoras ajenas",
                "riesgo": -15,
                "consejo": "Excelente, cerrar sesión evita que usen tus cuentas."
            },
            {
                "texto": "Uso WiFi público para entrar a cuentas importantes",
                "riesgo": 15,
                "consejo": "Evita entrar a cuentas importantes desde WiFi público."
            },
            {
                "texto": "Actualizo mis aplicaciones y mi sistema",
                "riesgo": -10,
                "consejo": "Actualizar tus apps ayuda a corregir fallos de seguridad."
            }
        ]

        self.checks = []

        ctk.CTkLabel(
            self,
            text="CyberCheck",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4ade80"
        ).pack(pady=15)

        ctk.CTkLabel(
            self,
            text="Medidor de Riesgo Digital",
            font=ctk.CTkFont(size=17, weight="bold")
        ).pack(pady=2)

        ctk.CTkLabel(
            self,
            text="Marca las opciones que aplican para ti:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=10)

        self.caja_preguntas = ctk.CTkFrame(self)
        self.caja_preguntas.pack(pady=10, padx=20, fill="both")

        for pregunta in self.preguntas:
            check = ctk.CTkCheckBox(
                self.caja_preguntas,
                text=pregunta["texto"],
                font=ctk.CTkFont(size=13)
            )
            check.pack(anchor="w", padx=15, pady=7)
            self.checks.append(check)

        self.boton = ctk.CTkButton(
            self,
            text="Calcular mi riesgo",
            width=220,
            height=40,
            fg_color="#22c55e",
            hover_color="#16a34a",
            command=self.calcular
        )
        self.boton.pack(pady=15)

        self.barra = ctk.CTkProgressBar(self, width=350)
        self.barra.pack(pady=10)
        self.barra.set(0)

        self.resultado = ctk.CTkLabel(
            self,
            text="Resultado pendiente",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.resultado.pack(pady=10)

        self.puntaje_texto = ctk.CTkLabel(
            self,
            text="Puntaje: 0 / 100",
            font=ctk.CTkFont(size=14)
        )
        self.puntaje_texto.pack(pady=3)

        self.consejos = ctk.CTkLabel(
            self,
            text="",
            justify="left",
            wraplength=430,
            font=ctk.CTkFont(size=13)
        )
        self.consejos.pack(pady=10)

        self.plan = ctk.CTkLabel(
            self,
            text="",
            justify="left",
            wraplength=430,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.plan.pack(pady=10)

    def calcular(self):
        riesgo = 30
        lista_consejos = []

        for i in range(len(self.checks)):
            if self.checks[i].get() == 1:
                riesgo += self.preguntas[i]["riesgo"]

                if self.preguntas[i]["riesgo"] > 0:
                    lista_consejos.append("- " + self.preguntas[i]["consejo"])

        if riesgo < 0:
            riesgo = 0

        if riesgo > 100:
            riesgo = 100

        self.barra.set(riesgo / 100)
        self.puntaje_texto.configure(text=f"Puntaje: {riesgo} / 100")

        if riesgo <= 25:
            nivel = "Seguro"
            color = "#4ade80"
            mensaje_plan = (
                "Plan de mejora:\n"
                "Vas bien. Solo sigue revisando tus cuentas y no te confíes."
            )

        elif riesgo <= 50:
            nivel = "Cuidado"
            color = "#facc15"
            mensaje_plan = (
                "Plan de mejora:\n"
                "Activa la verificación en dos pasos y revisa tus contraseñas."
            )

        elif riesgo <= 75:
            nivel = "Riesgo alto"
            color = "#fb923c"
            mensaje_plan = (
                "Plan de mejora:\n"
                "Cambia contraseñas repetidas, evita WiFi público y revisa enlaces."
            )

        else:
            nivel = "Modo peligro"
            color = "#ef4444"
            mensaje_plan = (
                "Plan de mejora:\n"
                "Necesitas mejorar varios hábitos: cambia contraseñas, "
                "activa verificación en dos pasos y evita sitios sospechosos."
            )

        self.barra.configure(progress_color=color)

        self.resultado.configure(
            text=nivel,
            text_color=color
        )

        if len(lista_consejos) == 0:
            texto_consejos = "No marcaste hábitos peligrosos. Buen trabajo."
        else:
            texto_consejos = "Consejos:\n" + "\n".join(lista_consejos)

        self.consejos.configure(text=texto_consejos)
        self.plan.configure(text=mensaje_plan)


if __name__ == "__main__":
    app = CyberCheck()
    app.mainloop()