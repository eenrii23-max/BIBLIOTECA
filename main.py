"""Punto de entrada: junta los tres componentes y ofrece un menú por consola."""

from catalogo import Catalogo
from socios import Socios
from prestamos import Prestamos


def crear_datos_demo(catalogo):
    catalogo.agregar("Don Quijote de la Mancha", "Cervantes", 2)
    catalogo.agregar("Cien años de soledad", "García Márquez", 1)
    catalogo.agregar("La sombra del viento", "Ruiz Zafón", 3)
    catalogo.agregar("El principito", "Saint-Exupéry", 1)


def pedir_numero(texto):
    try:
        return int(input(texto))
    except ValueError:
        print("Introduce un número válido.")
        return None


def menu():
    print("\n=== BIBLIOTECA DE BARRIO ===")
    print("1. Buscar libro")
    print("2. Dar de alta socio")
    print("3. Hacer préstamo")
    print("4. Devolver libro")
    print("5. Reservar libro prestado")
    print("6. Ver préstamos de un socio")
    print("0. Salir")
    return input("Elige una opción: ").strip()


def main():
    catalogo = Catalogo()
    socios = Socios()
    prestamos = Prestamos(catalogo, socios)  # se le entregan los componentes
    crear_datos_demo(catalogo)

    while True:
        opcion = menu()
        if opcion == "1":
            texto = input("Título (o parte): ")
            resultados = catalogo.buscar(texto)
            if not resultados:
                print("Sin resultados.")
            for libro in resultados:
                print(libro)
        elif opcion == "2":
            try:
                socio = socios.alta(input("Nombre del socio: "))
                print(f"Socio creado: {socio}")
            except ValueError as e:
                print(e)
        elif opcion == "3":
            id_socio = pedir_numero("ID del socio: ")
            id_libro = pedir_numero("ID del libro: ")
            if id_socio and id_libro:
                _, mensaje = prestamos.prestar(id_socio, id_libro)
                print(mensaje)
        elif opcion == "4":
            id_prestamo = pedir_numero("ID del préstamo: ")
            if id_prestamo:
                _, mensaje = prestamos.devolver(id_prestamo)
                print(mensaje)
        elif opcion == "5":
            id_socio = pedir_numero("ID del socio: ")
            id_libro = pedir_numero("ID del libro: ")
            if id_socio and id_libro:
                _, mensaje = prestamos.reservar(id_socio, id_libro)
                print(mensaje)
        elif opcion == "6":
            id_socio = pedir_numero("ID del socio: ")
            if id_socio:
                lista = prestamos.activos_de(id_socio)
                if not lista:
                    print("Sin préstamos activos.")
                for p in lista:
                    libro = catalogo.obtener(p.id_libro)
                    print(f"Préstamo {p.id}: {libro.titulo} (vence {p.vence})")
        elif opcion == "0":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
