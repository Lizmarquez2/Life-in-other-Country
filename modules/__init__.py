# modules/__init__.py

from .data_loader import (
    cargar_todos_datos,
    obtener_tasas_cambio,
    obtener_personas,
    obtener_metas
)

from .conversiones import (
    sol_a_cad,
    cad_a_sol,
    formato_moneda_soles,
    formato_moneda_cad
)

from .calculadora import (
    calcular_totales_movimientos,
    calcular_progreso_bolsa,
    calcular_por_persona,
    obtener_kpis_principales
)

__all__ = [
    'cargar_todos_datos',
    'obtener_tasas_cambio',
    'obtener_personas',
    'obtener_metas',
    'sol_a_cad',
    'cad_a_sol',
    'formato_moneda_soles',
    'formato_moneda_cad',
    'calcular_totales_movimientos',
    'calcular_progreso_bolsa',
    'calcular_por_persona',
    'obtener_kpis_principales'
]
