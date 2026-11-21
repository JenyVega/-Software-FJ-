"""Gestor central: administra las listas internas de clientes, servicios y reservas."""
import functools

from entidades import Cliente
from excepciones import ErrorSistemaFJ, ReservaInvalidaError
from logger_config import obtener_logger
from reserva import Reserva

log = obtener_logger()


def controlar_errores(func):
    """Captura cualquier error, lo registra en el log y mantiene el sistema activo."""
    @functools.wraps(func)
    def envoltura(*args, **kwargs):
        try:
            resultado = func(*args, **kwargs)
            log.info("OK: %s", func.__name__)
            return resultado
        except ErrorSistemaFJ as e:
            causa = f" (causa: {type(e.__cause__).__name__}: {e.__cause__})" if e.__cause__ else ""
            log.error("%s | %s: %s%s", func.__name__, type(e).__name__, e, causa)
            print(f"   ✘ {type(e).__name__}: {e}")
        except Exception as e:  # nunca debe caerse el programa
            log.critical("%s | ERROR INESPERADO %s: %s", func.__name__, type(e).__name__, e)
            print(f"   ✘ Error inesperado ({type(e).__name__}): {e}")
        return None
    return envoltura


class GestorFJ:
    def __init__(self):
        self.clientes, self.servicios, self.reservas = [], [], []

    @controlar_errores
    def registrar_cliente(self, *datos):
        cliente = Cliente(*datos)
        if any(c.id == cliente.id for c in self.clientes):
            raise ReservaInvalidaError(f"Ya existe un cliente con id {cliente.id}.")
        self.clientes.append(cliente)
        print(f"   ✔ {cliente}")
        return cliente

    @controlar_errores
    def registrar_servicio(self, clase, *datos):
        servicio = clase(*datos)
        self.servicios.append(servicio)
        print(f"   ✔ {servicio}")
        return servicio

    @controlar_errores
    def crear_reserva(self, id_reserva, cliente, servicio, horas, **parametros):
        reserva = Reserva(id_reserva, cliente, servicio, horas, **parametros)
        self.reservas.append(reserva)
        print(f"   ✔ {reserva}")
        return reserva

    @controlar_errores
    def confirmar(self, reserva):
        reserva.confirmar()
        print(f"   ✔ {reserva}")

    @controlar_errores
    def cancelar(self, reserva):
        reserva.cancelar()
        print(f"   ✔ {reserva}")

    @controlar_errores
    def procesar(self, reserva):
        reserva.procesar()
        print(f"   ✔ {reserva}")
