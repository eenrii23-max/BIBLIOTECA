# Diario de decisiones

## Petición del cliente: «Que Prestamos lea directamente la lista de libros de Catalogo»

**Decisión: NO lo hago.** Si Prestamos leyera la lista interna de Catalogo, quedaría atado a cómo Catalogo guarda los datos y cualquier cambio (por ejemplo, pasar de lista a base de datos) rompería Prestamos. En su lugar, Prestamos usa solo las funciones públicas `obtener`, `disponibles`, `marcar_prestado` y `marcar_devuelto`, que son igual de rápidas de llamar y mantienen los componentes independientes.

## Otras decisiones

- Cada título (`Libro`) tiene varios `Ejemplar`, cada uno con su propio estado (disponible/prestado).
- Una devolución tardía sanciona al socio 7 días.
- Las reservas son una cola por libro: si hay reservas, los ejemplares libres se guardan para quienes están primeros en la cola.
