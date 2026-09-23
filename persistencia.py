
import json
import os
from modelo import Producto, catalogo_inicial


ARCHIVO = "datos.json"


def guardar(productos, ventas):
    registros = []

    for producto in productos:
        registros.append([
            producto.codigo,
            producto.nombre,
            producto.precio,
            producto.stock,
            producto.categoria
        ])

    datos = [registros, ventas]

    temporal = "datos.tmp"

    with open(temporal, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)

    os.replace(temporal, ARCHIVO)


def cargar():
    if not os.path.exists(ARCHIVO):
        return catalogo_inicial(), []

    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list) or len(datos) != 2:
            raise ValueError("Estructura inválida.")

        registros_productos = datos[0]
        ventas = datos[1]

        if not isinstance(registros_productos, list):
            raise ValueError("Productos inválidos.")

        if not isinstance(ventas, list):
            raise ValueError("Ventas inválidas.")

        productos = []
        codigos = set()

        for registro in registros_productos:
            if not isinstance(registro, list) or len(registro) != 5:
                raise ValueError("Registro de producto inválido.")

            codigo, nombre, precio, stock, categoria = registro

            if codigo in codigos:
                raise ValueError("Hay códigos de producto repetidos.")

            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError("El nombre no puede estar vacío.")

            if not isinstance(precio, int) or precio <= 0:
                raise ValueError("El precio debe ser un entero positivo.")

            if not isinstance(stock, int) or stock < 0:
                raise ValueError("El stock debe ser un entero no negativo.")

            if not isinstance(categoria, str) or not categoria.strip():
                raise ValueError("La categoría no puede estar vacía.")

            codigos.add(codigo)

            productos.append(
                Producto(
                    codigo,
                    nombre,
                    precio,
                    stock,
                    categoria
                )
            )

        for venta in ventas:
            if not isinstance(venta, int) or venta <= 0:
                raise ValueError("Hay un importe de venta inválido.")

        return productos, ventas

    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Error al cargar datos.json: {error}")
        print("Se conservará el archivo dañado.")

        return catalogo_inicial(), []

