"""Clase abstracta Servicio y tres servicios especializados."""
from abc import ABC, abstractmethod

from entidades import EntidadBase
from excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                         ServicioInvalidoError, ServicioNoDisponibleError)

IVA = 0.19


class Servicio(EntidadBase, ABC):
    """Servicio genérico de Software FJ (abstracto)."""

    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        super().__init__(identificador)
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if isinstance(tarifa_hora, str):      # encadenamiento de excepciones
            try:
                tarifa_hora = float(tarifa_hora)
            except ValueError as e:
                raise ServicioInvalidoError(f"La tarifa '{tarifa_hora}' no es numérica.") from e
        if isinstance(tarifa_hora, bool) or not isinstance(tarifa_hora, (int, float)) \
                or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}.")
        self._nombre = str(nombre).strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    # --- propiedades encapsuladas ---
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    def verificar_disponible(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    # --- métodos abstractos (polimorfismo) ---
    @abstractmethod
    def validar_parametros(self, horas, **parametros):
        """Valida duración y parámetros propios del servicio."""

    @abstractmethod
    def _costo_base(self, horas, **parametros) -> float:
        """Costo sin impuestos ni descuentos."""

    @staticmethod
    def _validar_horas(horas):
        if horas is None:
            raise ParametroFaltanteError("La duración (horas) es obligatoria.")
        if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:
            raise ServicioInvalidoError(f"Duración inválida: {horas!r}.")

    # --- métodos sobrecargados (parámetros opcionales) ---
    def calcular_costo(self, horas, descuento=0.0, impuesto=0.0, **parametros):
        """Variantes: calcular_costo(h) | (h, descuento=0.1) | (h, impuesto=0.19) | ambos."""
        self.validar_parametros(horas, **parametros)
        if not 0 <= descuento < 1 or not 0 <= impuesto < 1:
            raise CalculoInconsistenteError("Descuento o impuesto fuera de rango.")
        total = self._costo_base(horas, **parametros) * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El costo calculado no es positivo.")
        return round(total, 2)

    def costo_con_impuesto(self, horas, impuesto=IVA, **parametros):
        return self.calcular_costo(horas, impuesto=impuesto, **parametros)

    def costo_con_descuento(self, horas, descuento, impuesto=IVA, **parametros):
        return self.calcular_costo(horas, descuento=descuento, impuesto=impuesto, **parametros)


class ReservaSala(Servicio):
    """Reserva de salas con capacidad máxima."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}.")
        self._capacidad = capacidad

    def validar_parametros(self, horas, **p):
        self._validar_horas(horas)
        if horas > 12:
            raise ServicioInvalidoError("Una sala no puede reservarse más de 12 horas.")
        asistentes = p.get("asistentes")
        if asistentes is None:
            raise ParametroFaltanteError("Falta el parámetro 'asistentes'.")
        if not isinstance(asistentes, int) or not 0 < asistentes <= self._capacidad:
            raise ServicioInvalidoError(
                f"Asistentes inválidos ({asistentes!r}); capacidad máx. {self._capacidad}.")

    def _costo_base(self, horas, **p):
        return self.tarifa_hora * horas

    def describir(self):
        return f"Sala[{self.id}] {self.nombre} | cap. {self._capacidad} | ${self.tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos por unidades."""

    def __init__(self, identificador, nombre, tarifa_hora, stock, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(stock, int) or stock <= 0:
            raise ServicioInvalidoError(f"Stock inválido: {stock!r}.")
        self._stock = stock

    def validar_parametros(self, horas, **p):
        self._validar_horas(horas)
        cantidad = p.get("cantidad")
        if cantidad is None:
            raise ParametroFaltanteError("Falta el parámetro 'cantidad'.")
        if not isinstance(cantidad, int) or not 0 < cantidad <= self._stock:
            raise ServicioInvalidoError(f"Cantidad inválida ({cantidad!r}); stock {self._stock}.")

    def _costo_base(self, horas, **p):
        return self.tarifa_hora * horas * p["cantidad"]

    def describir(self):
        return f"Equipo[{self.id}] {self.nombre} | stock {self._stock} | ${self.tarifa_hora:,.0f}/h"


class AsesoriaEspecializada(Servicio):
    """Asesoría con recargo según el nivel del experto."""

    RECARGOS = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, identificador, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not especialidad or not str(especialidad).strip():
            raise ParametroFaltanteError("La especialidad es obligatoria.")
        self._especialidad = str(especialidad).strip()

    def validar_parametros(self, horas, **p):
        self._validar_horas(horas)
        nivel = p.get("nivel", "junior")
        if nivel not in self.RECARGOS:
            raise ServicioInvalidoError(f"Nivel inválido: {nivel!r}. Use {list(self.RECARGOS)}.")

    def _costo_base(self, horas, **p):
        return self.tarifa_hora * horas * self.RECARGOS[p.get("nivel", "junior")]

    def describir(self):
        return f"Asesoría[{self.id}] {self.nombre} ({self._especialidad}) | ${self.tarifa_hora:,.0f}/h"
