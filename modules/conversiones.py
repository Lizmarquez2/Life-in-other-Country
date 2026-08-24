import requests

def obtener_tasas_api():
    """Consulta una API gratuita para obtener tasas de cambio actualizadas frente al CAD y USD."""
    try:
        # Consultamos usando CAD como base para obtener la relación con PEN y USD
        url = "https://api.frankfurter.app/latest?from=CAD&to=PEN,USD"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})
            cad_a_sol_val = rates.get("PEN", 3.70)
            cad_a_usd_val = rates.get("USD", 0.74)
            
            # Calculamos las inversas necesarias para mantener la compatibilidad con tus funciones
            return {
                "cad_a_sol": cad_a_sol_val,
                "sol_a_cad": 1.0 / cad_a_sol_val if cad_a_sol_val > 0 else 0.27,
                "sol_a_usd": (1.0 / cad_a_sol_val) * cad_a_usd_val if cad_a_sol_val > 0 else 0.20,
                "usd_a_cad": 1.0 / cad_a_usd_val if cad_a_usd_val > 0 else 1.35
            }
    except Exception:
        pass
    
    # Valores de respaldo (fallback) si falla la conexión a internet o la API
    return {
        "sol_a_cad": 0.27,
        "cad_a_sol": 3.70,
        "sol_a_usd": 0.20,
        "usd_a_cad": 1.35
    }

# modules/conversiones.py - Conversiones de moneda
# modules/conversiones.py - Conversiones de moneda (Optimizado)

def sol_a_cad(cantidad_soles, tasa=None):
    """Convierte soles a CAD$ usando tasas de API o fijas."""
    if not tasa:
        tasa = obtener_tasas_api()
    return cantidad_soles * tasa.get("sol_a_cad", 0.27)

def cad_a_sol(cantidad_cad, tasa=None):
    """Convierte CAD$ a soles usando tasas de API o fijas."""
    if not tasa:
        tasa = obtener_tasas_api()
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
    
    if moneda == "PEN":
        monto_soles = monto
        monto_cad = sol_a_cad(monto, tasas)
        monto_usd = sol_a_usd(monto, tasas)
    elif moneda == "USD":
        # Convertir USD a Soles dividiendo entre la tasa sol_a_usd (o multiplicando por su equivalente)
        tasa_sol_usd = tasas.get("sol_a_usd", 0.20)
        monto_soles = monto / tasa_sol_usd if tasa_sol_usd > 0 else monto * 5
        monto_cad = usd_a_cad(monto, tasas)
        monto_usd = monto
    elif moneda == "CAD":
        tasa_cad_sol = tasas.get("cad_a_sol", 3.70)
        monto_soles = monto * tasa_cad_sol
        monto_cad = monto
        monto_usd = monto_soles * tasas.get("sol_a_usd", 0.20)
    else:
        monto_soles = monto
        monto_cad = 0
        monto_usd = 0
    
    return {
        "monto_original_soles": monto_soles,
        "monto_cad": monto_cad,
        "monto_usd": monto_usd
    }

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
            tasa_sol_usd = tasas.get("sol_a_usd", 0.20)
            total += (monto / tasa_sol_usd) if tasa_sol_usd > 0 else (monto * 5)
            
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
