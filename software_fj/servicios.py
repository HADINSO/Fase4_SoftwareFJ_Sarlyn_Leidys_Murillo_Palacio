"""Módulo de servicios del sistema Software FJ."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .entidades import Entidad
from .excepciones import DatoInvalidoError, ServicioNoDisponibleError


class Servicio(Entidad, ABC):
    """Clase abstracta que representa un servicio ofrecido por Software FJ."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        disponible: bool = True,
        impuesto: float = 0.19,
    ) -> None:
        super().__init__(identificador)
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)
        self._impuesto = float(impuesto)
        self.validar()

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    @property
    def impuesto(self) -> float:
        return self._impuesto

    def validar(self) -> bool:
        if not self.identificador:
            raise DatoInvalidoError("El identificador del servicio es obligatorio.")
        if not self._nombre or len(self._nombre) < 3:
            raise DatoInvalidoError("El nombre del servicio debe tener al menos 3 caracteres.")
        if self._tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base del servicio debe ser mayor que cero.")
        if not (0 <= self._impuesto <= 1):
            raise DatoInvalidoError("El impuesto debe estar entre 0 y 1.")
        return True

    def verificar_disponibilidad(self) -> bool:
        """Verifica si el servicio está disponible para reservas."""
        return self._disponible

    @abstractmethod
    def costo_base(self, horas: float, unidades: int = 1) -> float:
        """Calcula el costo base específico del servicio (polimorfismo)."""

    def calcular_costo(
        self,
        horas: float = 1.0,
        unidades: int = 1,
        descuento: float = 0.0,
        aplicar_impuesto: bool = True,
    ) -> float:
        """Calcula el costo total con descuentos e impuestos.

        Método con parámetros opcionales para demostrar sobrecarga adaptada en Python.
        """
        if not self.verificar_disponibilidad():
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")
        if horas <= 0:
            raise DatoInvalidoError("Las horas deben ser mayores que cero.")
        if unidades <= 0:
            raise DatoInvalidoError("Las unidades deben ser mayores que cero.")
        if not (0 <= descuento <= 0.5):
            raise DatoInvalidoError("El descuento debe estar entre 0 y 0.5 (0% a 50%).")

        subtotal = self.costo_base(horas, unidades)
        subtotal_desc = subtotal * (1 - descuento)
        if aplicar_impuesto:
            total = subtotal_desc * (1 + self._impuesto)
        else:
            total = subtotal_desc
        return round(total, 2)

    def descripcion(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Servicio[{self.identificador}] {self.nombre} - Tarifa: {self._tarifa_base:.2f} - {estado}"


class ReservaSala(Servicio):
    """Servicio para reserva de salas."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        capacidad: int,
        disponible: bool = True,
        impuesto: float = 0.19,
    ) -> None:
        self._capacidad = int(capacidad)
        super().__init__(identificador, nombre, tarifa_base, disponible, impuesto)

    @property
    def capacidad(self) -> int:
        return self._capacidad

    def validar(self) -> bool:
        super().validar()
        if self._capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor que cero.")
        return True

    def costo_base(self, horas: float, unidades: int = 1) -> float:
        """Costo base para sala: tarifa por hora ajustada por número de salas (unidades)."""
        recargo_capacidad = 1.0 + (max(self._capacidad - 10, 0) * 0.01)
        return self.tarifa_base * horas * unidades * recargo_capacidad

    def descripcion(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"ReservaSala[{self.identificador}] {self.nombre} - Capacidad: {self.capacidad} - "
            f"Tarifa/h: {self.tarifa_base:.2f} - {estado}"
        )


class AlquilerEquipo(Servicio):
    """Servicio para alquiler de equipos."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        tipo_equipo: str,
        disponible: bool = True,
        impuesto: float = 0.19,
    ) -> None:
        self._tipo_equipo = tipo_equipo.strip()
        super().__init__(identificador, nombre, tarifa_base, disponible, impuesto)

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    def validar(self) -> bool:
        super().validar()
        if not self._tipo_equipo:
            raise DatoInvalidoError("El tipo de equipo es obligatorio.")
        return True

    def costo_base(self, horas: float, unidades: int = 1) -> float:
        """Costo base para alquiler: tarifa por hora por cada equipo (unidad)."""
        return self.tarifa_base * horas * unidades

    def descripcion(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"AlquilerEquipo[{self.identificador}] {self.nombre} ({self.tipo_equipo}) - "
            f"Tarifa/h: {self.tarifa_base:.2f} - {estado}"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        nivel: str = "general",
        disponible: bool = True,
        impuesto: float = 0.19,
    ) -> None:
        self._nivel = nivel.strip().lower()
        super().__init__(identificador, nombre, tarifa_base, disponible, impuesto)

    @property
    def nivel(self) -> str:
        return self._nivel

    def validar(self) -> bool:
        super().validar()
        niveles_validos = {"basico", "general", "avanzado"}
        if self._nivel not in niveles_validos:
            raise DatoInvalidoError(
                f"Nivel de asesoría inválido. Use uno de: {', '.join(sorted(niveles_validos))}."
            )
        return True

    def costo_base(self, horas: float, unidades: int = 1) -> float:
        """Costo base para asesoría: tarifa por hora ajustada por nivel y unidades (sesiones)."""
        factores = {"basico": 1.0, "general": 1.15, "avanzado": 1.35}
        factor = factores.get(self._nivel, 1.0)
        return self.tarifa_base * horas * unidades * factor

    def descripcion(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"AsesoriaEspecializada[{self.identificador}] {self.nombre} - Nivel: {self.nivel} - "
            f"Tarifa/h: {self.tarifa_base:.2f} - {estado}"
        )
