"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidades import Cliente, EntidadBase
from excepciones import (ErrorSistemaFJ, OperacionNoPermitidaError, ReservaInvalidaError)
from logger_config import obtener_logger
from servicios import IVA, Servicio

log = obtener_logger()


class Reserva(EntidadBase):
    PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"

    def __init__(self, identificador, cliente, servicio, horas, **parametros):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido.")
        servicio.verificar_disponible()
        servicio.validar_parametros(horas, **parametros)   # falla temprano
        self._cliente, self._servicio = cliente, servicio
        self._horas, self._parametros = horas, parametros
        self._estado = self.PENDIENTE
        self._costo_total = None

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def confirmar(self):
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}.")
        self._estado = self.CONFIRMADA
        log.info("Reserva %s confirmada.", self.id)

    def cancelar(self):
        if self._estado in (self.CANCELADA, self.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado}.")
        self._estado = self.CANCELADA
        log.info("Reserva %s cancelada.", self.id)

    def procesar(self):
        """Calcula el costo final. Usa try/except/else/finally y encadenamiento."""
        try:
            if self._estado != self.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesan reservas CONFIRMADAS (actual: {self._estado}).")
            self._servicio.verificar_disponible()
            costo = self._servicio.calcular_costo(self._horas, impuesto=IVA, **self._parametros)
        except ErrorSistemaFJ:
            raise                                   # error conocido: se propaga tal cual
        except Exception as e:                      # error inesperado: se encadena
            raise ReservaInvalidaError(f"Fallo inesperado al procesar {self.id}.") from e
        else:
            self._costo_total, self._estado = costo, self.PROCESADA
            log.info("Reserva %s procesada. Total: $%s", self.id, f"{costo:,.2f}")
            return costo
        finally:
            log.debug("Fin del intento de procesamiento de la reserva %s.", self.id)

    def describir(self):
        total = f"${self._costo_total:,.2f}" if self._costo_total else "—"
        return (f"Reserva[{self.id}] {self._cliente.nombre} -> {self._servicio.nombre} "
                f"| {self._horas}h | {self._estado} | Total: {total}")
