# modules/conversiones.py - Conversiones de moneda

def sol_a_cad(cantidad_soles, tasa):
    """Convierte soles a CAD$."""
    return cantidad_soles * tasa.get("sol_a_cad", 0.27)

def cad_a_sol(cantidad_cad, tasa):
    """Convierte CAD$ a soles."""
    return cantidad_cad * tasa.get("cad_a_sol", 3.70)

def sol_a_usd(cantidad_soles, tasa):
    """Convierte soles a USD."""
    return cantidad_soles * tasa.get("sol_a_usd", 0.20)

def usd_a_cad(cantidad_usd, tasa):
    """Convierte USD a CAD$."""
    return cantidad_usd * tasa.get("usd_a_cad", 1.35)

def formato_moneda_soles(cantidad):
    """Formatea cantidad en formato de soles."""
    return f"S/ {cantidad:,.2f}"

def formato_moneda_cad(cantidad):
    """Formatea cantidad en formato CAD."""
    return f"CAD $ {cantidad:,.2f}"

def convertir_movimiento(movimiento, tasas):
    """
    Convierte un movimiento a múltiples monedas.
    Retorna dict con monedas convertidas.
    """
    monto = movimiento.get("monto_original", 0)
    moneda = movimiento.get("moneda_original", "PEN")
    
    resultado = {
        "monto_original_soles": monto if moneda == "PEN" else sol_a_usd(monto, tasas) if moneda == "USD" else 0,
        "monto_cad": sol_a_cad(monto, tasas) if moneda == "PEN" else usd_a_cad(monto, tasas) if moneda == "USD" else 0,
        "monto_usd": sol_a_usd(monto, tasas) if moneda == "PEN" else monto if moneda == "USD" else 0
    }
    
    return resultado

def calcular_total_soles(movimientos, tasas):
    """Suma todos los montos convirtiéndolos a soles."""
    total = 0
    for mov in movimientos:
        moneda = mov.get("moneda_original", "PEN")
        monto = mov.get("monto_original", 0)
        
        if moneda == "PEN":
            total += monto
        elif moneda == "CAD":
            total += cad_a_sol(monto, tasas)
        elif moneda == "USD":
            total += (monto / tasas.get("sol_a_usd", 0.20))
    
    return total

def calcular_total_cad(movimientos, tasas):
    """Suma todos los montos convirtiéndolos a CAD."""
    total = 0
    for mov in movimientos:
        moneda = mov.get("moneda_original", "PEN")
        monto = mov.get("monto_original", 0)
        
        if moneda == "PEN":
            total += sol_a_cad(monto, tasas)
        elif moneda == "CAD":
            total += monto
        elif moneda == "USD":
            total += usd_a_cad(monto, tasas)
    
    return total
