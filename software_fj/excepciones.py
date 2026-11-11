"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base para errores del sistema Software FJ."""


class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando un dato proporcionado no cumple las validaciones."""


class ClienteNoEncontradoError(SoftwareFJError):
    """Se lanza cuando no se encuentra un cliente solicitado."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando un servicio no existe o no está disponible."""


class ReservaNoPermitidaError(SoftwareFJError):
    """Se lanza cuando una operación sobre una reserva no es válida."""


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio para una operación."""
