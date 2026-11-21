# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto en Python (3.8+), sin bases de datos. Curso Programación 213023 – UNAD.

## Ejecutar
    python main.py

## Estructura (un módulo por integrante, sugerido)
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas |
| `logger_config.py` | Archivo de logs (`logs/sistema.log`) |
| `entidades.py` | `EntidadBase` (abstracta) y `Cliente` |
| `servicios.py` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reserva.py` | `Reserva` (confirmar, cancelar, procesar) |
| `gestor.py` | `GestorFJ`: listas internas y control de errores |
| `main.py` | Simulación de 12 operaciones válidas e inválidas |

## Conceptos aplicados
Abstracción, herencia, polimorfismo, encapsulación (propiedades), sobrecarga (parámetros opcionales),
try/except, try/except/else, try/except/finally y encadenamiento (`raise ... from e`).
