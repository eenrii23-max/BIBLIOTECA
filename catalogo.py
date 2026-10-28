"""Componente Catalogo: guarda libros y sus ejemplares.

No conoce a Socios ni a Prestamos.
"""

DISPONIBLE = "disponible"
PRESTADO = "prestado"


class Ejemplar:
    """Una copia física de un libro, con su propio estado."""

    def __init__(self, id_ejemplar, estado=DISPONIBLE):
        self.id = id_ejemplar
        self.estado = estado


class Libro:
    """Un título (identidad: id) con varios ejemplares (estado)."""

    def __init__(self, id_libro, titulo, autor, num_ejemplares=1):
        self.id = id_libro
        self.titulo = titulo
        self.autor = autor
        self.ejemplares = [
            Ejemplar(f"{id_libro}-{n}") for n in range(1, num_ejemplares + 1)
        ]

    def disponibles(self):
        return [e for e in self.ejemplares if e.estado == DISPONIBLE]

    def __str__(self):
        return (f"[{self.id}] {self.titulo} - {self.autor} "
                f"({len(self.disponibles())}/{len(self.ejemplares)} disponibles)")


class Catalogo:
    def __init__(self):
        self._libros = {}  # privado: nadie fuera debe tocarlo

    def agregar(self, titulo, autor, num_ejemplares=1):
        id_libro = len(self._libros) + 1
        libro = Libro(id_libro, titulo, autor, num_ejemplares)
        self._libros[id_libro] = libro
        return libro

    def buscar(self, titulo):
        """Devuelve los libros cuyo título contiene el texto (sin mayúsculas)."""
        texto = titulo.strip().lower()
        return [l for l in self._libros.values() if texto in l.titulo.lower()]

    def obtener(self, id_libro):
        """Devuelve el Libro o None si no existe."""
        return self._libros.get(id_libro)

    def disponibles(self, id_libro):
        """Número de ejemplares libres de un libro."""
        libro = self.obtener(id_libro)
        return len(libro.disponibles()) if libro else 0

    def marcar_prestado(self, id_libro):
        """Marca un ejemplar libre como prestado y devuelve su id (o None)."""
        libro = self.obtener(id_libro)
        if libro is None:
            return None
        libres = libro.disponibles()
        if not libres:
            return None
        libres[0].estado = PRESTADO
        return libres[0].id

    def marcar_devuelto(self, id_libro, id_ejemplar):
        libro = self.obtener(id_libro)
        if libro is None:
            return False
        for e in libro.ejemplares:
            if e.id == id_ejemplar and e.estado == PRESTADO:
                e.estado = DISPONIBLE
                return True
        return False
