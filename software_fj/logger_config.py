"""Configuración centralizada del sistema de logs para Software FJ."""

from __future__ import annotations

import logging
from pathlib import Path


def configurar_logger(nombre: str = "software_fj", ruta_log: str | Path | None = None) -> logging.Logger:
    """Configura y retorna un logger con salida a archivo y consola.

    Args:
        nombre: Nombre del logger.
        ruta_log: Ruta del archivo de log. Si es None, se usa logs/software_fj.log
            relativo a la carpeta raíz del proyecto.

    Returns:
        Instancia de logging.Logger configurada.
    """
    logger = logging.getLogger(nombre)
    if logger.handlers:
        # Evita duplicar handlers si se configura varias veces.
        return logger

    logger.setLevel(logging.INFO)

    if ruta_log is None:
        base_dir = Path(__file__).resolve().parents[1]
        ruta_log = base_dir / "logs" / "software_fj.log"
    ruta_log = Path(ruta_log)
    ruta_log.parent.mkdir(parents=True, exist_ok=True)

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(ruta_log, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formato)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formato)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger
