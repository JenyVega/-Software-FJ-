"""Configuración del archivo de logs (eventos y errores)."""
import logging
import os

RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "sistema.log")


def obtener_logger() -> logging.Logger:
    logger = logging.getLogger("softwarefj")
    if not logger.handlers:  # evita duplicar handlers
        os.makedirs(RUTA_LOGS, exist_ok=True)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(ARCHIVO_LOG, mode="w", encoding="utf-8")
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(handler)
    return logger
