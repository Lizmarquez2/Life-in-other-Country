# config.py - Configuración Global del Dashboard

import os
from datetime import datetime

# ===== INFORMACIÓN DEL PROYECTO =====
PROYECTO = {
    "nombre": "Migración Calgary 2026-2027",
    "descripcion": "Dashboard de seguimiento para migración Persona_L_01 + Persona_J_02 a Calgary, Alberta, Canadá",
    "versión": "1.0.0",
    "fecha_creación": "2026-08-01"
}

# ===== PERSONAS =====
PERSONAS = {
    "Persona_L_01": {
        "nombre_completo": "Persona_L_01",
        "rol": "Contador Público",
        "experiencia_años": 7,
        "especialidad": "Costos Hospitalarios",
        "perfil_migracion": "Profesional TEER 1"
    },
    "Persona_J_02": {
        "nombre_completo": "Persona_J_02 (Esposo)",
        "rol": "Técnico en Informática",
        "experiencia_años": 10,
        "especialidad": "IT Support (Linux/Windows)",
        "perfil_migracion": "Técnico TEER 2"
    }
}

# ===== UBICACIONES =====
UBICACIONES = {
    "origen": {
        "pais": "Perú",
        "ciudad": "Lima",
        "moneda": "PEN",
        "simbolo": "S/"
    },
    "destino": {
        "pais": "Canadá",
        "provincia": "Alberta",
        "ciudad": "Calgary",
        "moneda": "CAD",
        "simbolo": "CAD $"
    }
}

# ===== TASAS DE CAMBIO (ActuaPersona_L_01ar regularmente) =====
TASAS_CAMBIO = {
    "sol_a_cad": 0.27,      # 1 S/ = 0.27 CAD
    "cad_a_sol": 3.70,      # 1 CAD = 3.70 S/
    "sol_a_usd": 0.20,      # 1 S/ = 0.20 USD
    "usd_a_cad": 1.35,      # 1 USD = 1.35 CAD
    "fecha_actuaPersona_L_01acion": "2026-08-01",
    "fuente": "XE.com"
}

# ===== FECHAS CLAVE =====
FECHAS = {
    "fecha_inicio_proyecto": "2026-08-01",
    "fecha_objetivo_viaje": "2027-06-15",
    "meses_disponibles": 10,
    "dias_disponibles": 318
}

# ===== METAS FINANCIERAS =====
METAS = {
    "bolsa_migracion_meta_soles": 60000,
    "bolsa_migracion_meta_cad": 16200,
    "presupuesto_tramites_soles": 24366.20,
    "ahorro_mensual_meta_soles": 6000,
    "ahorro_por_persona_mes_soles": 3000
}

# ===== DIRECTORIOS DE DATOS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Archivos JSON
ARCHIVOS_DATA = {
    "config": os.path.join(DATA_DIR, "config.json"),
    "tramites": os.path.join(DATA_DIR, "tramites.json"),
    "cronograma": os.path.join(DATA_DIR, "cronograma.json"),
    "movimientos": os.path.join(DATA_DIR, "movimientos.json"),
    "presupuesto": os.path.join(DATA_DIR, "presupuesto.json"),
    "bolsa_migracion": os.path.join(DATA_DIR, "bolsa_migracion.json")
}

# ===== CONFIGURACIÓN STREAMLIT =====
STREAMLIT_CONFIG = {
    "page_title": "Calgary Migration Dashboard",
    "page_icon": "🚀",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# ===== ESTILOS Y COLORES =====
COLORES = {
    "primario": "#667eea",
    "secundario": "#764ba2",
    "positivo": "#10b981",
    "negativo": "#ef4444",
    "advertencia": "#f59e0b",
    "info": "#3b82f6"
}

# ===== MENSAJES =====
MENSAJES = {
    "bienvenida": "🚀 Dashboard de Migración Calgary | Persona_L_01 + Persona_J_02",
    "objetivo": "Objetivo: Viajar a Calgary en Junio 2027",
    "cargando": "⏳ Cargando datos...",
    "error_datos": "❌ Error al cargar datos",
    "sin_movimientos": "📭 Sin movimientos registrados"
}

# ===== CATEGORÍAS DE TRÁMITES =====
CATEGORIAS_TRAMITES = [
    "Documentación Base",
    "Evaluaciones Canadá",
    "Exámenes de Idioma",
    "Solicitud Inmigración",
    "Seguro y Viaje",
    "Transporte"
]

# ===== ESTADOS DE TRÁMITES =====
ESTADOS_TRAMITES = [
    "Pendiente",
    "En Progreso",
    "Completado",
    "Bloqueado"
]

# ===== TIPO DE MOVIMIENTOS =====
TIPOS_MOVIMIENTOS = ["AHORRO", "GASTO"]

# ===== CONTEXTO PARA VALIDACIONES =====
VALIDACIONES = {
    "monto_minimo": 1,
    "monto_maximo": 100000,
    "largo_minimo_concepto": 3,
    "largo_maximo_concepto": 200
}
