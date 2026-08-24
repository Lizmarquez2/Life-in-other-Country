# modules/data_loader.py - Cargador de datos desde JSONs

import json
import os
from pathlib import Path

def cargar_json(archivo_path):
    """Carga un archivo JSON y retorna los datos."""
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {archivo_path}")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Error al decodificar JSON: {archivo_path}")
        return {}

def cargar_todos_datos():
    """Carga todos los archivos de datos del proyecto."""
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"
    
    datos = {
        "config": cargar_json(data_dir / "config.json"),
        "tramites": cargar_json(data_dir / "tramites.json"),
        "cronograma": cargar_json(data_dir / "cronograma.json"),
        "movimientos": cargar_json(data_dir / "movimientos.json"),
        "presupuesto": cargar_json(data_dir / "presupuesto.json"),
        "bolsa_migracion": cargar_json(data_dir / "bolsa_migracion.json")
    }
    
    return datos

def obtener_tasas_cambio(datos):
    """Extrae las tasas de cambio del config."""
    return datos.get("config", {}).get("tasas_cambio", {})

def obtener_personas(datos):
    """Retorna lista de personas del proyecto."""
    personas = datos.get("config", {}).get("personas", {})
    return list(personas.keys())

def obtener_metas(datos):
    """Retorna metas financieras."""
    return datos.get("config", {}).get("metas_financieras", {})

def obtener_fechas(datos):
    """Retorna fechas clave del proyecto."""
    return datos.get("config", {}).get("fechas_clave", {})

def obtener_tramites_por_persona(datos, persona):
    """Retorna trámites asignados a una persona."""
    tramites_data = datos.get("tramites", {}).get("tramites", [])
    tramites_filtrados = [
        t for t in tramites_data 
        if persona in t.get("personas_afectadas", [])
    ]
    return tramites_filtrados

def obtener_movimientos_persona(datos, persona):
    """Retorna movimientos (ahorro/gastos) de una persona."""
    movimientos = datos.get("movimientos", {}).get("movimientos", [])
    movimientos_filtrados = [
        m for m in movimientos 
        if m.get("persona") == persona
    ]
    return movimientos_filtrados

def obtener_saldo_persona(datos, persona):
    """Calcula saldo neto (ahorrado - gastado) de una persona."""
    resumen = datos.get("movimientos", {}).get("resumen_por_persona", {})
    return resumen.get(persona, {}).get("saldo_neto_soles", 0)

def obtener_bolsa_info(datos):
    """Retorna información de la bolsa migratoria."""
    return datos.get("bolsa_migracion", {}).get("bolsa_migracion", {})

def guardar_datos_json(nombre_archivo, datos):
    """Guarda el diccionario actualizado en el archivo JSON correspondiente."""
    ruta = Path(__file__).parent.parent / nombre_archivo
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
