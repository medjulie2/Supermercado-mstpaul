# bethel medjulie stpaul 3d lunes 17 noviembre, programacion y base de datos
def productosMasCaro(productos):
  masCaro = ""
  precioMasAlto = 0
  for linea in productos:
    registro = linea.strip().split(",")
    #print registro
    nombre = registro[1]
    precio = float(registro[2])
    if precio > precioMasAlto:
      precioMasAlto = precio
      masCaro = nombre
  return masCaro# Se abre el archivo y se llama a la función que crearon
with open('productos.csv', 'r') as productos:
  productoMasCaro(productos)
  def valorTotalBodega(productos):
    import csv   # Importamos la librería csv para leer archivos separados por comas

    total = 0  # Aquí acumularemos el valor total de todo lo que hay en bodega

    # Abrimos el archivo recibido en modo lectura
    with open(productos, "r", encoding="utf-8") as file:
        lector = csv.reader(file, delimiter=",")  # Indicamos que el separador es coma

        # Recorremos cada fila del archivo
        for fila in lector:
            # Cada fila tiene: [id_producto, nombre, precio, cantidad]

            precio = float(fila[2])            # Convertimos el precio a número (float)
            cantidad = int(fila[3])            # Convertimos la cantidad a número entero

            total += precio * cantidad         # Sumamos al total (precio por cantidad)

    return total   # Al final devolvemos el total calculado
# Se abre el archivo y se llama a la función que crearon
with open('productos.csv', 'r') as productos:
  valorTotalBodega(productos)def productoConMasIngresos(archivo_items, archivo_productos):
    """
    Recibe los paths de los archivos de items y productos,
    y devuelve el nombre del producto que ha generado más ingresos totales.
    """

    # Leer productos
    productos = {}
    with open(archivo_productos, 'r', encoding='utf-8') as f:
        for linea in f.readlines()[1:]:
            datos = linea.strip().split(';')
            productos[datos[0]] = {'nombre': datos[1], 'precio': float(datos[2])}

    # Calcular ingresos por producto
    ingresos = {}
    with open(archivo_items, 'r', encoding='utf-8') as f:
        for linea in f.readlines()[1:]:
            datos = linea.strip().split(';')
            id_prod = datos[1]
            cantidad = int(datos[2])

            if id_prod in productos:
                ingreso = productos[id_prod]['precio'] * cantidad
                ingresos[id_prod] = ingresos.get(id_prod, 0) + ingreso

    # Retornar nombre del producto con más ingresos
    id_max = max(ingresos, key=ingresos.get)
    return productos[id_max]['nombre']
with open('productos.csv', 'r') as productos:
  with open('items.csv', 'r') as items:
    productoConMasIngresos(items, productos)def totalVentasDelMes(año, mes, items, productos, ventas):
  # Su código aquí
  def totalVentasDelMes(archivo_items, archivo_productos, archivo_ventas, mes, año):
    import csv
    from datetime import datetime

    # 1. Cargar precios de los productos en un diccionario
    precios = {}
    with open(archivo_productos, encoding="utf-8") as prod_file:
        lector = csv.reader(prod_file, delimiter=";")
        next(lector)  # saltar encabezado
        for id_prod, nombre, precio, cant_bod in lector:
            precios[id_prod] = float(precio)

    # 2. Identificar qué boletas pertenecen al mes y año solicitado
    ventas_validas = set()
    with open(archivo_ventas, encoding="utf-8") as ventas_file:
        lector = csv.reader(ventas_file, delimiter=";")
        next(lector)
        for num_boleta, fecha, rut in lector:
            # Detectar formato de fecha
            if "-" in fecha:
                partes = fecha.split("-")
                if len(partes[0]) == 4:      # yyyy-mm-dd
                    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
                else:                        # dd-mm-yyyy
                    fecha_dt = datetime.strptime(fecha, "%d-%m-%Y")
            else:
                continue

            if fecha_dt.month == mes and fecha_dt.year == año:
                ventas_validas.add(num_boleta)

    # 3. Leer los items y sumar el total de ventas
    total = 0
    with open(archivo_items, encoding="utf-8") as items_file:
        lector = csv.reader(items_file, delimiter=";")
        next(lector)
        for num_boleta, id_producto, cantidad in lector:
            if num_boleta in ventas_validas:
                total += precios[id_producto] * int(cantidad)

    return total
with open('productos.csv', 'r') as productos:
  with open('items.csv', 'r') as items:
    with open('ventas.csv', 'r') as ventas:
      totalVentasDelMes(2010, 10, items, productos, ventas)
def crearInforme(archivo_productos, archivo_items, archivo_ventas, mes, año):
    # Se asume que las funciones ya están definidas:
    # productoMasCaro(), valorTotalBodega(), productoConMasIngresos(), totalVentasDelMes()

    nombre_mas_caro = productoMasCaro(archivo_productos)
    total_bodega = valorTotalBodega(archivo_productos)
    prod_mas_ingresos = productoConMasIngresos(archivo_items, archivo_productos)
    total_ventas_mes = totalVentasDelMes(archivo_items, archivo_productos, archivo_ventas, mes, año)

    # Construcción del texto del informe
    texto = (
        f"El producto más caro es {nombre_mas_caro}\n"
        f"El valor total de la bodega es de ${total_bodega}\n"
        f"El producto con más ingresos es {prod_mas_ingresos}\n"
        f"En el período de {mes}/{año}, el total de ventas es de ${total_ventas_mes}\n"
    )

    # Escritura del archivo
    with open("informe.txt", "w", encoding="utf-8") as f:
        f.write(texto)

    print("Informe generado exitosamente en 'informe.txt'")