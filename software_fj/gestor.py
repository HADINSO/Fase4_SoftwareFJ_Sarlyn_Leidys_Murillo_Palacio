"""Gestor central del sistema Software FJ."""

from __future__ import annotations

from typing import Dict, List, Optional

from .clientes import Cliente
from .excepciones import (
    ClienteNoEncontradoError,
    DatoInvalidoError,
    ParametroFaltanteError,
    ReservaNoPermitidaError,
    ServicioNoDisponibleError,
)
from .logger_config import configurar_logger
from .reservas import Reserva
from .servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas en memoria."""

    def __init__(self, ruta_log: Optional[str] = None) -> None:
        self.logger = configurar_logger(ruta_log=ruta_log)
        self._clientes: Dict[str, Cliente] = {}
        self._servicios: Dict[str, Servicio] = {}
        self._reservas: Dict[str, Reserva] = {}
        self.logger.info("Gestor de Software FJ inicializado.")

    # -------------------- Clientes --------------------
    def registrar_cliente(self, identificador: str, nombre: str, correo: str, telefono: str) -> Cliente:
        """Registra un cliente validando duplicados y datos."""
        try:
            if not all([identificador, nombre, correo, telefono]):
                raise ParametroFaltanteError("Todos los datos del cliente son obligatorios.")
            if identificador in self._clientes:
                raise DatoInvalidoError(f"Ya existe un cliente con identificador '{identificador}'.")
            correo_norm = correo.strip().lower()
            for c in self._clientes.values():
                if c.correo == correo_norm:
                    raise DatoInvalidoError(
                        f"Ya existe un cliente registrado con el correo '{correo_norm}'."
                    )
        except (DatoInvalidoError, ParametroFaltanteError):
            raise
        except Exception as exc:
            raise DatoInvalidoError("Error al validar datos del cliente.") from exc

        try:
            cliente = Cliente(identificador, nombre, correo, telefono)
        except DatoInvalidoError as exc:
            # Encadenamiento: error de dominio originado por validación específica
            raise DatoInvalidoError(f"No fue posible registrar el cliente: {exc}") from exc
        else:
            self._clientes[identificador] = cliente
            self.logger.info("Cliente registrado: %s", cliente.descripcion())
            return cliente
        finally:
            self.logger.info("Operación de registro de cliente finalizada (id=%s).", identificador)

    def consultar_cliente(self, identificador: str) -> Cliente:
        if not identificador:
            raise ParametroFaltanteError("Debe proporcionar el identificador del cliente.")
        cliente = self._clientes.get(identificador)
        if cliente is None:
            raise ClienteNoEncontradoError(f"No se encontró el cliente con id '{identificador}'.")
        return cliente

    def listar_clientes(self) -> List[Cliente]:
        return list(self._clientes.values())

    # -------------------- Servicios --------------------
    def _validar_id_servicio(self, identificador: str) -> None:
        if identificador in self._servicios:
            raise DatoInvalidoError(f"Ya existe un servicio con identificador '{identificador}'.")

    def crear_servicio_reserva_sala(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        capacidad: int,
        disponible: bool = True,
    ) -> ReservaSala:
        try:
            if not all([identificador, nombre]) or capacidad is None:
                raise ParametroFaltanteError("Faltan parámetros obligatorios para crear la sala.")
            self._validar_id_servicio(identificador)
            servicio = ReservaSala(identificador, nombre, tarifa_base, capacidad, disponible)
        except (DatoInvalidoError, ParametroFaltanteError):
            raise
        except Exception as exc:
            raise DatoInvalidoError("Error inesperado al crear servicio de sala.") from exc
        else:
            self._servicios[identificador] = servicio
            self.logger.info("Servicio creado: %s", servicio.descripcion())
            return servicio
        finally:
            self.logger.info("Operación de creación de servicio sala finalizada (id=%s).", identificador)

    def crear_servicio_alquiler_equipo(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        tipo_equipo: str,
        disponible: bool = True,
    ) -> AlquilerEquipo:
        try:
            if not all([identificador, nombre, tipo_equipo]):
                raise ParametroFaltanteError("Faltan parámetros obligatorios para crear el equipo.")
            self._validar_id_servicio(identificador)
            servicio = AlquilerEquipo(identificador, nombre, tarifa_base, tipo_equipo, disponible)
        except (DatoInvalidoError, ParametroFaltanteError):
            raise
        except Exception as exc:
            raise DatoInvalidoError("Error inesperado al crear servicio de alquiler.") from exc
        else:
            self._servicios[identificador] = servicio
            self.logger.info("Servicio creado: %s", servicio.descripcion())
            return servicio
        finally:
            self.logger.info("Operación de creación de alquiler finalizada (id=%s).", identificador)

    def crear_servicio_asesoria(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        nivel: str = "general",
        disponible: bool = True,
    ) -> AsesoriaEspecializada:
        try:
            if not all([identificador, nombre, nivel]):
                raise ParametroFaltanteError("Faltan parámetros obligatorios para crear la asesoría.")
            self._validar_id_servicio(identificador)
            servicio = AsesoriaEspecializada(identificador, nombre, tarifa_base, nivel, disponible)
        except (DatoInvalidoError, ParametroFaltanteError):
            raise
        except Exception as exc:
            raise DatoInvalidoError("Error inesperado al crear servicio de asesoría.") from exc
        else:
            self._servicios[identificador] = servicio
            self.logger.info("Servicio creado: %s", servicio.descripcion())
            return servicio
        finally:
            self.logger.info("Operación de creación de asesoría finalizada (id=%s).", identificador)

    def consultar_servicio(self, identificador: str) -> Servicio:
        if not identificador:
            raise ParametroFaltanteError("Debe proporcionar el identificador del servicio.")
        servicio = self._servicios.get(identificador)
        if servicio is None:
            raise ServicioNoDisponibleError(f"No se encontró el servicio con id '{identificador}'.")
        return servicio

    def listar_servicios(self) -> List[Servicio]:
        return list(self._servicios.values())

    # -------------------- Reservas --------------------
    def crear_reserva(
        self,
        identificador: str,
        id_cliente: str,
        id_servicio: str,
        horas: float,
        unidades: int = 1,
    ) -> Reserva:
        """Crea una reserva asociando cliente y servicio."""
        try:
            if not all([identificador, id_cliente, id_servicio]):
                raise ParametroFaltanteError("Faltan parámetros obligatorios para crear la reserva.")
            if identificador in self._reservas:
                raise DatoInvalidoError(f"Ya existe una reserva con identificador '{identificador}'.")
            try:
                cliente = self.consultar_cliente(id_cliente)
            except ClienteNoEncontradoError as exc:
                raise ReservaNoPermitidaError("No se puede crear la reserva: cliente inexistente.") from exc
            try:
                servicio = self.consultar_servicio(id_servicio)
            except ServicioNoDisponibleError as exc:
                raise ServicioNoDisponibleError(
                    "No se puede crear la reserva: el servicio solicitado no existe o no está disponible."
                ) from exc
            if not servicio.verificar_disponibilidad():
                raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")
            reserva = Reserva(identificador, cliente, servicio, horas, unidades)
        except (DatoInvalidoError, ParametroFaltanteError, ReservaNoPermitidaError, ServicioNoDisponibleError):
            raise
        except Exception as exc:
            raise ReservaNoPermitidaError("Error inesperado al crear la reserva.") from exc
        else:
            self._reservas[identificador] = reserva
            self.logger.info("Reserva creada: %s", reserva.descripcion())
            return reserva
        finally:
            self.logger.info("Operación de creación de reserva finalizada (id=%s).", identificador)

    def consultar_reserva(self, identificador: str) -> Reserva:
        if not identificador:
            raise ParametroFaltanteError("Debe proporcionar el identificador de la reserva.")
        reserva = self._reservas.get(identificador)
        if reserva is None:
            raise ReservaNoPermitidaError(f"No se encontró la reserva con id '{identificador}'.")
        return reserva

    def confirmar_reserva(self, identificador: str) -> Reserva:
        try:
            reserva = self.consultar_reserva(identificador)
            reserva.confirmar()
        except Exception:
            raise
        else:
            self.logger.info("Reserva confirmada: %s", reserva.descripcion())
            return reserva
        finally:
            self.logger.info("Operación de confirmación de reserva finalizada (id=%s).", identificador)

    def cancelar_reserva(self, identificador: str, motivo: str = "") -> Reserva:
        try:
            reserva = self.consultar_reserva(identificador)
            reserva.cancelar(motivo)
        except Exception:
            raise
        else:
            self.logger.info("Reserva cancelada: %s. Motivo: %s", reserva.descripcion(), motivo or "N/A")
            return reserva
        finally:
            self.logger.info("Operación de cancelación de reserva finalizada (id=%s).", identificador)

    def procesar_reserva(self, identificador: str, descuento: float = 0.0, aplicar_impuesto: bool = True) -> float:
        try:
            reserva = self.consultar_reserva(identificador)
            costo = reserva.procesar(descuento=descuento, aplicar_impuesto=aplicar_impuesto)
        except Exception:
            raise
        else:
            self.logger.info("Reserva procesada: %s. Costo total: %.2f", reserva.descripcion(), costo)
            return costo
        finally:
            self.logger.info("Operación de procesamiento de reserva finalizada (id=%s).", identificador)

    def listar_reservas(self) -> List[Reserva]:
        return list(self._reservas.values())
