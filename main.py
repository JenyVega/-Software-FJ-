"""Simulación de 12 operaciones de Software FJ (válidas e inválidas)."""
from gestor import GestorFJ
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def paso(n, texto):
    print(f"\n[{n:02d}] {texto}")


def main():
    g = GestorFJ()
    print("=== SOFTWARE FJ · Sistema de Gestión ===")

    paso(1, "Registrar cliente válido")
    ana = g.registrar_cliente("C001", "Ana Gómez", "ana@correo.com", "3101234567")
    paso(2, "Registrar cliente con correo inválido")
    g.registrar_cliente("C002", "Luis Pérez", "luis-sin-arroba", "3207654321")
    paso(3, "Registrar cliente con teléfono inválido")
    g.registrar_cliente("C003", "Marta Ruiz", "marta@correo.com", "12ab")
    paso(4, "Registrar segundo cliente válido")
    carlos = g.registrar_cliente("C004", "Carlos Díaz", "carlos@correo.com", "3001112233")

    paso(5, "Crear servicios válidos (sala, equipo, asesoría)")
    sala = g.registrar_servicio(ReservaSala, "S01", "Sala Innovación", 50000, 10)
    equipo = g.registrar_servicio(AlquilerEquipo, "S02", "Portátil Pro", 8000, 5)
    asesoria = g.registrar_servicio(AsesoriaEspecializada, "S03", "Asesoría Cloud", 90000, "Cloud")
    paso(6, "Crear servicio con tarifa negativa")
    g.registrar_servicio(ReservaSala, "S04", "Sala Fantasma", -100, 5)
    print("   · Tarifa no numérica (excepción encadenada):")
    g.registrar_servicio(ReservaSala, "S05", "Sala Rara", "abc", 5)

    paso(7, "Reserva exitosa de sala (confirmar + procesar)")
    r1 = g.crear_reserva("R001", ana, sala, 3, asistentes=8)
    g.confirmar(r1)
    g.procesar(r1)

    paso(8, "Reserva fallida: asistentes exceden la capacidad")
    g.crear_reserva("R002", ana, sala, 2, asistentes=30)

    paso(9, "Reserva de equipo con falta de parámetro 'cantidad'")
    g.crear_reserva("R003", carlos, equipo, 4)

    paso(10, "Reserva de asesoría senior con descuento de costo (confirmar + procesar)")
    r4 = g.crear_reserva("R004", carlos, asesoria, 2, nivel="senior")
    g.confirmar(r4)
    g.procesar(r4)
    print(f"   · Variantes: base=${asesoria.calcular_costo(2, nivel='senior'):,.2f} | "
          f"con IVA=${asesoria.costo_con_impuesto(2, nivel='senior'):,.2f} | "
          f"IVA+10% desc=${asesoria.costo_con_descuento(2, 0.10, nivel='senior'):,.2f}")

    paso(11, "Servicio no disponible y operación no permitida")
    equipo.disponible = False
    g.crear_reserva("R005", ana, equipo, 2, cantidad=1)
    g.cancelar(r1)            # cancelar una reserva ya procesada
    g.procesar(r4)            # procesar dos veces

    paso(12, "Cancelar reserva válida y reserva con cliente inexistente")
    r6 = g.crear_reserva("R006", carlos, sala, 1, asistentes=4)
    g.cancelar(r6)
    g.crear_reserva("R007", None, sala, 1, asistentes=4)

    print("\n=== RESUMEN ===")
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | Reservas: {len(g.reservas)}")
    for r in g.reservas:
        print(" ", r)
    print("\nEl sistema siguió funcionando ante todos los errores. Revise logs/sistema.log")


if __name__ == "__main__":
    main()
