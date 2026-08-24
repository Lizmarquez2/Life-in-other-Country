# modules/calculadora.py - Cálculos automáticos (Optimizado)

from datetime import datetime
from modules.conversiones import sol_a_cad, cad_a_sol, calcular_total_soles, calcular_total_cad

def calcular_totales_movimientos(datos):
    """Calcula totales de ahorro y gasto."""
    movimientos = datos.get("movimientos", {}).get("movimientos", [])
    tasas = datos.get("config", {}).get("tasas_cambio", {})
    
    ahorros = [m for m in movimientos if m.get("tipo") == "AHORRO"]
    gastos = [m for m in movimientos if m.get("tipo") == "GASTO"]
    
    total_ahorrado_soles = calcular_total_soles(ahorros, tasas)
    total_gastado_soles = calcular_total_soles(gastos, tasas)
    saldo_soles = total_ahorrado_soles - total_gastado_soles
    
    total_ahorrado_cad = sol_a_cad(total_ahorrado_soles, tasas)
    total_gastado_cad = sol_a_cad(total_gastado_soles, tasas)
    # Consistencia: Saldo en CAD como la diferencia entre ahorros y gastos en CAD
    saldo_cad = total_ahorrado_cad - total_gastado_cad
    
    return {
        "total_ahorrado_soles": total_ahorrado_soles,
        "total_gastado_soles": total_gastado_soles,
        "saldo_soles": saldo_soles,
        "total_ahorrado_cad": total_ahorrado_cad,
        "total_gastado_cad": total_gastado_cad,
        "saldo_cad": saldo_cad
    }

def calcular_progreso_bolsa(datos):
    """Calcula progreso hacia la meta de bolsa migratoria."""
    totales = calcular_totales_movimientos(datos)
    metas = datos.get("config", {}).get("metas_financieras", {})
    
    meta_soles = metas.get("bolsa_migracion_meta_soles", 60000)
    saldo = totales.get("saldo_soles", 0)
    
    progreso_pct = (saldo / meta_soles * 100) if meta_soles > 0 else 0
    falta = max(0, meta_soles - saldo)
    
    return {
        "meta_soles": meta_soles,
        "ahorrado_soles": saldo,
        "falta_soles": falta,
        "progreso_pct": min(100.0, max(0.0, progreso_pct)),
        "alcanza_meta": saldo >= meta_soles
    }

def calcular_por_persona(datos, persona):
    """Calcula totales para una persona específica."""
    movimientos = datos.get("movimientos", {}).get("movimientos", [])
    tasas = datos.get("config", {}).get("tasas_cambio", {})
    
    movimientos_persona = [m for m in movimientos if m.get("persona") == persona]
    
    ahorros_persona = [m for m in movimientos_persona if m.get("tipo") == "AHORRO"]
    gastos_persona = [m for m in movimientos_persona if m.get("tipo") == "GASTO"]
    
    total_ahorrado = calcular_total_soles(ahorros_persona, tasas)
    total_gastado = calcular_total_soles(gastos_persona, tasas)
    saldo = total_ahorrado - total_gastado
    
    return {
        "persona": persona,
        "total_ahorrado_soles": total_ahorrado,
        "total_gastado_soles": total_gastado,
        "saldo_soles": saldo,
        "saldo_cad": sol_a_cad(saldo, tasas),
        "movimientos_count": len(movimientos_persona)
    }

def calcular_dias_faltantes(datos):
    """Calcula días faltantes para la fecha objetivo de viaje."""
    fechas = datos.get("config", {}).get("fechas_clave", {})
    fecha_viaje_str = fechas.get("fecha_objetivo_viaje", "2027-06-15")
    
    try:
        fecha_viaje = datetime.strptime(fecha_viaje_str, "%Y-%m-%d")
        hoy = datetime.now()
        dias_faltantes = (fecha_viaje - hoy).days
        return max(0, dias_faltantes)
    except (ValueError, TypeError):
        return 0

def calcular_progreso_tiempo(datos):
    """Calcula progreso de tiempo en el proyecto."""
    fechas = datos.get("config", {}).get("fechas_clave", {})
    
    inicio_str = fechas.get("fecha_inicio_proyecto", "2026-08-01")
    fin_str = fechas.get("fecha_objetivo_viaje", "2027-06-15")
    
    try:
        inicio = datetime.strptime(inicio_str, "%Y-%m-%d")
        fin = datetime.strptime(fin_str, "%Y-%m-%d")
        hoy = datetime.now()
        
        dias_totales = (fin - inicio).days
        dias_transcurridos = (hoy - inicio).days
        
        progreso_pct = (dias_transcurridos / dias_totales * 100) if dias_totales > 0 else 0
        
        return {
            "dias_totales": dias_totales,
            "dias_transcurridos": dias_transcurridos,
            "dias_faltantes": max(0, (fin - hoy).days),
            "progreso_pct": min(100.0, max(0.0, progreso_pct))
        }
    except (ValueError, TypeError):
        return {"dias_totales": 0, "dias_transcurridos": 0, "dias_faltantes": 0, "progreso_pct": 0}

def obtener_tramites_por_estado(datos, estado):
    """Retorna trámites filtrados por estado."""
    tramites = datos.get("tramites", {}).get("tramites", [])
    return [t for t in tramites if t.get("estado_actual", {}).get("estado", "") == estado]

def calcular_presupuesto_por_categoria(datos):
    """Calcula presupuesto total por categoría."""
    presupuesto = datos.get("presupuesto", {}).get("presupuesto", {})
    categorias = presupuesto.get("desglose_por_categoria", {})
    
    resultado = {}
    for categoria, datos_cat in categorias.items():
        resultado[categoria] = {
            "moneda": datos_cat.get("moneda", "PEN"),
            "costo_total": datos_cat.get("costo_total", 0),
            "porcentaje": datos_cat.get("porcentaje_presupuesto", 0)
        }
    
    return resultado

def obtener_kpis_principales(datos):
    """Calcula KPIs principales para el dashboard."""
    totales = calcular_totales_movimientos(datos)
    progreso_bolsa = calcular_progreso_bolsa(datos)
    progreso_tiempo = calcular_progreso_tiempo(datos)
    dias_faltantes = calcular_dias_faltantes(datos)
    
    return {
        "ahorrado_soles": totales.get("total_ahorrado_soles", 0),
        "gastado_soles": totales.get("total_gastado_soles", 0),
        "saldo_disponible_soles": totales.get("saldo_soles", 0),
        "saldo_disponible_cad": totales.get("saldo_cad", 0),
        "progreso_bolsa_pct": progreso_bolsa.get("progreso_pct", 0),
        "bolsa_alcanzada": progreso_bolsa.get("alcanza_meta", False),
        "progreso_tiempo_pct": progreso_tiempo.get("progreso_pct", 0),
        "dias_faltantes": dias_faltantes
    }