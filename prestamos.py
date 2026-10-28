"""Componente Prestamos: aplica las reglas de la biblioteca.

Depende de Catalogo y Socios, pero SOLO usa sus funciones públicas
(obtener, disponibles, marcar_prestado, marcar_devuelto, esta_sancionado,
sancionar). Nunca toca sus listas internas.
"""

from datetime import date, timedelta

MAX_LIBROS_POR_SOCIO = 2
DIAS_PRESTAMO = 7
DIAS_SANCION = 7  # por devolver tarde


class Prestamo:
    """Un préstamo concreto: identidad (id) y estado (devuelto o no)."""

    def __init__(self, id_prestamo, id_socio, id_libro, id_ejemplar, desde):
        self.id = id_prestamo
        self.id_socio = id_socio
        self.id_libro = id_libro
        self.id_ejemplar = id_ejemplar
        self.desde = desde
        self.vence = desde + timedelta(days=DIAS_PRESTAMO)
        self.devuelto = False

    def esta_vencido(self, hoy):
        return not self.devuelto and hoy > self.vence


class Prestamos:
    def __init__(self, catalogo, socios):
        self._catalogo = catalogo
        self._socios = socios
        self._prestamos = {}
        self._reservas = {}  # id_libro -> [id_socio, ...] (cola)

    # ---------- consultas ----------
    def activos_de(self, id_socio):
        return [p for p in self._prestamos.values()
                if p.id_socio == id_socio and not p.devuelto]

    def reservas_de(self, id_libro):
        return list(self._reservas.get(id_libro, []))

    # ---------- reglas ----------
    def _puede_pedir(self, id_socio, id_libro, hoy):
        """Devuelve (ok, motivo)."""
        if self._socios.obtener(id_socio) is None:
            return False, "El socio no existe"
        if self._catalogo.obtener(id_libro) is None:
            return False, "El libro no existe"
        if self._socios.esta_sancionado(id_socio, hoy):
            return False, "El socio está sancionado"
        if len(self.activos_de(id_socio)) >= MAX_LIBROS_POR_SOCIO:
            return False, f"Máximo {MAX_LIBROS_POR_SOCIO} libros a la vez"
        return True, ""

    def prestar(self, id_socio, id_libro, hoy=None):
        """Devuelve (Prestamo | None, mensaje)."""
        hoy = hoy or date.today()
        ok, motivo = self._puede_pedir(id_socio, id_libro, hoy)
        if not ok:
            return None, motivo

        libres = self._catalogo.disponibles(id_libro)
        if libres == 0:
            return None, "No hay ejemplares libres. Puedes reservarlo."

        # Respetar la cola de reservas
        cola = self._reservas.get(id_libro, [])
        if cola:
            if id_socio in cola:
                if cola.index(id_socio) >= libres:
                    return None, "Hay reservas por delante de ti"
            elif libres <= len(cola):
                return None, "Los ejemplares libres están reservados"

        id_ejemplar = self._catalogo.marcar_prestado(id_libro)
        if id_ejemplar is None:
            return None, "No se pudo prestar el ejemplar"
        if id_socio in cola:
            cola.remove(id_socio)

        prestamo = Prestamo(len(self._prestamos) + 1, id_socio, id_libro,
                            id_ejemplar, hoy)
        self._prestamos[prestamo.id] = prestamo
        return prestamo, f"Préstamo creado. Devolver antes del {prestamo.vence}"

    def devolver(self, id_prestamo, hoy=None):
        """Devuelve (ok, mensaje). Sanciona si hay retraso."""
        hoy = hoy or date.today()
        prestamo = self._prestamos.get(id_prestamo)
        if prestamo is None or prestamo.devuelto:
            return False, "Préstamo no encontrado o ya devuelto"
        self._catalogo.marcar_devuelto(prestamo.id_libro, prestamo.id_ejemplar)
        prestamo.devuelto = True
        if hoy > prestamo.vence:
            self._socios.sancionar(prestamo.id_socio, DIAS_SANCION, hoy)
            return True, f"Devuelto con retraso: sancionado {DIAS_SANCION} días"
        return True, "Devuelto a tiempo"

    def reservar(self, id_socio, id_libro, hoy=None):
        """Reserva un libro que no tiene ejemplares libres."""
        hoy = hoy or date.today()
        ok, motivo = self._puede_pedir(id_socio, id_libro, hoy)
        if not ok:
            return False, motivo
        if self._catalogo.disponibles(id_libro) > 0:
            return False, "Hay ejemplares libres, pídelo prestado directamente"
        cola = self._reservas.setdefault(id_libro, [])
        if id_socio in cola:
            return False, "Ya tienes una reserva de este libro"
        cola.append(id_socio)
        return True, f"Reserva hecha. Posición en la cola: {len(cola)}"
