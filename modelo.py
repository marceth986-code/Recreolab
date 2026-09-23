import json
import os


class Producto:

    def __init__(self, codigo, nombre, precio, stock, categoria="General"):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria

    def __repr__(self):
        return f"{self.codigo}: {self.nombre} (${self.precio})"


def catalogo_inicial():
    return [
       Producto("A01", "Agua Mineral", 1000, 8, "Bebidas"),
        Producto("A02", "Jugo de Naranja", 1200, 6, "Bebidas"),
        Producto("A03", "Alfajor de Chocolate", 800, 10, "Snacks"),
        Producto("A04", "Galletitas Dulces", 900, 2, "Snacks"),
        Producto("A05", "Barrita de Cereal", 700, 5, "Snacks"),
        Producto("A06", "Coca Cola", 1500, 10, "Bebidas"),
        Producto("A07", "Pepsi", 1400, 8, "Bebidas"),
        Producto("A08", "Chicle de Menta", 400, 15, "Golosinas"),
        Producto("A09", "Gaseosa Goliat", 1100, 7, "Bebidas"),
        Producto("A10", "Cheetos", 1300, 6, "Snacks"),
        Producto("A11", "Turrón de Maní", 500, 12, "Golosinas"),
        Producto("A12", "Papas Fritas", 1600, 5, "Snacks"),
        Producto("A13", "Caramelos Mogul", 600, 20, "Golosinas"),
        Producto("A14", "Chocolatina", 1000, 9, "Golosinas"),
        Producto("A15", "Maní Salado", 800, 11, "Snacks"),
    ]


def buscar(productos, codigo):
    for producto in productos:
        if producto.codigo == codigo:
            return producto
    raise ValueError("El producto no existe.")


def cantidad_en_carrito(carrito, codigo):
    cantidad = 0
    for producto in carrito:
        if producto.codigo == codigo:
            cantidad += 1
    return cantidad


def total_carrito(carrito):
    total = 0
    for producto in carrito:
        total += producto.precio
    return total


def agregar(productos, carrito, codigo):
    producto = buscar(productos, codigo)
    if cantidad_en_carrito(carrito, codigo) >= producto.stock:
        raise ValueError("No queda stock suficiente para agregar otra unidad.")
    carrito.append(producto)


def quitar_producto(carrito, codigo):
    for i, producto in enumerate(carrito):
        if producto.codigo == codigo:
            carrito.pop(i)
            return
    raise ValueError("El producto no está en el carrito.")


def confirmar(carrito, ventas):
    if not carrito:
        raise ValueError("El carrito está vacío.")

    total = total_carrito(carrito)
    for producto in carrito:
        producto.stock -= 1

    ventas.append(total)
    carrito.clear()
    return total


def sugerir_pares(productos, presupuesto):
    if presupuesto <= 0:
        raise ValueError("El presupuesto debe ser mayor que cero.")

    opciones = []
    for i in range(len(productos)):
        for j in range(i + 1, len(productos)):
            primero = productos[i]
            segundo = productos[j]
            total = primero.precio + segundo.precio

            if primero.stock > 0 and segundo.stock > 0:
                if total <= presupuesto:
                    opciones.append(
                        [
                            primero.nombre,
                            segundo.nombre,
                            total,
                            presupuesto - total,
                        ]
                    )

    return opciones