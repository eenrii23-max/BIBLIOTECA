"""Componente Socios: guarda los socios y sus sanciones.

No conoce a Catalogo ni a Prestamos.
"""

from datetime import date, timedelta


class Socio:
    """Persona con identidad (id) y estado (sanción)."""

    def __init__(self, id_socio, nombre):
        self.id = id_socio
        self.nombre = nombre
        self.sancionado_hasta = None  # None = sin sanción

    def esta_sancionado(self, hoy=None):
        hoy = hoy or date.today()
        return self.sancionado_hasta is not None and hoy <= self.sancionado_hasta

    def __str__(self):
        extra = f" (sancionado hasta {self.sancionado_hasta})" if self.esta_sancionado() else ""
        return f"[{self.id}] {self.nombre}{extra}"


class Socios:
    def __init__(self):
        self._socios = {}

    def alta(self, nombre):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        id_socio = len(self._socios) + 1
        socio = Socio(id_socio, nombre)
        self._socios[id_socio] = socio
        return socio

    def obtener(self, id_socio):
        """Devuelve el Socio o None."""
        return self._socios.get(id_socio)

    def esta_sancionado(self, id_socio, hoy=None):
        socio = self.obtener(id_socio)
        return socio is not None and socio.esta_sancionado(hoy)

    def sancionar(self, id_socio, dias, hoy=None):
        """Sanciona al socio durante N días a partir de hoy."""
        socio = self.obtener(id_socio)
        if socio is None:
            return False
        hoy = hoy or date.today()
        socio.sancionado_hasta = hoy + timedelta(days=dias)
        return True
