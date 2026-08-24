import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Agregar módulos al path
sys.path.insert(0, str(Path(__file__).parent))

from modules.data_loader import cargar_todos_datos, obtener_personas
from modules.calculadora import (
    calcular_totales_movimientos,
    calcular_progreso_bolsa,
    calcular_por_persona,
    obtener_kpis_principales,
    calcular_progreso_tiempo,
    calcular_dias_faltantes
)
from modules.conversiones import formato_moneda_soles, formato_moneda_cad, sol_a_cad

# ===== CONFIGURACIÓN STREAMLIT =====
st.set_page_config(
    page_title="Calgary Migration Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== ESTILOS CSS =====
st.markdown("""
<style>
    .main { padding: 1rem; }
    .metric-card { background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; }
    h1 { color: #667eea; }
    h2 { color: #764ba2; }
    .success { color: #10b981; font-weight: bold; }
    .danger { color: #ef4444; font-weight: bold; }
    .warning { color: #f59e0b; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ===== CARGAR DATOS =====
@st.cache_data
def load_data():
    return cargar_todos_datos()

datos = load_data()

# ===== HEADER =====
st.markdown("# 🚀 Dashboard de Migración Calgary 2026-2027")
st.markdown("**2 Personas** | Objetivo: Junio 2027")
st.markdown("---")

# ===== SIDEBAR =====
st.sidebar.title("📌 Navegación")
pagina = st.sidebar.radio(
    "Selecciona una sección:",
    ["📊 Resumen Ejecutivo", "📅 Línea de Tiempo", "💰 Ahorro & Gastos", 
     "💵 Presupuesto", "🎫 Bolsa Migratoria", "⚙️ Configuración"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Estado del Proyecto**")
progreso_tiempo = calcular_progreso_tiempo(datos)
st.sidebar.progress(min(progreso_tiempo.get("progreso_pct", 0), 100) / 100)
st.sidebar.metric(
    "Tiempo Transcurrido",
    f"{progreso_tiempo.get('dias_transcurridos', 0)} / {progreso_tiempo.get('dias_totales', 0)} días"
)

# ===== PÁGINA 1: RESUMEN EJECUTIVO =====
if pagina == "📊 Resumen Ejecutivo":
    st.header("📊 Resumen Ejecutivo")
    
    # Cargar KPIs
    kpis = obtener_kpis_principales(datos)
    
    # Mostrar KPI cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Ahorrado",
            formato_moneda_soles(kpis["ahorrado_soles"]),
            f"{kpis['progreso_bolsa_pct']:.1f}% meta"
        )
    
    with col2:
        st.metric(
            "📊 Gastado",
            formato_moneda_soles(kpis["gastado_soles"]),
            "En trámites"
        )
    
    with col3:
        st.metric(
            "💵 Saldo Disponible",
            formato_moneda_soles(kpis["saldo_disponible_soles"]),
            f"≈ {formato_moneda_cad(kpis['saldo_disponible_cad'])}"
        )
    
    with col4:
        st.metric(
            "📅 Días para Viaje",
            kpis["dias_faltantes"],
            "Junio 15, 2027"
        )
    
    st.markdown("---")
    
    # Gráficos
    col_grafico1, col_grafico2 = st.columns(2)
    
    with col_grafico1:
        st.subheader("Progreso Bolsa Migratoria")
        progreso_bolsa = calcular_progreso_bolsa(datos)
        
        fig = go.Figure(data=[
            go.Pie(
                labels=["Ahorrado", "Falta"],
                values=[
                    progreso_bolsa["ahorrado_soles"],
                    max(0, progreso_bolsa["falta_soles"])
                ],
                marker=dict(colors=["#10b981", "#e5e7eb"])
            )
        ])
        st.plotly_chart(fig, use_container_width=True)
    
    with col_grafico2:
        st.subheader("Ahorrado vs Gastado")
        totales = calcular_totales_movimientos(datos)
        
        fig = go.Figure(data=[
            go.Bar(
                name="Ahorrado",
                x=["Soles"],
                y=[totales["total_ahorrado_soles"]],
                marker=dict(color="#10b981")
            ),
            go.Bar(
                name="Gastado",
                x=["Soles"],
                y=[totales["total_gastado_soles"]],
                marker=dict(color="#ef4444")
            )
        ])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📋 Próximos Pasos")
    
    proximos = [
        "✅ Pasaportes (Agosto 2026)",
        "✅ Apostillas (Agosto 2026)",
        "📋 ECA - Evaluación de Credenciales (Agosto 2026)",
        "📋 IELTS CLB 7 (Septiembre-Octubre 2026)",
        "📋 Express Entry (Enero 2027)",
        "🎫 Compra de Vuelos (Abril-Mayo 2027)"
    ]
    
    for paso in proximos:
        st.write(paso)

# ===== PÁGINA 2: LÍNEA DE TIEMPO =====
elif pagina == "📅 Línea de Tiempo":
    st.header("📅 Línea de Tiempo del Proyecto")
    
    col_l1, col_l2 = st.columns(2)
    
    with col_l1:
        st.subheader("👩‍💼 Persona_L_01")
        cronograma = datos.get("cronograma", {}).get("cronograma", {})
        liz_timeline = cronograma.get("linea_tiempo_persona", {}).get("Liz", [])
        
        for item in liz_timeline:
            mes = item.get("mes", "")
            hito = item.get("hito", "")
            costo_soles = item.get("costo_soles", 0)
            costo_cad = item.get("costo_cad", 0)
            
            if costo_soles > 0:
                st.write(f"**{mes}:** {hito}")
                st.write(f"└─ Costo: {formato_moneda_soles(costo_soles)}")
            elif costo_cad > 0:
                st.write(f"**{mes}:** {hito}")
                st.write(f"└─ Costo: {formato_moneda_cad(costo_cad)}")
            else:
                st.write(f"**{mes}:** {hito}")
    
    with col_l2:
        st.subheader("👨‍💻 Persona_J_02 (Técnico IT)")
        jhon_timeline = cronograma.get("linea_tiempo_persona", {}).get("Jhon", [])
        
        for item in jhon_timeline:
            mes = item.get("mes", "")
            hito = item.get("hito", "")
            costo_soles = item.get("costo_soles", 0)
            costo_cad = item.get("costo_cad", 0)
            
            if costo_soles > 0:
                st.write(f"**{mes}:** {hito}")
                st.write(f"└─ Costo: {formato_moneda_soles(costo_soles)}")
            elif costo_cad > 0:
                st.write(f"**{mes}:** {hito}")
                st.write(f"└─ Costo: {formato_moneda_cad(costo_cad)}")
            else:
                st.write(f"**{mes}:** {hito}")

# ===== PÁGINA 3: AHORRO & GASTOS =====
elif pagina == "💰 Ahorro & Gastos":
    st.header("💰 Registro de Ahorro & Gastos")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.subheader("👩‍💼 Persona_L_01")
        info_liz = calcular_por_persona(datos, "Persona_L_01")
        st.metric("Ahorrado", formato_moneda_soles(info_Persona_L_01["total_ahorrado_soles"]))
        st.metric("Gastado", formato_moneda_soles(info_Persona_L_01["total_gastado_soles"]))
        st.metric("Saldo", formato_moneda_soles(info_Persona_L_01["saldo_soles"]))
    
    with col_a2:
        st.subheader("👨‍💻 Persona_J_02")
        info_jhon = calcular_por_persona(datos, "Persona_J_02")
        st.metric("Ahorrado", formato_moneda_soles(info_Persona_J_02["total_ahorrado_soles"]))
        st.metric("Gastado", formato_moneda_soles(info_Persona_J_02["total_gastado_soles"]))
        st.metric("Saldo", formato_moneda_soles(info_Persona_J_02["saldo_soles"]))
    
    st.markdown("---")
    
    st.subheader("📊 Tabla de Movimientos")
    movimientos = datos.get("movimientos", {}).get("movimientos", [])
    
    if movimientos:
        df = pd.DataFrame(movimientos)
        df_display = df[["fecha", "persona", "tipo", "concepto", "monto_original", "moneda_original"]].copy()
        df_display.columns = ["Fecha", "Persona", "Tipo", "Concepto", "Monto", "Moneda"]
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("Sin movimientos registrados aún.")

# ===== PÁGINA 4: PRESUPUESTO =====
elif pagina == "💵 Presupuesto":
    st.header("💵 Presupuesto Detallado")
    
    presupuesto = datos.get("presupuesto", {}).get("presupuesto", {})
    
    st.subheader("💱 Gastos en Soles (Perú)")
    gastos_soles = presupuesto.get("gastos_en_soles", {}).get("items", [])
    
    if gastos_soles:
        df_soles = pd.DataFrame(gastos_soles)
        df_soles_display = df_soles[["nombre", "costo"]].copy()
        df_soles_display.columns = ["Trámite", "Costo (S/)"]
        st.dataframe(df_soles_display, use_container_width=True)
        st.metric("Subtotal S/", formato_moneda_soles(presupuesto.get("gastos_en_soles", {}).get("subtotal_soles", 0)))
    
    st.markdown("---")
    
    st.subheader("🍁 Gastos en CAD$ (Canadá)")
    gastos_cad = presupuesto.get("gastos_en_cad", {}).get("items", [])
    
    if gastos_cad:
        df_cad = pd.DataFrame(gastos_cad)
        df_cad_display = df_cad[["nombre", "costo"]].copy()
        df_cad_display.columns = ["Trámite", "Costo (CAD$)"]
        st.dataframe(df_cad_display, use_container_width=True)
        st.metric("Subtotal CAD$", formato_moneda_cad(presupuesto.get("gastos_en_cad", {}).get("subtotal_cad", 0)))

# ===== PÁGINA 5: BOLSA MIGRATORIA =====
elif pagina == "🎫 Bolsa Migratoria":
    st.header("🎫 Bolsa Migratoria")
    
    bolsa = datos.get("bolsa_migracion", {}).get("bolsa_migracion", {})
    objetivo = bolsa.get("objetivo", {})
    
    st.info(f"**Meta:** {formato_moneda_soles(objetivo.get('meta_soles', 0))} ≈ {formato_moneda_cad(objetivo.get('meta_cad', 0))}")
    
    progreso_bolsa = calcular_progreso_bolsa(datos)
    
    col_prog1, col_prog2 = st.columns(2)
    
    with col_prog1:
        st.metric("Ahorrado", formato_moneda_soles(progreso_bolsa["ahorrado_soles"]))
    
    with col_prog2:
        st.metric("Falta", formato_moneda_soles(progreso_bolsa["falta_soles"]))
    
    st.progress(min(progreso_bolsa["progreso_pct"] / 100, 1.0))
    st.write(f"**Progreso:** {progreso_bolsa['progreso_pct']:.1f}%")
    
    st.markdown("---")
    
    st.subheader("📈 Proyección Mensual")
    proyeccion = bolsa.get("proyeccion_mensual", [])
    
    if proyeccion:
        df_proyeccion = pd.DataFrame(proyeccion)
        df_proyeccion_display = df_proyeccion[[
            "mes", "liz_ahorro_soles", "jhon_ahorro_soles", 
            "gastos_soles", "saldo_acumulado_soles", "progreso_pct"
        ]].copy()
        df_proyeccion_display.columns = [
            "Mes", "Persona_L_01 Ahorro", "Persona_J_02 Ahorro", "Gastos", "Saldo Acumulado", "Progreso %"
        ]
        st.dataframe(df_proyeccion_display, use_container_width=True)

# ===== PÁGINA 6: CONFIGURACIÓN =====
elif pagina == "⚙️ Configuración":
    st.header("⚙️ Configuración del Proyecto")
    
    config = datos.get("config", {})
    
    st.subheader("📌 Información del Proyecto")
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.write("**Personas:**")
        personas = config.get("personas", {})
        for persona, info in personas.items():
            st.write(f"- {persona}: {info.get('nombre_completo', '')}")
    
    with col_info2:
        st.write("**Ubicaciones:**")
        ubicaciones = config.get("ubicaciones", {})
        origen = ubicaciones.get("origen", {})
        destino = ubicaciones.get("destino", {})
        st.write(f"De: {origen.get('pais', '')} ({origen.get('simbolo', '')})")
        st.write(f"A: {destino.get('ciudad', '')}, {destino.get('provincia', '')} ({destino.get('simbolo', '')})")
    
    st.markdown("---")
    
    st.subheader("💱 Tasas de Cambio (Última actualización)")
    tasas = config.get("tasas_cambio", {})
    
    col_tasa1, col_tasa2, col_tasa3, col_tasa4 = st.columns(4)
    
    with col_tasa1:
        st.metric("S/ → CAD$", tasas.get("sol_a_cad", 0))
    with col_tasa2:
        st.metric("CAD$ → S/", tasas.get("cad_a_sol", 0))
    with col_tasa3:
        st.metric("S/ → USD", tasas.get("sol_a_usd", 0))
    with col_tasa4:
        st.metric("USD → CAD$", tasas.get("usd_a_cad", 0))
    
    st.write(f"**Fuente:** {tasas.get('fuente', '')} - {tasas.get('fecha_actualizacion', '')}")
    
    st.markdown("---")
    
    st.subheader("🎯 Metas Financieras")
    metas = config.get("metas_financieras", {})
    
    for meta_name, meta_value in metas.items():
        st.write(f"**{meta_name}:** {formato_moneda_soles(meta_value) if isinstance(meta_value, (int, float)) else meta_value}")

# ===== FOOTER =====
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "Dashboard de Migración Calgary | Última actualización: Agosto 2026 | "
    "<a href='https://github.com/Lizmarquez2/Life-in-other-Country'>GitHub</a>"
    "</p>",
    unsafe_allow_html=True
)
