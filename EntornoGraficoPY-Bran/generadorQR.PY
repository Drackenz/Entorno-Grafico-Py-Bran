import customtkinter as ctk
from tkinter import filedialog, colorchooser
from PIL import Image
import qrcode
import io

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GeneradorQR(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Generador de Códigos QR")
        self.geometry("450x760")

        self.imagen_qr = None
        self.logo = None
        self.color_qr = "#22d3ee"

        ctk.CTkLabel(
            self,
            text="Generador de QR",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text="Escribe un texto, enlace o dirección de Bitcoin:"
        ).pack(pady=5)

        self.entrada = ctk.CTkEntry(
            self,
            placeholder_text="https://...",
            width=350,
            height=40
        )
        self.entrada.pack(pady=10)

        self.boton_color = ctk.CTkButton(
            self,
            text="Elegir color del QR",
            width=200,
            height=40,
            command=self.elegir_color
        )
        self.boton_color.pack(pady=10)

        self.texto_color = ctk.CTkLabel(
            self,
            text="Color actual: #22d3ee"
        )
        self.texto_color.pack(pady=5)

        self.boton_logo = ctk.CTkButton(
            self,
            text="Agregar logo al centro",
            width=200,
            height=40,
            command=self.elegir_logo
        )
        self.boton_logo.pack(pady=10)

        self.texto_logo = ctk.CTkLabel(
            self,
            text="Logo: ninguno"
        )
        self.texto_logo.pack(pady=5)

        ctk.CTkButton(
            self,
            text="Generar QR",
            width=200,
            height=40,
            command=self.generar
        ).pack(pady=15)

        self.vista = ctk.CTkLabel(
            self,
            text="Tu código QR aparecerá aquí",
            width=270,
            height=270
        )
        self.vista.pack(pady=20)

        self.boton_guardar = ctk.CTkButton(
            self,
            text="Guardar imagen",
            width=200,
            state="disabled",
            command=self.guardar
        )
        self.boton_guardar.pack(pady=10)

    def elegir_color(self):
        color = colorchooser.askcolor(title="Elige un color para el QR")

        if color[1] is not None:
            self.color_qr = color[1]
            self.texto_color.configure(text="Color actual: " + self.color_qr)

    def elegir_logo(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona un logo",
            filetypes=[
                ("Imagenes", "*.png *.jpg *.jpeg"),
                ("Todos los archivos", "*.*")
            ]
        )

        if ruta:
            self.logo = Image.open(ruta).convert("RGBA")
            self.texto_logo.configure(text="Logo agregado")

    def generar(self):
        texto = self.entrada.get().strip()

        if not texto:
            self.vista.configure(text="Escribe algo primero", image=None)
            return

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )

        qr.add_data(texto)
        qr.make(fit=True)

        imagen = qr.make_image(
            fill_color=self.color_qr,
            back_color="#0d0d18"
        )

        buffer = io.BytesIO()
        imagen.save(buffer, format="PNG")
        buffer.seek(0)

        self.imagen_qr = Image.open(buffer).convert("RGBA")

        # Aqui le pongo el logo en el centro si el usuario eligio uno
        if self.logo is not None:
            qr_ancho, qr_alto = self.imagen_qr.size

            tamano_logo = qr_ancho // 5

            logo_copia = self.logo.copy()
            logo_copia.thumbnail((tamano_logo, tamano_logo))

            pos_x = (qr_ancho - logo_copia.size[0]) // 2
            pos_y = (qr_alto - logo_copia.size[1]) // 2

            # Hice un cuadrito de fondo para que el logo se vea mejor
            fondo_logo = Image.new(
                "RGBA",
                (logo_copia.size[0] + 20, logo_copia.size[1] + 20),
                "#ffffff"
            )

            fondo_x = (qr_ancho - fondo_logo.size[0]) // 2
            fondo_y = (qr_alto - fondo_logo.size[1]) // 2

            self.imagen_qr.paste(fondo_logo, (fondo_x, fondo_y))
            self.imagen_qr.paste(logo_copia, (pos_x, pos_y), logo_copia)

        self.vista.configure(
            image=ctk.CTkImage(self.imagen_qr, size=(270, 270)),
            text=""
        )

        self.boton_guardar.configure(state="normal")

    def guardar(self):
        if not self.imagen_qr:
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png")]
        )

        if ruta:
            self.imagen_qr.save(ruta)


if __name__ == "__main__":
    app = GeneradorQR()
    app.mainloop()