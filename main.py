from customtkinter import *
from tkinter import ttk, messagebox
import sqlite3

# Base de datos
def obtener():
    loco = sqlite3.connect("elChino.db")
    cr = loco.cursor()
    cr.execute("SELECT * FROM productos")
    productos = cr.fetchall()
    loco.close()
    return productos

def agregar(nombre, precio, stock):
    loco = sqlite3.connect("elChino.db")
    cr = loco.cursor()
    cr.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", (nombre, precio, stock))
    loco.commit()
    loco.close()

def eliminar(id):
    loco = sqlite3.connect("elChino.db")
    cr = loco.cursor()
    cr.execute("DELETE FROM productos WHERE id = ?", (id,))
    loco.commit()
    loco.close()

def actualizar(id, nombre=None, precio=None, stock=None):
    loco = sqlite3.connect("elChino.db")
    cr = loco.cursor()
    if nombre is not None and precio is not None and stock is not None:
        cr.execute("UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?", (nombre, precio, stock, id))
    elif nombre is not None:
        cr.execute("UPDATE productos SET nombre = ? WHERE id = ?", (nombre, id))
    elif precio is not None:
        cr.execute("UPDATE productos SET precio = ? WHERE id = ?", (precio, id))
    elif stock is not None:
        cr.execute("UPDATE productos SET stock = ? WHERE id = ?", (stock, id))
    loco.commit()
    loco.close()

