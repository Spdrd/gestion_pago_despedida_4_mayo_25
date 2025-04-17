import customtkinter as ctk
import repo
from utils import formatear_con_puntos

class Pantalla:

    def __init__(self):
        # Configuración del tema
        ctk.set_appearance_mode("System")  # "Light" o "Dark"
        ctk.set_default_color_theme("blue")  # Puedes cambiar a "green", "dark-blue", etc.

        # Cargar datos
        self.personas = repo.cargar_datos()

        # Crear ventana
        self.ventana = ctk.CTk()
        self.ventana.title("Suma de Pagos desde JSON")
        self.ventana.geometry("320x400")

        # Instrucción
        self.label_instruccion = ctk.CTkLabel(self.ventana, text="Seleccione una persona:")
        self.label_instruccion.pack(pady=5)

        # ComboBox
        nombres = [p["nombre"] for p in self.personas]
        self.combo_nombres = ctk.CTkComboBox(self.ventana, values=nombres, command=self.mostrar_suma)
        self.combo_nombres.pack(pady=5)

        # Resultado
        self.label_resultado = ctk.CTkLabel(self.ventana, text="Suma de pagos: $0")
        self.label_resultado.pack(pady=10)

        # Entrada de nuevo pago
        self.label_nuevo_pago = ctk.CTkLabel(self.ventana, text="Añadir nuevo pago:")
        self.label_nuevo_pago.pack()
        self.entry_pago = ctk.CTkEntry(self.ventana)
        self.entry_pago.pack(pady=5)

        # Botón para agregar pago
        self.boton_agregar = ctk.CTkButton(self.ventana, text="Agregar Pago", command=self.agregar_pago)
        self.boton_agregar.pack(pady=5)

        # Separador visual
        ctk.CTkLabel(self.ventana, text="").pack()

        # Entrada para nuevo nombre
        self.label_nuevo_nombre = ctk.CTkLabel(self.ventana, text="Añadir nueva persona:")
        self.label_nuevo_nombre.pack()
        self.entry_nuevo_nombre = ctk.CTkEntry(self.ventana)
        self.entry_nuevo_nombre.pack(pady=5)

        # Botón para agregar persona
        self.boton_agregar_nombre = ctk.CTkButton(self.ventana, text="Agregar Persona", command=self.agregar_persona)
        self.boton_agregar_nombre.pack(pady=5)

        # Label Total
        self.label_total_general = ctk.CTkLabel(self.ventana, text="Total general: $0")
        self.label_total_general.pack(pady=5)
        self.mostrar_total_general()


        # Ejecutar app
        self.ventana.mainloop()

    def mostrar_total_general(self):
        total = sum(pago["valor"] for persona in self.personas for pago in persona["pagos"])
        total_formateado = formatear_con_puntos(total)
        self.label_total_general.configure(text=f"Total general: ${total_formateado}")


    def mostrar_suma(self, *args):
        nombre_seleccionado = self.combo_nombres.get()
        for persona in self.personas:
            if persona["nombre"] == nombre_seleccionado:
                suma = sum(p["valor"] for p in persona["pagos"])
                suma_formateada = formatear_con_puntos(suma)
                self.label_resultado.configure(text=f"Suma de pagos: ${suma_formateada}")
                break

    def agregar_pago(self):
        nombre = self.combo_nombres.get()
        monto_texto = self.entry_pago.get()

        if not monto_texto.isdigit():
            self.label_resultado.configure(text="Ingrese un monto válido")
            return

        monto = int(monto_texto)
        repo.agregar_pago(nombre, monto)
        self.personas = repo.cargar_datos()
        self.mostrar_suma()
        self.mostrar_total_general()


    def agregar_persona(self):
        nuevo_nombre = self.entry_nuevo_nombre.get().strip()

        if not nuevo_nombre:
            self.label_resultado.configure(text="Ingrese un nombre válido")
            return

        if any(p["nombre"] == nuevo_nombre for p in self.personas):
            self.label_resultado.configure(text="La persona ya existe")
            return

        # Añadir a la lista
        repo.crear_persona(nuevo_nombre)
        self.personas = repo.cargar_datos()

        # Actualizar ComboBox
        self.combo_nombres.configure(values=[p["nombre"] for p in self.personas])
        self.entry_nuevo_nombre.delete(0, 'end')
        self.label_resultado.configure(text=f"{nuevo_nombre} añadido correctamente")
        self.mostrar_total_general()


