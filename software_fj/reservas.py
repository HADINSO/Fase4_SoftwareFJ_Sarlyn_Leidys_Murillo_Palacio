"""Módulo de reservas del sistema Software FJ."""

from __future__ import annotations

from datetime import datetime

from .clientes import Cliente
from .excepciones import DatoInvalidoError, ReservaNoPermitidaError, ServicioNoDisponibleError
from .servicios import Servicio


class Reserva:
    """Representa una reserva que asocia un cliente con un servicio."""

    ESTADOS_VALIDOS = {"CREADA", "CONFIRMADA", "CANCELADA", "PROCESADA"}

    def __init__(
        self,
        identificador: str,
        cliente: Cliente,
        servicio: Servicio,
        horas: float,
        unidades: int = 1,
        fecha: datetime | None = None,
    ) -> None:
        self._identificador = str(identificador).strip()
        self._cliente = cliente
        self._servicio = servicio
        self._horas = float(horas)
        self._unidades = int(unidades)
        self._fecha = fecha or datetime.now()
        self._estado = "CREADA"
        self._costo_total: float | None = None
        self.validar()

    @property
    def identificador(self) -> str:
        return self._identificador

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def horas(self) -> float:
        return self._horas

    @property
    def unidades(self) -> int:
        return self._unidades

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float | None:
        return self._costo_total

    def validar(self) -> bool:
        if not self._identificador:
            raise DatoInvalidoError("El identificador de la reserva es obligatorio.")
        if self._cliente is None:
            raise DatoInvalidoError("La reserva debe estar asociada a un cliente.")
        if self._servicio is None:
            raise DatoInvalidoError("La reserva debe estar asociada a un servicio.")
        if self._horas <= 0:
            raise DatoInvalidoError("La duración de la reserva debe ser mayor que cero.")
        if self._unidades <= 0:
            raise DatoInvalidoError("Las unidades de la reserva deben ser mayores que cero.")
        return True

    def _validar_estado(self, estado: str) -> None:
        if estado not in self.ESTADOS_VALIDOS:
            raise ReservaNoPermitidaError(f"Estado de reserva no válido: {estado}")

    def confirmar(self) -> None:
        """Confirma la reserva si está en estado CREADA y el servicio está disponible."""
        if self._estado != "CREADA":
            raise ReservaNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}."
            )
        if not self._servicio.verificar_disponibilidad():
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' no está disponible para confirmar."
            )
        self._estado = "CONFIRMADA"

    def cancelar(self, motivo: str = "") -> None:
        """Cancela la reserva si no ha sido procesada."""
        if self._estado == "PROCESADA":
            raise ReservaNoPermitidaError("No se puede cancelar una reserva ya procesada.")
        if self._estado == "CANCELADA":
            raise ReservaNoPermitidaError("La reserva ya se encuentra cancelada.")
        self._estado = "CANCELADA"
        self._motivo_cancelacion = motivo  # atributo informativo

    def calcular_costo(self, descuento: float = 0.0, aplicar_impuesto: bool = True) -> float:
        """Calcula y almacena el costo total de la reserva."""
        self._costo_total = self._servicio.calcular_costo(
            horas=self._horas,
            unidades=self._unidades,
            descuento=descuento,
            aplicar_impuesto=aplicar_impuesto,
        )
        return self._costo_total

    def procesar(self, descuento: float = 0.0, aplicar_impuesto: bool = True) -> float:
        """Procesa la reserva: requiere estado CONFIRMADA y calcula el costo."""
        if self._estado != "CONFIRMADA":
            raise ReservaNoPermitidaError(
                "Solo se pueden procesar reservas previamente confirmadas."
            )
        costo = self.calcular_costo(descuento=descuento, aplicar_impuesto=aplicar_impuesto)
        self._estado = "PROCESADA"
        return costo

    def descripcion(self) -> str:
        costo = f"{self._costo_total:.2f}" if self._costo_total is not None else "N/A"
        return (
            f"Reserva[{self.identificador}] Cliente: {self.cliente.identificador} "
            f"Servicio: {self.servicio.identificador} Estado: {self.estado} "
            f"Horas: {self.horas} Unidades: {self.unidades} Costo: {costo}"
        )

    def __str__(self) -> str:
        return self.descripcion()
