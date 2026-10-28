# Biblioteca de barrio

Aplicación en Python (consola) y versión web en JavaScript, con tres componentes independientes:
`catalogo.py`, `socios.py` y `prestamos.py`, unidos por `main.py`.

## Ejecutar la versión Python

```bash
python3 main.py
python3 test_biblioteca.py   # pruebas de las reglas
```

## Versión web

Abre `index.html` en el navegador, o visita la página publicada con GitHub Pages.

## Reglas implementadas

- Máximo 2 libros a la vez por socio.
- Cada préstamo caduca a los 7 días (devolver tarde sanciona 7 días).
- Cada título tiene varios ejemplares con su propio estado.
- Un socio sancionado no puede pedir libros.
- Se pueden reservar libros ya prestados (cola de reservas).

## Documentación

- `diagrama.svg`: componentes y dependencias.
- `DIARIO.md`: decisión sobre la petición del cliente.
