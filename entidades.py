"""Clase abstracta de entidades generales y la clase Cliente."""
import re
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError, ParametroFaltanteError


class EntidadBase(ABC):
    """Abstracción de cualquier entidad del sistema (cliente, servicio, reserva)."""

    def __init__(self, identificador):
        if identificador is None or str(identificador).strip() == "":
            raise ParametroFaltanteError("El identificador es obligatorio.")
        self._id = str(identificador).strip()  # encapsulado

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible de la entidad."""

    def __str__(self):
        return self.describir()


class Cliente(EntidadBase):
    """Cliente con datos personales encapsulados y validaciones estrictas."""

    _PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

    def __init__(self, identificador, nombre, email, telefono):
        super().__init__(identificador)
        self.nombre = nombre      # pasan por los setters (validan)
        self.email = email
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El nombre es obligatorio.")
        valor = str(valor).strip()
        if len(valor) < 3 or not all(c.isalpha() or c.isspace() for c in valor):
            raise ClienteInvalidoError(f"Nombre inválido: '{valor}'.")
        self._nombre = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El correo es obligatorio.")
        if not self._PATRON_EMAIL.match(str(valor).strip()):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'.")
        self._email = str(valor).strip().lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None:
            raise ParametroFaltanteError("El teléfono es obligatorio.")
        digitos = str(valor).strip()
        if not digitos.isdigit() or not 7 <= len(digitos) <= 10:
            raise ClienteInvalidoError(f"Teléfono inválido: '{valor}'.")
        self._telefono = digitos

    def describir(self):
        return f"Cliente[{self.id}] {self.nombre} | {self.email} | Tel: {self.telefono}"
