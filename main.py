from customtkinter import *
from tkinter import ttk
from sqlite3 import *

import sqlite3
# Conectar o crear la base de datos
loco = sqlite3.connect("elChino.db")
cur = loco.cursor()

# Crear tabla de palabras
cur.execute("""
CREATE TABLE IF NOT EXISTS palabras (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 palabra TEXT NOT NULL,
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

