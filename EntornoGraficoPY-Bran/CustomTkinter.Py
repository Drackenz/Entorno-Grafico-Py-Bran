import customtkinter as ctk

ctk.set_appearance_mode("dark")          # Modo oscuro automático
ctk.set_default_color_theme("blue")      # Paleta de color

ventana = ctk.CTk()
ventana.title("App Moderna")
ventana.geometry("400x300")

etiqueta = ctk.CTkLabel(ventana,
                        text="¡Diseño moderno! ✨",
                        font=ctk.CTkFont(size=20, weight="bold"))
etiqueta.pack(pady=50)

boton = ctk.CTkButton(ventana, text="Botón con estilo",
                      command=lambda: etiqueta.configure(text="¡Increíble! 🔥"))
boton.pack()

ventana.mainloop()
