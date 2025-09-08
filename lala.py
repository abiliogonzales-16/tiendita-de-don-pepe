import tkinter as tk
from tkinter import messagebox
import sqlite3

# --------------------- Base de datos ---------------------
def conectar_db():
    conn = sqlite3.connect("tienda.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def obtener_productos():
    conn = sqlite3.connect("tienda.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def agregar_producto(nombre, precio, stock):
    conn = sqlite3.connect("tienda.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", (nombre, precio, stock))
    conn.commit()
    conn.close()

def eliminar_producto(id_producto):
    conn = sqlite3.connect("tienda.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id_producto,))
    conn.commit()
    conn.close()

def modificar_producto(campo, nuevo_valor, id_producto):
    conn = sqlite3.connect("tienda.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE productos SET {campo} = ? WHERE id = ?", (nuevo_valor, id_producto))
    conn.commit()
    conn.close()

# --------------------- Interfaz ---------------------
class TiendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tienda de Don Pepe")
        self.mostrar_tabla()

    def mostrar_tabla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        productos = obtener_productos()

        tk.Label(self.root, text="ID | Nombre | Precio | Stock", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=4)

        if productos:
            for idx, producto in enumerate(productos, start=1):
                texto = f"{producto[0]} | {producto[1]} | {producto[2]} | {producto[3]}"
                tk.Label(self.root, text=texto).grid(row=idx, column=0, columnspan=4)
            fila_botones = idx + 1
        else:
            tk.Label(self.root, text="No hay productos registrados.").grid(row=1, column=0, columnspan=4)
            fila_botones = 2

        tk.Button(self.root, text="Agregar", command=self.ventana_agregar).grid(row=fila_botones, column=0)
        tk.Button(self.root, text="Eliminar", command=self.ventana_eliminar).grid(row=fila_botones, column=1)
        tk.Button(self.root, text="Modificar", command=self.ventana_modificar).grid(row=fila_botones, column=2)

    def ventana_agregar(self):
        win = tk.Toplevel()
        win.title("Agregar Producto")

        tk.Label(win, text="Nombre:").pack()
        nombre_entry = tk.Entry(win)
        nombre_entry.pack()

        tk.Label(win, text="Precio:").pack()
        precio_entry = tk.Entry(win)
        precio_entry.pack()

        tk.Label(win, text="Stock:").pack()
        stock_entry = tk.Entry(win)
        stock_entry.pack()

        def agregar():
            try:
                nombre = nombre_entry.get().strip()
                precio = float(precio_entry.get())
                stock = int(stock_entry.get())

                if not nombre:
                    raise ValueError("Nombre vacío")

                agregar_producto(nombre, precio, stock)
                win.destroy()
                self.mostrar_tabla()
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos. Verifica que todos los campos estén completos y correctos.")

        tk.Button(win, text="Agregar", command=agregar).pack()
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def ventana_eliminar(self):
        win = tk.Toplevel()
        win.title("Eliminar Producto")

        tk.Label(win, text="ID del producto a eliminar:").pack()
        id_entry = tk.Entry(win)
        id_entry.pack()

        def eliminar():
            try:
                id_producto = int(id_entry.get())
                eliminar_producto(id_producto)
                win.destroy()
                self.mostrar_tabla()
            except ValueError:
                messagebox.showerror("Error", "ID inválido. Debe ser un número entero.")

        tk.Button(win, text="Eliminar", command=eliminar).pack()
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def ventana_modificar(self):
        win = tk.Toplevel()
        win.title("¿Qué quieres modificar?")

        def ir_modificar(campo):
            win.destroy()
            self.ventana_modificar_campo(campo)

        tk.Button(win, text="Nombre", command=lambda: ir_modificar("nombre")).pack()
        tk.Button(win, text="Precio", command=lambda: ir_modificar("precio")).pack()
        tk.Button(win, text="Stock", command=lambda: ir_modificar("stock")).pack()
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

    def ventana_modificar_campo(self, campo):
        win = tk.Toplevel()
        win.title(f"Modificar {campo}")

        tk.Label(win, text="ID del producto a modificar:").pack()
        id_entry = tk.Entry(win)
        id_entry.pack()

        tk.Label(win, text=f"Nuevo {campo}:").pack()
        valor_entry = tk.Entry(win)
        valor_entry.pack()

        def modificar():
            try:
                id_producto = int(id_entry.get())
                nuevo_valor = valor_entry.get().strip()

                if campo == "precio":
                    nuevo_valor = float(nuevo_valor)
                elif campo == "stock":
                    nuevo_valor = int(nuevo_valor)
                elif campo == "nombre" and not nuevo_valor:
                    raise ValueError("Nombre vacío")

                modificar_producto(campo, nuevo_valor, id_producto)
                win.destroy()
                self.mostrar_tabla()
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos. Verifica que los campos estén correctos.")

        tk.Button(win, text="OK", command=modificar).pack()
        tk.Button(win, text="Cancelar", command=win.destroy).pack()

# --------------------- Ejecutar App ---------------------
if __name__ == "__main__":
    conectar_db()
    root = tk.Tk()
    app = TiendaApp(root)
    root.mainloop()
