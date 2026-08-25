import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Agregar módulos al path
sys.path.insert(0, str(Path(__file__).parent))

from modules.data_loader import cargar_todos_datos, obtener_personas, guardar_datos_json
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

# --- SINCRONIZACIÓN DE MOVIMIENTOS EN SESIÓN ---
if "movimientos_session" not in st.session_state:
    st.session_state.movimientos_session = datos.get("movimientos", {}).get("movimientos", [])

if "movimientos" not in datos:
    datos["movimientos"] = {}
datos["movimientos"]["movimientos"] = st.session_state.movimientos_session

# ===== HEADER =====
st.markdown("# 🚀 Dashboard de Migración Calgary 2026-2027")
st.markdown("**2 Personas** | Objetivo: Junio 2027")
st.markdown("---")

# ===== SIDEBAR =====
st.sidebar.title("📌 Navegación")
pagina = st.sidebar.radio(
    "Selecciona una sección:",
    ["📊 Resumen Ejecutivo", "📅 Línea de Tiempo", "💰 Ahorro & Gastos", 
     "💵 Presupuesto", "🎫 Bolsa Migratoria", "📋 Trámites y Mapeo","⚙️ Configuración"]
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
        progreso_bolsa = calcular_progreso_bolsa(datos)
        meta_total = progreso_bolsa["meta_soles"]
        ahorrado_actual = progreso_bolsa["ahorrado_soles"]
        falta_dinero = meta_total - ahorrado_actual
        
        # Ritmo de ahorro mensual estimado (puedes ajustarlo si prefieres 1,000 o 1,500)
        ahorro_mensual_estimado = 1200.0 
        
        if ahorrado_actual >= meta_total:
            st.metric(
                "⏳ Tiempo para Viaje",
                "¡Meta Cumplida!",
                "Listos para Canadá ✈️"
            )
        else:
            # Calculamos los meses totales que faltan
            meses_totales = max(0.1, falta_dinero / ahorro_mensual_estimado)
            
            # Convertimos a años y meses enteros
            anos = int(meses_totales // 12)
            meses_restantes = int(meses_totales % 12)
            
            # Construimos el texto dinámico según el tiempo estimado
            if anos > 0:
                tiempo_texto = f"{anos} año{'s' if anos > 1 else ''} y {meses_restantes} mes{'es' if meses_restantes != 1 else ''}"
            else:
                tiempo_texto = f"{meses_restantes} mes{'es' if meses_restantes != 1 else ''}"
                
            st.metric(
                "⏳ Tiempo Proyectado",
                tiempo_texto,
                f"Faltan {formato_moneda_soles(falta_dinero)}"
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
    st.write("Seguimiento de hitos y etapas clave hacia nuestra llegada a Canadá.")
    
    col_l1, col_l2 = st.columns(2)
    
    cronograma = datos.get("cronograma", {}).get("cronograma", {})
    
    with col_l1:
        st.subheader("👩‍💼 Persona_L_01")
        Persona_L_01_timeline = cronograma.get("linea_tiempo_persona", {}).get("Persona_L_01", [])
        
        for item in Persona_L_01_timeline:
            mes = item.get("mes", "")
            hito = item.get("hito", "")
            costo_soles = item.get("costo_soles", 0)
            costo_cad = item.get("costo_cad", 0)
            
            # Mostramos el hito con un formato claro
            st.markdown(f"📌 **{mes}**")
            st.write(f"↳ {hito}")
            if costo_soles > 0:
                st.caption(f"Costo: S/ {costo_soles:,.2f}")
            elif costo_cad > 0:
                st.caption(f"Costo: CAD $ {costo_cad:,.2f}")
            st.markdown("---")
            
    with col_l2:
        st.subheader("👨‍💻 Persona_J_02 (Técnico IT)")
        Persona_J_02_timeline = cronograma.get("linea_tiempo_persona", {}).get("Persona_J_02", [])
        
        for item in Persona_J_02_timeline:
            mes = item.get("mes", "")
            hito = item.get("hito", "")
            costo_soles = item.get("costo_soles", 0)
            costo_cad = item.get("costo_cad", 0)
            
            st.markdown(f"📌 **{mes}**")
            st.write(f"↳ {hito}")
            if costo_soles > 0:
                st.caption(f"Costo: S/ {costo_soles:,.2f}")
            elif costo_cad > 0:
                st.caption(f"Costo: CAD $ {costo_cad:,.2f}")
            st.markdown("---")

# ===== PÁGINA 3: AHORRO & GASTOS =====
elif pagina == "💰 Ahorro & Gastos":
    st.header("💰 Registro de Ahorro & Gastos")
    
    # 1. Inicializamos la sesión si no existe
    if "movimientos_session" not in st.session_state:
        st.session_state.movimientos_session = datos.get("movimientos", {}).get("movimientos", [])

    movimientos_actuales = st.session_state.movimientos_session

    # 2. Función auxiliar directa para calcular totales por persona de forma dinámica
    def calcular_totales_directos(movimientos, persona_id):
        total_ahorrado = sum(
            m.get("monto_original", 0) for m in movimientos 
            if m.get("persona") == persona_id and m.get("tipo") == "AHORRO"
        )
        total_gastado = sum(
            m.get("monto_original", 0) for m in movimientos 
            if m.get("persona") == persona_id and m.get("tipo") == "GASTO"
        )
        saldo = total_ahorrado - total_gastado
        return {
            "total_ahorrado_soles": total_ahorrado,
            "total_gastado_soles": total_gastado,
            "saldo_soles": saldo
        }

    info_Persona_L_01 = calcular_totales_directos(movimientos_actuales, "Persona_L_01")
    info_Persona_J_02 = calcular_totales_directos(movimientos_actuales, "Persona_J_02")

    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.subheader("👩‍💼 Persona_L_01")
        st.metric("Ahorrado", formato_moneda_soles(info_Persona_L_01["total_ahorrado_soles"]))
        st.metric("Gastado", formato_moneda_soles(info_Persona_L_01["total_gastado_soles"]))
        st.metric("Saldo", formato_moneda_soles(info_Persona_L_01["saldo_soles"]))
    
    with col_a2:
        st.subheader("👨‍💻 Persona_J_02")
        st.metric("Ahorrado", formato_moneda_soles(info_Persona_J_02["total_ahorrado_soles"]))
        st.metric("Gastado", formato_moneda_soles(info_Persona_J_02["total_gastado_soles"]))
        st.metric("Saldo", formato_moneda_soles(info_Persona_J_02["saldo_soles"]))
    
    st.markdown("---")
    
    st.subheader("📊 Tabla de Movimientos")
    
    # Mostramos los movimientos desde la sesión activa
    movimientos_actuales = st.session_state.movimientos_session
    
    if movimientos_actuales:
        df = pd.DataFrame(movimientos_actuales)
        df_display = df[["fecha", "persona", "tipo", "concepto", "monto_original", "moneda_original"]].copy()
        df_display.columns = ["Fecha", "Persona", "Tipo", "Concepto", "Monto", "Moneda"]
        st.dataframe(df_display, use_container_width=True)
        
        # --- SECCIÓN PARA ELIMINAR MOVIMIENTOS ERRÓNEOS ---
        with st.expander("🗑️ Eliminar un movimiento equivocado"):
            opciones_movimientos = [
                f"#{i} - {m.get('fecha')} | {m.get('persona')} | {m.get('concepto')} | S/ {m.get('monto_original')}"
                for i, m in enumerate(movimientos_actuales)
            ]
            
            movimiento_a_borrar = st.selectbox("Selecciona el movimiento a eliminar", opciones_movimientos)
            
            if st.button("Eliminar Registro Seleccionado", type="primary"):
                indice_a_borrar = opciones_dict[movimiento_seleccionado]
                st.session_state.movimientos_session.pop(indice_a_borrar)
                
                datos["movimientos"]["movimientos"] = st.session_state.movimientos_session
                guardar_datos_json(datos)
                
                # 🧹 Limpiamos la caché aquí también
                st.cache_data.clear()
                
                st.success("¡Movimiento eliminado con éxito!")
                st.rerun()
    else:
        st.info("Sin movimientos registrados aún.")

    st.subheader("📝 Registrar Nuevo Movimiento")

    with st.form("form_movimiento", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha")
            persona = st.selectbox("Persona", ["Persona_L_01", "Persona_J_02"])
            tipo = st.selectbox("Tipo de Movimiento", ["AHORRO", "GASTO"])
        with col2:
            monto = st.number_input("Monto", min_value=0.0, step=10.0)
            moneda = st.selectbox("Moneda", ["PEN", "CAD", "USD"])
            
        concepto = st.selectbox(
            "Concepto / Descripción", 
            [
                "Ahorro mensual",
                "Pasaportes (2 personas)",
                "Apostillas títulos (2 personas)",
                "Antecedentes penales (2 personas)",
                "Vuelos Lima-Calgary (2 personas)",
                "ECA - Persona_L_01",
                "ECA - Persona_J_02",
                "IELTS CLB 7 - Persona_L_01",
                "IELTS CLB 7 - Persona_J_02",
                "Express Entry (pareja)",
                "Seguro médico (3 meses)",
                "Gastos varios / Contingencia",
                "Bolsa de Viaje"
            ]
        )
        
        observaciones = st.text_input("Observaciones (Opcional)")
        
        submitted = st.form_submit_button("Guardar Movimiento")
        
        if submitted:
            nuevo_registro = {
                "fecha": str(fecha),
                "persona": persona,
                "tipo": tipo,
                "concepto": concepto,
                "monto_original": monto,
                "moneda_original": moneda,
                "observaciones": observaciones
            }
            
           # Al guardar un movimiento:
            st.session_state.movimientos_session.append(nuevo_registro)
            datos["movimientos"]["movimientos"] = st.session_state.movimientos_session
            
            guardar_datos_json(datos)
            
            # 🧹 Limpiamos la caché de Streamlit para obligarlo a leer el nuevo JSON la próxima vez
            st.cache_data.clear()
            
            st.success("¡Movimiento registrado y guardado con éxito!")
            st.rerun()

# ===== PÁGINA 4: PRESUPUESTO =====
elif pagina == "💵 Presupuesto":
    st.header("💵 Presupuesto Detallado")
    
    # Obtenemos el tipo de cambio de la configuración
    configuracion = datos.get("configuracion", {})
    tipo_cambio_cad = configuracion.get("tipo_cambio_cad", datos.get("tipo_cambio", 2.75))
    
    # 💱 GASTOS EN SOLES (Perú)
    st.subheader("💱 Gastos en Soles (Perú)")
    st.write("Presupuesto base y desglose detallado para el seguimiento de trámites.")
    
    if "presupuesto_soles_detallado" not in st.session_state:
        st.session_state.presupuesto_soles_detallado = [
            {
                "tramite_principal": "Pasaportes (2 personas)",
                "costo_total_base": 241.80,
                "desglose": [
                    {"subitem": "Pasaporte Persona_L_01", "costo_unitario": 120.90, "cantidad": 1},
                    {"subitem": "Pasaporte Persona_J_02", "costo_unitario": 120.90, "cantidad": 1}
                ]
            },
            {
                "tramite_principal": "Apostillas títulos (2 personas)",
                "costo_total_base": 92.00,
                "desglose": [
                    {"subitem": "Título Universitario", "costo_unitario": 46.00, "cantidad": 2},
                    {"subitem": "Título Técnico", "costo_unitario": 46.00, "cantidad": 0},
                    {"subitem": "Certificados de Estudios", "costo_unitario": 46.00, "cantidad": 0}
                ]
            },
            {
                "tramite_principal": "Antecedentes penales (2 personas)",
                "costo_total_base": 162.80,
                "desglose": [
                    {"subitem": "Certificado Antecedentes Penales", "costo_unitario": 81.40, "cantidad": 2}
                ]
            },
            {
                "tramite_principal": "Vuelos Lima-Calgary (2 personas)",
                "costo_total_base": 12000.00,
                "desglose": [
                    {"subitem": "Pasajes Aéreos Lima-Calgary", "costo_unitario": 6000.00, "cantidad": 2}
                ]
            }
        ]

    subtotal_soles_general = 0

    for idx, grupo in enumerate(st.session_state.presupuesto_soles_detallado):
        st.markdown(f"### 📌 {grupo['tramite_principal']}")
        
        subtotal_grupo = 0
        for sub_idx, item in enumerate(grupo["desglose"]):
            col_d1, col_d2, col_d3, col_d4 = st.columns([3, 1.5, 1, 1.5])
            with col_d1:
                st.write(f"• {item['subitem']}")
            with col_d2:
                st.text(f"S/ {item['costo_unitario']:,.2f}")
            with col_d3:
                nueva_cant = st.number_input(
                    "Cant", 
                    min_value=0, 
                    value=item["cantidad"], 
                    step=1, 
                    key=f"soles_{idx}_{sub_idx}",
                    label_visibility="collapsed"
                )
                item["cantidad"] = nueva_cant
            with col_d4:
                total_sub = item["costo_unitario"] * item["cantidad"]
                subtotal_grupo += total_sub
                st.text(f"S/ {total_sub:,.2f}")
                
        grupo["costo_total_base"] = subtotal_grupo
        subtotal_soles_general += subtotal_grupo
        st.caption(f"Subtotal para **{grupo['tramite_principal']}**: S/ {subtotal_grupo:,.2f}")
        st.markdown("---")

    st.metric("Subtotal S/", formato_moneda_soles(subtotal_soles_general))
    
    st.markdown("---")
    
    # 🍁 GASTOS EN CAD$ (Canadá)
    st.subheader("🍁 Gastos en CAD$ (Canadá)")
    st.write("Manteniendo la estructura de trazabilidad inicial con sus desgloses correspondientes.")
    
    if "presupuesto_cad_detallado" not in st.session_state:
        st.session_state.presupuesto_cad_detallado = [
            {
                "tramite_principal": "ECA - Persona_L_01",
                "costo_total_base": 329.00,
                "desglose": [{"subitem": "Evaluación WES/ICES - L", "costo_unitario": 329.00, "cantidad": 1}]
            },
            {
                "tramite_principal": "ECA - Persona_J_02",
                "costo_total_base": 329.00,
                "desglose": [{"subitem": "Evaluación WES/ICES - J", "costo_unitario": 329.00, "cantidad": 1}]
            },
            {
                "tramite_principal": "IELTS CLB 7 - Persona_L_01",
                "costo_total_base": 350.00,
                "desglose": [{"subitem": "Examen IELTS General - L", "costo_unitario": 350.00, "cantidad": 1}]
            },
            {
                "tramite_principal": "IELTS CLB 7 - Persona_J_02",
                "costo_total_base": 350.00,
                "desglose": [{"subitem": "Examen IELTS General - J", "costo_unitario": 350.00, "cantidad": 1}]
            },
            {
                "tramite_principal": "Express Entry (pareja)",
                "costo_total_base": 1250.00,
                "desglose": [{"subitem": "Tasas de Visado / Portal Online", "costo_unitario": 1250.00, "cantidad": 1}]
            },
            {
                "tramite_principal": "Seguro médico (3 meses)",
                "costo_total_base": 600.00,
                "desglose": [
                    {"subitem": "Cobertura inicial de salud (2 personas x 3 meses)", "costo_unitario": 100.00, "cantidad": 6}
                ]
            }
        ]

    subtotal_cad_general = 0
    subtotal_cad_en_soles = 0

    for idx, grupo in enumerate(st.session_state.presupuesto_cad_detallado):
        st.markdown(f"### 📌 {grupo['tramite_principal']}")
        
        subtotal_grupo_cad = 0
        for sub_idx, item in enumerate(grupo["desglose"]):
            col_c1, col_c2, col_c3, col_c4, col_c5 = st.columns([2.5, 1.2, 1, 1.3, 1.3])
            with col_c1:
                st.write(f"• {item['subitem']}")
            with col_c2:
                st.text(f"CAD $ {item['costo_unitario']:,.2f}")
            with col_c3:
                nueva_cant_cad = st.number_input(
                    "Cant", 
                    min_value=0, 
                    value=item["cantidad"], 
                    step=1, 
                    key=f"cad_{idx}_{sub_idx}",
                    label_visibility="collapsed"
                )
                item["cantidad"] = nueva_cant_cad
            with col_c4:
                total_sub_cad = item["costo_unitario"] * item["cantidad"]
                subtotal_grupo_cad += total_sub_cad
                st.text(f"CAD $ {total_sub_cad:,.2f}")
            with col_c5:
                total_sub_soles = total_sub_cad * tipo_cambio_cad
                st.text(f"S/ {total_sub_soles:,.2f}")
                
        grupo["costo_total_base"] = subtotal_grupo_cad
        subtotal_cad_general += subtotal_grupo_cad
        subtotal_cad_en_soles += (subtotal_grupo_cad * tipo_cambio_cad)
        st.caption(f"Subtotal para **{grupo['tramite_principal']}**: CAD $ {subtotal_grupo_cad:,.2f} (≈ S/ {subtotal_grupo_cad * tipo_cambio_cad:,.2f})")
        st.markdown("---")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Subtotal CAD$", formato_moneda_cad(subtotal_cad_general))
    with col_m2:
        st.metric(
            "Subtotal Equivalente en Soles", 
            formato_moneda_soles(subtotal_cad_en_soles), 
            help=f"Tipo de cambio API: 1 CAD = {tipo_cambio_cad} PEN"
        )

# ===== PÁGINA 5: BOLSA MIGRATORIA =====
elif pagina == "🎫 Bolsa Migratoria":
    st.header("🎫 Bolsa Migratoria (Prueba de Fondos)")
    st.write("Fondo intocable destinado exclusivamente a la acreditación de fondos requeridos por Canadá.")
    
    bolsa = datos.get("bolsa_migracion", {}).get("bolsa_migracion", {})
    objetivo = bolsa.get("objetivo", {})
    
    st.info(f"**Meta de Acreditación:** {formato_moneda_soles(objetivo.get('meta_soles', 0))} ≈ {formato_moneda_cad(objetivo.get('meta_cad', 0))}")
    
    progreso_bolsa = calcular_progreso_bolsa(datos)
    
    col_prog1, col_prog2 = st.columns(2)
    
    with col_prog1:
        st.metric("Ahorrado Actual", formato_moneda_soles(progreso_bolsa["ahorrado_soles"]))
    
    with col_prog2:
        st.metric("Falta por Ahorrar", formato_moneda_soles(progreso_bolsa["falta_soles"]))
    
    st.progress(min(progreso_bolsa["progreso_pct"] / 100, 1.0))
    st.write(f"**Progreso de la Meta:** {progreso_bolsa['progreso_pct']:.1f}%")
    
    st.markdown("---")
    
    # --- SIMULADOR DINÁMICO DE APORTES ---
    st.subheader("⚙️ Simulador de Aportes Mensuales (Sin Gastos)")
    st.write("Define los aportes limpios destinados 100% a la cuenta de fondos migratorios.")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        nuevo_ahorro_Persona_L_01 = st.number_input("Aporte mensual Persona_L_01 (S/)", value=700.0, step=50.0)
    with col_s2:
        nuevo_ahorro_Persona_J_02 = st.number_input("Aporte mensual Persona_J_02 (S/)", value=250.0, step=50.0)
        
    aporte_mensual_total = nuevo_ahorro_Persona_L_01 + nuevo_ahorro_Persona_J_02
    meta_total = objetivo.get('meta_soles', 60000)
    meta_faltante = meta_total - progreso_bolsa["ahorrado_soles"]
    
    if aporte_mensual_total > 0:
        meses_estimados = meta_faltante / aporte_mensual_total
        anos_estimados = meses_estimados / 12  
        st.success(f"💡 Con un aporte conjunto libre de gastos de S/ {aporte_mensual_total:,.2f} mensuales, te tomará aproximadamente **{anos_estimados:.1f} años** ({meses_estimados:.1f} meses) completar la bolsa migratoria.")
    else:
        st.warning("⚠️ Ingresa aportes mayores a cero para calcular la estimación.")
        
    st.markdown("---")
    
    st.subheader("📈 Proyección de Crecimiento de la Bolsa")
    proyeccion = bolsa.get("proyeccion_mensual", [])
    
    if proyeccion:
        df_proyeccion = pd.DataFrame(proyeccion)
        
        meses_necesarios = int(meses_estimados) + 1 if aporte_mensual_total > 0 else len(df_proyeccion)
        
        if len(df_proyeccion) < meses_necesarios:
            ultimo_mes = pd.to_datetime("2026-08-01")
            fechas_extendidas = pd.date_range(start=ultimo_mes, periods=meses_necesarios, freq='MS')
            df_proyeccion = pd.DataFrame({
                "mes": fechas_extendidas.strftime("%B %Y")
            })
            
        # Asignamos los aportes limpios
        df_proyeccion["Persona_L_01_ahorro_soles"] = nuevo_ahorro_Persona_L_01
        df_proyeccion["Persona_J_02_ahorro_soles"] = nuevo_ahorro_Persona_J_02
        
        # El saldo neto mensual es 100% el ahorro conjunto (sin restar gastos)
        df_proyeccion["saldo_neto_mes"] = df_proyeccion["Persona_L_01_ahorro_soles"] + df_proyeccion["Persona_J_02_ahorro_soles"]
        df_proyeccion["saldo_acumulado_soles"] = df_proyeccion["saldo_neto_mes"].cumsum() + progreso_bolsa["ahorrado_soles"]
        df_proyeccion["progreso_pct"] = (df_proyeccion["saldo_acumulado_soles"] / meta_total) * 100
        
        df_proyeccion_display = df_proyeccion[[
            "mes", "Persona_L_01_ahorro_soles", "Persona_J_02_ahorro_soles", 
            "saldo_acumulado_soles", "progreso_pct"
        ]].copy()
        
        df_proyeccion_display.columns = [
            "Mes", "Persona_L_01 Ahorro", "Persona_J_02 Ahorro", "Saldo Acumulado", "Progreso %"
        ]
        
        df_proyeccion_display["Progreso %"] = df_proyeccion_display["Progreso %"].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(df_proyeccion_display, use_container_width=True)
        
# ===== PÁGINA: TRÁMITES Y MAPEO =====
elif pagina == "📋 Trámites y Mapeo":
    st.header("📋 Seguimiento, Mapeo y Trazabilidad")
    st.write("El estado de cada trámite se actualiza automáticamente según los gastos reales registrados en **Ahorro & Gastos** en comparación con el **Presupuesto**.")

    # Función auxiliar para determinar el estado automático basado en el gasto registrado vs esperado
    def calcular_estado_tramite(gasto_registrado, costo_esperado):
        if costo_esperado <= 0:
            return "Pendiente"
        elif gasto_registrado >= costo_esperado:
            return "Completado"
        elif gasto_registrado > 0:
            return "En proceso"
        else:
            return "Pendiente"

    # Nota: Asegúrate de reemplazar 'st.session_state.gastos_registrados' con la variable 
    # o estructura exacta que uses en tu página de Ahorro & Gastos para sumar los gastos por concepto.
    # Si guardas los gastos en una lista, puedes sumar por nombre de trámite.
    
    # 💱 Trámites en Soles
    if "presupuesto_soles_detallado" in st.session_state and st.session_state.presupuesto_soles_detallado:
        st.subheader("💱 Trazabilidad en Soles (Ahorro/Gastos vs Presupuesto)")
        
        for idx, grupo in enumerate(st.session_state.presupuesto_soles_detallado):
            nombre_tramite = grupo.get("tramite_principal", "Trámite sin nombre")
            costo_esperado = grupo.get("costo_total_base", 0.0)
            
            # Simulamos o leemos el gasto real acumulado en Ahorro & Gastos para este concepto.
            # (Aquí puedes conectar la variable o diccionario donde Ahorro & Gastos guarda los gastos por trámite)
            # Ejemplo: buscando en un registro de gastos de session_state
            gasto_en_ahorro = sum(
                item.get("monto", 0) for item in st.session_state.get("lista_gastos_soles", []) 
                if item.get("concepto") == nombre_tramite
            )
            # O si prefieres una alternativa directa por si el usuario edita un acumulador:
            # gasto_en_ahorro = grupo.get("gasto_registrado_actual", 0.0) 

            # Cálculo automático del estado
            estado_calculado = calcular_estado_tramite(gasto_en_ahorro, costo_esperado)
            grupo["estado"] = estado_calculado  # Actualizamos el estado de manera unificada

            # Renderizado visual en columnas
            col_t1, col_t2, col_t3, col_t4 = st.columns([2.5, 1.5, 1.5, 1.5])
            with col_t1:
                st.markdown(f"**{nombre_tramite}**")
                for sub in grupo.get("desglose", []):
                    if sub.get("cantidad", 0) > 0:
                        st.caption(f"  - {sub.get('subitem', '')} (S/ {sub.get('costo_unitario', 0):,.2f} c/u)")
            with col_t2:
                st.text(f"Presupuesto:\nS/ {costo_esperado:,.2f}")
            with col_t3:
                st.text(f"Gastado (Ahorro):\nS/ {gasto_en_ahorro:,.2f}")
            with col_t4:
                # Mostrar el estado con un color o indicador visual según corresponda
                if estado_calculado == "Completado":
                    st.success(f"🟢 {estado_calculado}")
                elif estado_calculado == "En proceso":
                    st.warning(f"🟡 {estado_calculado}")
                else:
                    st.info(f"⚪ {estado_calculado}")
            st.markdown("---")
    else:
        st.info("💡 Visita primero la sección de **Presupuesto** para inicializar los datos.")

    # 🍁 Trámites en CAD
    if "presupuesto_cad_detallado" in st.session_state and st.session_state.presupuesto_cad_detallado:
        st.subheader("🍁 Trazabilidad en CAD$ (Ahorro/Gastos vs Presupuesto)")
        
        for idx, grupo in enumerate(st.session_state.presupuesto_cad_detallado):
            nombre_tramite = grupo.get("tramite_principal", "Trámite sin nombre")
            costo_esperado_cad = grupo.get("costo_total_base", 0.0)
            
            # Gasto acumulado en CAD desde Ahorro & Gastos
            gasto_en_ahorro_cad = sum(
                item.get("monto", 0) for item in st.session_state.get("lista_gastos_cad", []) 
                if item.get("concepto") == nombre_tramite
            )

            estado_calculado_cad = calcular_estado_tramite(gasto_en_ahorro_cad, costo_esperado_cad)
            grupo["estado"] = estado_calculado_cad

            col_c1, col_c2, col_c3, col_c4 = st.columns([2.5, 1.5, 1.5, 1.5])
            with col_c1:
                st.markdown(f"**{nombre_tramite}**")
                for sub in grupo.get("desglose", []):
                    if sub.get("cantidad", 0) > 0:
                        st.caption(f"  - {sub.get('subitem', '')} (CAD $ {sub.get('costo_unitario', 0):,.2f} c/u)")
            with col_c2:
                st.text(f"Presupuesto:\nCAD $ {costo_esperado_cad:,.2f}")
            with col_c3:
                st.text(f"Gastado (Ahorro):\nCAD $ {gasto_en_ahorro_cad:,.2f}")
            with col_c4:
                if estado_calculado_cad == "Completado":
                    st.success(f"🟢 {estado_calculado_cad}")
                elif estado_calculado_cad == "En proceso":
                    st.warning(f"🟡 {estado_calculado_cad}")
                else:
                    st.info(f"⚪ {estado_calculado_cad}")
            st.markdown("---")
        
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
