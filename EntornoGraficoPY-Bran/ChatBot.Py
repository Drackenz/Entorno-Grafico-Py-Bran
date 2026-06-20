import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import random
import requests

class ChatBot:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("🤖 ChatBot — Tu Asistente Virtual")
        self.ventana.geometry("460x600")
        self.ventana.configure(bg="#0d0d18")

        # Reto extra
        self.api_key = "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"

        self.conocimiento = {
            ("hola", "buenas", "hey"): [
                "¡Hola! ¿En qué te ayudo? 😊",
                "¡Qué onda! 👋",
                "¡Buenas! Aquí estoy."
            ],
            ("como estas", "que tal"): [
                "¡De maravilla! Listo para ayudarte 🚀",
                "Excelente, ¿y vos?"
            ],
            ("nombre",): [
                "Me llamo ChatBot, tu asistente virtual 🤖"
            ],
            ("chiste", "broma"): [
                "¿Por qué los programadores prefieren el modo oscuro? Porque la luz atrae a los bugs 🐛😂",
                "Hay 10 tipos de personas: las que saben binario y las que no."
            ],
            ("python",): [
                "Python es ideal para empezar a programar 🐍"
            ],
            ("gracias",): [
                "¡De nada! 🙌",
                "¡Para eso estoy! 💪"
            ],
            ("adios", "chao", "bye"): [
                "¡Hasta luego! 👋",
                "¡Chao pescao! 🐟"
            ]
        }

        self.por_defecto = [
            "No entendí eso 🤔 ¿Lo puedes decir de otra forma?",
            "Pregúntame sobre: hora, fecha, chiste, python..."
        ]

        self.chat = scrolledtext.ScrolledText(
            ventana,
            wrap=tk.WORD,
            bg="#141422",
            fg="#e8ecf5",
            font=("Segoe UI", 11),
            state="disabled",
            borderwidth=0
        )
        self.chat.pack(padx=12, pady=12, fill="both", expand=True)

        barra = tk.Frame(ventana, bg="#0d0d18")
        barra.pack(padx=12, pady=(0, 12), fill="x")

        self.entrada = tk.Entry(
            barra,
            font=("Segoe UI", 12),
            bg="#1f2336",
            fg="white",
            insertbackground="white",
            borderwidth=0
        )
        self.entrada.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 6))
        self.entrada.bind("<Return>", self.enviar)

        tk.Button(
            barra,
            text="Enviar ➤",
            command=self.enviar,
            borderwidth=0,
            bg="#a78bfa",
            fg="#0d0d18",
            font=("Segoe UI", 11, "bold")
        ).pack(side="right", ipadx=8)

        self.responder("¡Hola! Soy tu asistente 🤖 Escribe algo para empezar.")

    def imprimir(self, autor, texto, emoji):
        self.chat.config(state="normal")
        self.chat.insert(tk.END, f"\n{emoji} {autor}: {texto}\n")
        self.chat.config(state="disabled")
        self.chat.see(tk.END)

    def responder(self, texto):
        self.imprimir("ChatBot", texto, "🤖")

    def pensar(self, mensaje):

        # Reto extra:
        # se intenta responder con una IA real usando requests

        try:
            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            datos = {
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": mensaje
                    }
                ]
            }

            respuesta = requests.post(
                url,
                headers=headers,
                json=datos
            )

            resultado = respuesta.json()

            return resultado["choices"][0]["message"]["content"]

        except:

            # Si falla la IA, usa el chatbot normal

            m = mensaje.lower()

            if "hora" in m:
                return f"Son las {datetime.now():%H:%M} ⏰"

            if "fecha" in m:
                return f"Hoy es {datetime.now():%d/%m/%Y} 📅"

            for claves, respuestas in self.conocimiento.items():
                if any(clave in m for clave in claves):
                    return random.choice(respuestas)

            return random.choice(self.por_defecto)

    def enviar(self, evento=None):
        mensaje = self.entrada.get().strip()

        if not mensaje:
            return

        self.imprimir("Tú", mensaje, "🧑")
        self.entrada.delete(0, tk.END)

        respuesta = self.pensar(mensaje)

        self.ventana.after(
            450,
            lambda: self.responder(respuesta)
        )


if __name__ == "__main__":
    raiz = tk.Tk()
    ChatBot(raiz)
    raiz.mainloop()