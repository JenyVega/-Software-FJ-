"""Excepciones personalizadas del sistema Software FJ."""


class ErrorSistemaFJ(Exception):
    """Excepción base de la que heredan todos los errores del sistema."""


class ParametroFaltanteError(ErrorSistemaFJ):
    """Falta un parámetro obligatorio."""


class ClienteInvalidoError(ErrorSistemaFJ):
    """Los datos del cliente no son válidos."""


class ServicioInvalidoError(ErrorSistemaFJ):
    """Los datos o parámetros del servicio no son válidos."""


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """El servicio solicitado no está disponible."""


class ReservaInvalidaError(ErrorSistemaFJ):
    """La reserva no se pudo crear o procesar."""


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """La operación no está permitida en el estado actual."""


class CalculoInconsistenteError(ErrorSistemaFJ):
    """El cálculo de costos produjo un resultado inconsistente."""
