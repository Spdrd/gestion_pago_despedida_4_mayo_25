import tkinter as tk
from tkinter import ttk
import repo
from utils import formatear_con_puntos

class Pantalla:

    def __init__(self):
        # Cargar datos
        self.personas = repo.cargar_datos()

        # Crear ventana
        self.ventana = tk.Tk()
        self.ventana.title("Suma de Pagos desde JSON")
        self.ventana.geometry("320x360")

        # Instrucción
        self.label_instruccion = tk.Label(self.ventana, text="Seleccione una persona:")
        self.label_instruccion.pack(pady=5)

        # ComboBox
        nombres = [p["nombre"] for p in self.personas]
        self.combo_nombres = ttk.Combobox(self.ventana, values=nombres, state="readonly")
        self.combo_nombres.pack(pady=5)
        self.combo_nombres.bind("<<ComboboxSelected>>", self.mostrar_suma)

        # Resultado
        self.label_resultado = tk.Label(self.ventana, text="Suma de pagos: $0")
        self.label_resultado.pack(pady=10)

        # Entrada de nuevo pago
        self.label_nuevo_pago = tk.Label(self.ventana, text="Añadir nuevo pago:")
        self.label_nuevo_pago.pack()
        self.entry_pago = tk.Entry(self.ventana)
        self.entry_pago.pack(pady=5)

        # Botón para agregar pago
        self.boton_agregar = tk.Button(self.ventana, text="Agregar Pago", command=self.agregar_pago)
        self.boton_agregar.pack(pady=5)

        # Separador
        tk.Label(self.ventana, text="").pack()

        # Entrada para nuevo nombre
        self.label_nuevo_nombre = tk.Label(self.ventana, text="Añadir nueva persona:")
        self.label_nuevo_nombre.pack()
        self.entry_nuevo_nombre = tk.Entry(self.ventana)
        self.entry_nuevo_nombre.pack(pady=5)

        # Botón para agregar persona
        self.boton_agregar_nombre = tk.Button(self.ventana, text="Agregar Persona", command=self.agregar_persona)
        self.boton_agregar_nombre.pack(pady=5)

        # Ejecutar app
        self.ventana.mainloop()

    def mostrar_suma(self, *args):
        nombre_seleccionado = self.combo_nombres.get()
        for persona in self.personas:
            if persona["nombre"] == nombre_seleccionado:
                suma = sum(p["valor"] for p in persona["pagos"])
                suma_formateada = formatear_con_puntos(suma)
                self.label_resultado.config(text=f"Suma de pagos: ${suma_formateada}")
                break

    def agregar_pago(self):
        nombre = self.combo_nombres.get()
        monto_texto = self.entry_pago.get()

        if not monto_texto.isdigit():
            self.label_resultado.config(text="Ingrese un monto válido")
            return

        monto = int(monto_texto)
        repo.agregar_pago(nombre, monto)
        self.personas = repo.cargar_datos()
        self.mostrar_suma()

    def agregar_persona(self):
        nuevo_nombre = self.entry_nuevo_nombre.get().strip()

        if not nuevo_nombre:
            self.label_resultado.config(text="Ingrese un nombre válido")
            return

        if any(p["nombre"] == nuevo_nombre for p in self.personas):
            self.label_resultado.config(text="La persona ya existe")
            return

        # Añadir a la lista
        repo.crear_persona(nuevo_nombre)
        self.personas = repo.cargar_datos()

        # Actualizar ComboBox
        self.combo_nombres['values'] = [p["nombre"] for p in self.personas]
        self.entry_nuevo_nombre.delete(0, tk.END)
        self.label_resultado.config(text=f"{nuevo_nombre} añadido correctamente")
