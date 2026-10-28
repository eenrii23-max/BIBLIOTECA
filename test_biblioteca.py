from datetime import date, timedelta
from catalogo import Catalogo
from socios import Socios
from prestamos import Prestamos

c, s = Catalogo(), Socios()
p = Prestamos(c, s)
q = c.agregar("Quijote", "Cervantes", 2)
b = c.agregar("Principito", "Saint", 1)
d = c.agregar("Sombra", "Zafon", 1)
a, o, e = s.alta("Ana"), s.alta("Oscar"), s.alta("Eva")
hoy = date(2026, 10, 28)

# 2 ejemplares independientes
assert p.prestar(a.id, q.id, hoy)[0] is not None
assert p.prestar(o.id, q.id, hoy)[0] is not None
assert c.disponibles(q.id) == 0
# máx 2 libros
assert p.prestar(a.id, b.id, hoy)[0] is not None
pr, msg = p.prestar(a.id, d.id, hoy)
assert pr is None and "Máximo" in msg
# caduca a los 7 días
assert p.activos_de(a.id)[0].vence == hoy + timedelta(days=7)
# reserva de libro prestado
assert p.reservar(e.id, b.id, hoy)[0]
assert not p.reservar(e.id, b.id, hoy)[0]
# la reserva bloquea a otros
assert p.devolver(3, hoy)[0]   # Ana devuelve Principito
assert p.prestar(o.id, b.id, hoy)[0] is None
assert p.prestar(e.id, b.id, hoy)[0] is not None
# sanción por retraso
ok, msg = p.devolver(1, hoy + timedelta(days=9))
assert "sancionado" in msg and s.esta_sancionado(a.id, hoy + timedelta(days=9))
pr, msg = p.prestar(a.id, d.id, hoy + timedelta(days=9))
assert pr is None and "sancionado" in msg
print("TODAS LAS PRUEBAS OK")
