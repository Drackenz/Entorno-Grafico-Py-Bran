import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import random
import requests
import sqlite3


class ChatBot:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("ChatBot - Tu Asistente Virtual")
        self.ventana.geometry("480x650")
        self.ventana.configure(bg="#0d0d18")

        # Aqui va la api si el estudiante quiere usar IA real
        self.api_key = "PON_AQUI_TU_API_KEY"

        # Aqui conecto la base de datos
        self.conexion = sqlite3.connect("chatbot_historial.db")
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

        self.conocimiento = {
            ("hola", "buenas", "hey"): [
                "Hola, en que te ayudo?",
                "Que onda, aqui estoy.",
                "Buenas, dime que necesitas."
            ],
            ("como estas", "que tal"): [
                "Estoy bien, listo para ayudarte.",
                "Todo bien, gracias por preguntar."
            ],
            ("nombre",): [
                "Me llamo ChatBot, tu asistente virtual."
            ],
            ("chiste", "broma"): [
                "Por que los programadores prefieren el modo oscuro? Porque la luz atrae bugs.",
                "Hay 10 tipos de personas: las que saben binario y las que no."
            ],
            ("python",): [
                "Python es un lenguaje muy bueno para empezar a programar."
            ],
            ("gracias",): [
                "De nada.",
                "Para eso estoy."
            ],
            ("adios", "chao", "bye"): [
                "Hasta luego.",
                "Chao, cuidate."
            ]
        }

        self.por_defecto = [
            "No entendi eso, puedes decirlo de otra forma?",
            "Puedes preguntarme sobre hora, fecha, chiste o python."
        ]

        titulo = tk.Label(
            ventana,
            text="ChatBot con Historial",
            bg="#0d0d18",
            fg="#a78bfa",
            font=("Segoe UI", 18, "bold")
        )
        titulo.pack(pady=(12, 0))

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
        barra.pack(padx=12, pady=(0, 8), fill="x")

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
            text="Enviar",
            command=self.enviar,
            borderwidth=0,
            bg="#a78bfa",
            fg="#0d0d18",
            font=("Segoe UI", 11, "bold")
        ).pack(side="right", ipadx=8)

        barra_botones = tk.Frame(ventana, bg="#0d0d18")
        barra_botones.pack(padx=12, pady=(0, 12), fill="x")

        tk.Button(
            barra_botones,
            text="Ver historial",
            command=self.ver_historial,
            borderwidth=0,
            bg="#22d3ee",
            fg="#0d0d18",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=6)

        tk.Button(
            barra_botones,
            text="Borrar historial",
            command=self.borrar_historial,
            borderwidth=0,
            bg="#ef4444",
            fg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", expand=True, fill="x", padx=(5, 0), ipady=6)

        self.responder("Hola, soy tu asistente. Escribe algo para empezar.")

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT,
                mensaje TEXT,
                fecha TEXT
            )
        """)
        self.conexion.commit()

    def guardar_mensaje(self, autor, mensaje):
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.cursor.execute(
            "INSERT INTO historial (autor, mensaje, fecha) VALUES (?, ?, ?)",
            (autor, mensaje, fecha)
        )

        self.conexion.commit()

    def imprimir(self, autor, texto):
        self.chat.config(state="normal")
        self.chat.insert(tk.END, f"\n{autor}: {texto}\n")
        self.chat.config(state="disabled")
        self.chat.see(tk.END)

    def responder(self, texto):
        self.imprimir("ChatBot", texto)
        self.guardar_mensaje("ChatBot", texto)

    def pensar(self, mensaje):
        # Primero intenta usar IA real si hay una API key
        if self.api_key != "PON_AQUI_TU_API_KEY":
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

                respuesta = requests.post(url, headers=headers, json=datos)
                resultado = respuesta.json()

                return resultado["choices"][0]["message"]["content"]

            except:
                pass

        # Si falla la IA, usa respuestas normales
        m = mensaje.lower()

        if "hora" in m:
            return f"Son las {datetime.now():%H:%M}"

        if "fecha" in m:
            return f"Hoy es {datetime.now():%d/%m/%Y}"

        for claves, respuestas in self.conocimiento.items():
            if any(clave in m for clave in claves):
                return random.choice(respuestas)

        return random.choice(self.por_defecto)

    def enviar(self, evento=None):
        mensaje = self.entrada.get().strip()

        if not mensaje:
            return

        self.imprimir("Tu", mensaje)
        self.guardar_mensaje("Tu", mensaje)

        self.entrada.delete(0, tk.END)

        respuesta = self.pensar(mensaje)

        self.ventana.after(
            450,
            lambda: self.responder(respuesta)
        )

    def ver_historial(self):
        self.cursor.execute("SELECT autor, mensaje, fecha FROM historial")
        datos = self.cursor.fetchall()

        if len(datos) == 0:
            messagebox.showinfo("Historial", "Todavia no hay mensajes guardados.")
            return

        ventana_historial = tk.Toplevel(self.ventana)
        ventana_historial.title("Historial del ChatBot")
        ventana_historial.geometry("520x500")
        ventana_historial.configure(bg="#0d0d18")

        caja = scrolledtext.ScrolledText(
            ventana_historial,
            wrap=tk.WORD,
            bg="#141422",
            fg="#e8ecf5",
            font=("Segoe UI", 10)
        )
        caja.pack(padx=12, pady=12, fill="both", expand=True)

        for autor, mensaje, fecha in datos:
            caja.insert(tk.END, f"[{fecha}] {autor}: {mensaje}\n\n")

        caja.config(state="disabled")

    def borrar_historial(self):
        respuesta = messagebox.askyesno(
            "Borrar historial",
            "Seguro que quieres borrar todo el historial?"
        )

        if respuesta:
            self.cursor.execute("DELETE FROM historial")
            self.conexion.commit()
            messagebox.showinfo("Listo", "Historial borrado correctamente.")

    def cerrar(self):
        self.conexion.close()
        self.ventana.destroy()


if __name__ == "__main__":
    raiz = tk.Tk()
    app = ChatBot(raiz)
    raiz.protocol("WM_DELETE_WINDOW", app.cerrar)
    raiz.mainloop()