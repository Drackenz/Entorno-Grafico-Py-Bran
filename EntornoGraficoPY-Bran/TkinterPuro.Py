import tkinter as tk

ventana = tk.Tk()                       # 1. Crear la ventana principal
ventana.title("¡Mi Primera App!")       # 2. Ponerle un título
ventana.geometry("400x300")             # 3. Tamaño: ancho x alto

etiqueta = tk.Label(ventana,
                    text="¡Hola, mundo gráfico! 🚀",
                    font=("Arial", 16))
etiqueta.pack(pady=50)                   # 4. Mostrarla en pantalla

boton = tk.Button(ventana, text="¡Haz clic!",
                  command=lambda: etiqueta.config(text="¡Funcionó! 🎉"))
boton.pack()

ventana.mainloop()                       # 5. Mantener la ventana viva