# Configuración inicial
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Tienda de Don Pepe")
        self.geometry("700x500")
        self.resizable(False, False)

        # Tabla
        self.tabla = ttk.Treeview(self, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
        for col in ("ID", "Nombre", "Precio", "Stock"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center")
        self.tabla.pack(pady=20, fill="x", padx=20)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.place(x=670, y=60, height=210)

        # Botones principales
        btn_frame = CTkFrame(self)
        btn_frame.pack(pady=10)

        btn_agregar = CTkButton(btn_frame, text="Agregar", width=100, command=self.open_agregar)
        btn_agregar.grid(row=0, column=0, padx=5)
        btn_eliminar = CTkButton(btn_frame, text="Eliminar", width=100, command=self.open_eliminar)
        btn_eliminar.grid(row=0, column=1, padx=5)
        btn_modificar = CTkButton(btn_frame, text="Modificar", width=100, command=self.open_modificar)
        btn_modificar.grid(row=0, column=2, padx=5)

        self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for producto in obtener():
            self.tabla.insert("", "end", values=producto)

    def open_agregar(self):
        AgregarVentana(self)

    def open_eliminar(self):
        EliminarVentana(self)

    def open_modificar(self):
        ModificarVentana(self)

# Ventana Agregar
class AgregarVentana(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Agregar Producto")
        self.geometry("300x250")
        self.parent = parent

        self.nombre_var = StringVar()
        self.precio_var = StringVar()
        self.stock_var = StringVar()

        CTkLabel(self, text="Nombre:").pack(pady=5)
        self.nombre_entry = CTkEntry(self, textvariable=self.nombre_var)
        self.nombre_entry.pack(pady=5)

        CTkLabel(self, text="Precio:").pack(pady=5)
        self.precio_entry = CTkEntry(self, textvariable=self.precio_var)
        self.precio_entry.pack(pady=5)

        CTkLabel(self, text="Stock:").pack(pady=5)
        self.stock_entry = CTkEntry(self, textvariable=self.stock_var)
        self.stock_entry.pack(pady=5)

        btn_frame = CTkFrame(self)
        btn_frame.pack(pady=10)

        CTkButton(btn_frame, text="Cancelar", command=self.destroy).grid(row=0, column=0, padx=5)
        CTkButton(btn_frame, text="Agregar", command=self.agregar_producto).grid(row=0, column=1, padx=5)

    def agregar_producto(self):
        nombre = self.nombre_var.get()
        precio = self.precio_var.get()
        stock = self.stock_var.get()

        if nombre and precio and stock:
            try:
                precio = float(precio)
                stock = int(stock)
                agregar(nombre, precio, stock)
                self.parent.actualizar_tabla()
                self.destroy()
            except ValueError:
                messagebox.showerror("Error", "Precio debe ser un número y Stock un entero.")
        else:
            messagebox.showwarning("Campos incompletos", "Complete todos los campos.")

# Ventana Eliminar
class EliminarVentana(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Eliminar Producto")
        self.geometry("300x150")
        self.parent = parent

        self.id_var = StringVar()

        CTkLabel(self, text="ID del producto:").pack(pady=10)
        self.id_entry = CTkEntry(self, textvariable=self.id_var)
        self.id_entry.pack(pady=5)

        btn_frame = CTkFrame(self)
        btn_frame.pack(pady=10)

        CTkButton(btn_frame, text="Cancelar", command=self.destroy).grid(row=0, column=0, padx=5)
        CTkButton(btn_frame, text="Eliminar", command=self.eliminar_producto).grid(row=0, column=1, padx=5)

    def eliminar_producto(self):
        id = self.id_var.get()
        if id:
            try:
                id = int(id)
                eliminar(id)
                self.parent.actualizar_tabla()
                self.destroy()
            except ValueError:
                messagebox.showerror("Error", "ID debe ser un número entero.")
        else:
            messagebox.showwarning("Campo vacío", "Ingrese el ID del producto.")

# Ventana Modificar (elige qué campo modificar)
class ModificarVentana(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("¿Qué quieres modificar?")
        self.geometry("300x200")
        self.parent = parent

        CTkLabel(self, text="¿Qué quieres modificar?").pack(pady=10)

        CTkButton(self, text="Stock", command=self.modificar_stock).pack(pady=5)
        CTkButton(self, text="Nombre", command=self.modificar_nombre).pack(pady=5)
        CTkButton(self, text="Precio", command=self.modificar_precio).pack(pady=5)
        CTkButton(self, text="Cancelar", command=self.destroy).pack(pady=5)

    def modificar_stock(self):
        ModificarCampo(self, "Stock", "nuevo stock").grab_set()
        self.destroy()

    def modificar_nombre(self):
        ModificarCampo(self, "Nombre", "nuevo nombre").grab_set()
        self.destroy()

    def modificar_precio(self):
        ModificarCampo(self, "Precio", "nuevo precio").grab_set()
        self.destroy()

# Ventana para modificar un campo específico
class ModificarCampo(CTkToplevel):
    def __init__(self, parent, campo, titulo):
        super().__init__(parent)
        self.title(f"Modificar {campo}")
        self.geometry("300x200")
        self.parent = parent.master  # para llamar a actualizar_tabla()

        self.id_var = StringVar()
        self.valor_var = StringVar()

        CTkLabel(self, text=f"{titulo}:").pack(pady=10)
        self.valor_entry = CTkEntry(self, textvariable=self.valor_var)
        self.valor_entry.pack(pady=5)

        CTkLabel(self, text="ID del producto a modificar:").pack(pady=10)
        self.id_entry = CTkEntry(self, textvariable=self.id_var)
        self.id_entry.pack(pady=5)

        btn_frame = CTkFrame(self)
        btn_frame.pack(pady=10)

        CTkButton(btn_frame, text="Cancelar", command=self.destroy).grid(row=0, column=0, padx=5)
        CTkButton(btn_frame, text="OK", command=self.modificar_valor).grid(row=0, column=1, padx=5)

        self.campo = campo

    def modificar_valor(self):
        valor = self.valor_var.get()
        id = self.id_var.get()
        if valor and id:
            try:
                id = int(id)
                if self.campo == "Stock":
                    valor = int(valor)
                    actualizar(id, stock=valor)
                elif self.campo == "Precio":
                    valor = float(valor)
                    actualizar(id, precio=valor)
                elif self.campo == "Nombre":
                    actualizar(id, nombre=valor)
                self.parent.actualizar_tabla()
                self.destroy()
            except ValueError:
                messagebox.showerror("Error", "Verifica que los valores sean correctos.")
        else:
            messagebox.showwarning("Campos incompletos", "Complete todos los campos.")

if __name__ == "__main__":
    # Crear tabla si no existe (como en tu código original)
    loco = sqlite3.connect("elChino.db")
    cur = loco.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)
    loco.commit()
    loco.close()

    app = App()
    app.mainloop()












