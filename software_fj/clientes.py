"""Módulo de gestión y representación de clientes."""

from __future__ import annotations

import re

from .entidades import Entidad
from .excepciones import DatoInvalidoError


class Cliente(Entidad):
    """Representa un cliente con datos personales encapsulados."""

    _EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    _TELEFONO_RE = re.compile(r"^\d{7,15}$")

    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str) -> None:
        super().__init__(identificador)
        self._nombre = nombre.strip()
        self._correo = correo.strip().lower()
        self._telefono = telefono.strip()
        self.validar()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = valor.strip()
        self._validar_nombre()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        self._correo = valor.strip().lower()
        self._validar_correo()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        self._telefono = valor.strip()
        self._validar_telefono()

    def _validar_nombre(self) -> None:
        if not self._nombre or len(self._nombre) < 3:
            raise DatoInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", self._nombre):
            raise DatoInvalidoError("El nombre del cliente solo puede contener letras y espacios.")

    def _validar_correo(self) -> None:
        if not self._EMAIL_RE.fullmatch(self._correo):
            raise DatoInvalidoError(f"El correo electrónico '{self._correo}' no es válido.")

    def _validar_telefono(self) -> None:
        if not self._TELEFONO_RE.fullmatch(self._telefono):
            raise DatoInvalidoError(
                "El número telefónico debe contener solo dígitos (entre 7 y 15)."
            )

    def validar(self) -> bool:
        """Valida estrictamente los datos del cliente."""
        if not self.identificador:
            raise DatoInvalidoError("El identificador del cliente es obligatorio.")
        self._validar_nombre()
        self._validar_correo()
        self._validar_telefono()
        return True

    def descripcion(self) -> str:
        """Retorna la descripción del cliente (método sobrescrito)."""
        return (
            f"Cliente[{self.identificador}] {self.nombre} "
            f"<{self.correo}> Tel: {self.telefono}"
        )

    def actualizar_contacto(self, correo: str | None = None, telefono: str | None = None) -> None:
        """Actualiza datos de contacto con parámetros opcionales (sobrecarga adaptada)."""
        if correo is not None:
            self.correo = correo
        if telefono is not None:
            self.telefono = telefono
        if correo is None and telefono is None:
            raise DatoInvalidoError("Debe proporcionar al menos un dato de contacto para actualizar.")
