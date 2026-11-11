"""Definición de entidades base del sistema Software FJ."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta general para representar entidades del sistema."""

    def __init__(self, identificador: str) -> None:
        self._identificador = str(identificador).strip()

    @property
    def identificador(self) -> str:
        """Identificador único de la entidad."""
        return self._identificador

    @abstractmethod
    def descripcion(self) -> str:
        """Retorna una descripción legible de la entidad."""

    @abstractmethod
    def validar(self) -> bool:
        """Valida el estado interno de la entidad."""

    def __str__(self) -> str:
        return self.descripcion()
