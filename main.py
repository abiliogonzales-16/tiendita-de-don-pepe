from customtkinter import *
from tkinter import ttk
import sqlite3

# Conectar o crear la base de datos
loco = sqlite3.connect("elChino.db")
cur = loco.cursor()

# Crear tabla de productos
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
print("Base de datos lista")

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

def actualizar(id, nombre, precio, stock):
    loco = sqlite3.connect("elChino.db")
    cr = loco.cursor()
    cr.execute("UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?", (nombre, precio, stock, id))
    loco.commit()
    loco.close()
print("Base de datos lista")

#Establece el modo oscuro para la interfaz
set_appearance_mode("dark")
#Establece el tema de color azul oscuro para la interfaz
set_default_color_theme("dark-blue")

app = CTk()
app.geometry("700x500")
app.title("Gestor de Productos")
app.resizable(False, False)
# app.iconbitmap("icono.ico")  # Comentado para evitar error si no existe el archivo
app.config(bg="#1a1a1a")
app.eval('tk::PlaceWindow . center')
app.grid_columnconfigure((0, 1, 2, 3), weight=1)
app.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
#Variables globales
nombre_var = StringVar()
precio_var = StringVar()
stock_var = StringVar()
id_var = StringVar()
#Funciones
def agregar_producto():
    nombre = nombre_var.get()
    precio = precio_var.get()
    stock = stock_var.get()
    if nombre and precio and stock:
        try:
            precio = float(precio)
            stock = int(stock)
            agregar(nombre, precio, stock)
            nombre_var.set("")
            precio_var.set("")
            stock_var.set("")
            actualizar_tabla()
        except ValueError:
            print("Precio debe ser un número y Stock debe ser un entero")
    else:
        print("Todos los campos son obligatorios")
def eliminar_producto():
    id = id_var.get()
    if id:
        try:
            id = int(id)
            eliminar(id)
            id_var.set("")
            actualizar_tabla()
        except ValueError:
            print("ID debe ser un número entero")
    else:
        print("El campo ID es obligatorio")
def actualizar_producto():
    id = id_var.get()
    nombre = nombre_var.get()
    precio = precio_var.get()
    stock = stock_var.get()
    if id and nombre and precio and stock:
        try:
            id = int(id)
            precio = float(precio)
            stock = int(stock)
            actualizar(id, nombre, precio, stock)
            id_var.set("")
            nombre_var.set("")
            precio_var.set("")
            stock_var.set("")
            actualizar_tabla()
        except ValueError:
            print("ID debe ser un entero, Precio debe ser un número y Stock debe ser un entero")
    else:
        print("Todos los campos son obligatorios")
def actualizar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)
    productos = obtener()
    for producto in productos:
        tabla.insert("", "end", values=producto)
#Widgets
#Etiquetas
titulo = CTkLabel(app, text="Gestor de Productos", font=("Arial", 20))
titulo.grid(row=0, column=0, columnspan=4, pady=10)
nombre_label = CTkLabel(app, text="Nombre:")
nombre_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
precio_label = CTkLabel(app, text="Precio:")
precio_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
stock_label = CTkLabel(app, text="Stock:")
stock_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
id_label = CTkLabel(app, text="ID:")
id_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
#Entradas
nombre_entry = CTkEntry(app, textvariable=nombre_var)
nombre_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
precio_entry = CTkEntry(app, textvariable=precio_var)
precio_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
stock_entry = CTkEntry(app, textvariable=stock_var)
stock_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
id_entry = CTkEntry(app, textvariable=id_var)
id_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
#Botones
agregar_btn = CTkButton(app, text="Agregar", command=agregar_producto)
agregar_btn.grid(row=1, column=2, padx=10, pady=5)
eliminar_btn = CTkButton(app, text="Eliminar", command=eliminar_producto)
eliminar_btn.grid(row=4, column=2, padx=10, pady=5)
actualizar_btn = CTkButton(app, text="Actualizar", command=actualizar_producto)
actualizar_btn.grid(row=4, column=3, padx=10, pady=5)
#Tabla
tabla = ttk.Treeview(app, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Precio", text="Precio")
tabla.heading("Stock", text="Stock")
tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
#Scrollbar
scrollbar = ttk.Scrollbar(app, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scrollbar.set)
scrollbar.grid(row=5, column=4, sticky="ns")
actualizar_tabla()
app.mainloop()