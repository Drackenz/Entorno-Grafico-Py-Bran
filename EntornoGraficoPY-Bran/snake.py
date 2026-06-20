import tkinter as tk
import random

class JuegoSnake:
    ANCHO, ALTO, CELDA, VELOCIDAD = 600, 400, 20, 110

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("🐍 La Serpiente")
        self.ventana.resizable(False, False)

        self.puntaje = 0
        self.direccion = "Right"
        self.velocidad_actual = self.VELOCIDAD

        self.marcador = tk.Label(ventana, text="Puntaje: 0",
                                 font=("Consolas", 20, "bold"),
                                 bg="#06060c", fg="#4ade80")
        self.marcador.pack()

        self.lienzo = tk.Canvas(ventana, width=self.ANCHO, height=self.ALTO,
                                bg="#06060c", highlightthickness=0)
        self.lienzo.pack()

        self.serpiente = [(100, 100), (80, 100), (60, 100)]
        self.comida = self.nueva_comida()

        self.boton_reiniciar = None

        # Controles con las flechas del teclado
        for tecla in ("Left", "Right", "Up", "Down"):
            self.ventana.bind(f"<{tecla}>",
                              lambda e, t=tecla: self.girar(t))

        self.actualizar()

    def nueva_comida(self):
        x = random.randint(0, (self.ANCHO - self.CELDA) // self.CELDA) * self.CELDA
        y = random.randint(0, (self.ALTO - self.CELDA) // self.CELDA) * self.CELDA
        return (x, y)

    def girar(self, nueva):
        opuestos = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if nueva != opuestos[self.direccion]:
            self.direccion = nueva

    def mover(self):
        x, y = self.serpiente[0]

        if self.direccion == "Right":
            x += self.CELDA
        elif self.direccion == "Left":
            x -= self.CELDA
        elif self.direccion == "Up":
            y -= self.CELDA
        elif self.direccion == "Down":
            y += self.CELDA

        cabeza = (x, y)
        self.serpiente.insert(0, cabeza)

        if cabeza == self.comida:
            self.puntaje += 10
            self.marcador.config(text=f"Puntaje: {self.puntaje}")
            self.comida = self.nueva_comida()

            # Reto extra:
            # cada 50 puntos aumenta un poco la velocidad
            if self.puntaje % 50 == 0 and self.velocidad_actual > 40:
                self.velocidad_actual -= 10

        else:
            self.serpiente.pop()

    def hay_choque(self):
        x, y = self.serpiente[0]

        fuera = x < 0 or x >= self.ANCHO or y < 0 or y >= self.ALTO
        se_muerde = self.serpiente[0] in self.serpiente[1:]

        return fuera or se_muerde

    def dibujar(self):
        self.lienzo.delete("all")

        cx, cy = self.comida
        self.lienzo.create_oval(
            cx, cy,
            cx + self.CELDA,
            cy + self.CELDA,
            fill="#ff2d78",
            outline=""
        )

        for i, (x, y) in enumerate(self.serpiente):
            color = "#22d3ee" if i == 0 else "#4ade80"

            self.lienzo.create_rectangle(
                x, y,
                x + self.CELDA,
                y + self.CELDA,
                fill=color,
                outline="#06060c"
            )

    def reiniciar(self):
        if self.boton_reiniciar:
            self.boton_reiniciar.destroy()

        self.puntaje = 0
        self.velocidad_actual = self.VELOCIDAD
        self.direccion = "Right"

        self.marcador.config(text="Puntaje: 0")

        self.serpiente = [(100, 100), (80, 100), (60, 100)]
        self.comida = self.nueva_comida()

        self.actualizar()

    def game_over(self):
        self.lienzo.create_text(
            self.ANCHO // 2,
            self.ALTO // 2,
            text="GAME OVER",
            fill="#ff2d78",
            font=("Consolas", 42, "bold")
        )

        self.lienzo.create_text(
            self.ANCHO // 2,
            self.ALTO // 2 + 45,
            text=f"Puntaje final: {self.puntaje}",
            fill="#4ade80",
            font=("Consolas", 18)
        )

        # Reto extra:
        # aparece un botón para volver a jugar
        self.boton_reiniciar = tk.Button(
            self.ventana,
            text="Reiniciar",
            command=self.reiniciar
        )
        self.boton_reiniciar.pack(pady=10)

    def actualizar(self):
        if self.hay_choque():
            self.game_over()
            return

        self.mover()
        self.dibujar()

        self.ventana.after(
            self.velocidad_actual,
            self.actualizar
        )


if __name__ == "__main__":
    raiz = tk.Tk()
    JuegoSnake(raiz)
    raiz.mainloop()