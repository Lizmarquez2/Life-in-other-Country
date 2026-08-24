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
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.subheader("👩‍💼 Persona_L_01")
        info_Persona_L_01 = calcular_por_persona(datos, "Persona_L_01")
        st.metric("Ahorrado", formato_moneda_soles(info_Persona_L_01["total_ahorrado_soles"]))
        st.metric("Gastado", formato_moneda_soles(info_Persona_L_01["total_gastado_soles"]))
        st.metric("Saldo", formato_moneda_soles(info_Persona_L_01["saldo_soles"]))
    
    with col_a2:
        st.subheader("👨‍💻 Persona_J_02")
        info_Persona_J_02 = calcular_por_persona(datos, "Persona_J_02")
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

    st.subheader("➕ Registrar Nuevo Aporte")
    with st.form("form_nuevo_aporte", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            persona_aporte = st.selectbox("¿Quién aporta?", ["Persona_L_01", "Persona_J_02"])
            monto_aporte = st.number_input("Monto en Soles (S/)", min_value=0.0, step=10.0, format="%.2f")
        with col_f2:
            fecha_aporte = st.date_input("Fecha del aporte")
            concepto_aporte = st.text_input("Concepto / Descripción", placeholder="Ej. Ahorro de sueldo mensual")
        
        submit_aporte = st.form_submit_button("Guardar Aporte")
        
        if submit_aporte:
            # Estructura del nuevo registro
            nuevo_registro = {
                "fecha": str(fecha_aporte),
                "persona": persona_aporte,
                "monto_soles": monto_aporte,
                "concepto": concepto_aporte
            }
            
            # Asegurarnos de que exista la llave de movimientos en tus datos
            if "movimientos" not in datos:
                datos["movimientos"] = []
                
            # Agregar a la lista de datos en memoria
            datos["movimientos"].append(nuevo_registro)
            
            # Guardar en el archivo JSON correspondiente (ej. movimientos.json)
            try:
                guardar_datos_json("movimientos.json", {"movimientos": datos["movimientos"]})
                st.success(f"¡Aporte de S/ {monto_aporte:.2f} registrado con éxito para {persona_aporte}!")
                st.rerun() # Recarga la app para mostrar los cambios actualizados
            except Exception as e:
                st.error(f"Error al guardar el archivo: {e}")

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
        nuevo_ahorro_liz = st.number_input("Aporte mensual Persona_L_01 (S/)", value=700.0, step=50.0)
    with col_s2:
        nuevo_ahorro_jhon = st.number_input("Aporte mensual Persona_J_02 (S/)", value=250.0, step=50.0)
        
    aporte_mensual_total = nuevo_ahorro_liz + nuevo_ahorro_jhon
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
        df_proyeccion["Persona_L_01_ahorro_soles"] = nuevo_ahorro_liz
        df_proyeccion["Persona_J_02_ahorro_soles"] = nuevo_ahorro_jhon
        
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
        
# ===== PÁGINA 5: TRAMITES Y MAPEO =====
elif pagina == "📋 Trámites y Mapeo":
    st.header("📋 Seguimiento de Trámites Migratorios")
    st.write("Gestiona el estado de tus documentos y requisitos para Canadá.")
    
    lista_tramites = datos.get("tramites", {}).get("tramites", [])
    
    if lista_tramites:
        for i, t in enumerate(lista_tramites):
            col_t1, col_t2 = st.columns([3, 1])
            with col_t1:
                st.write(f"**{t.get('nombre', '')}**")
            with col_t2:
                estado_actual = t.get('estado', 'Pendiente')
                opciones = ["Pendiente", "En Proceso", "Completado"]
                indice = opciones.index(estado_actual) if estado_actual in opciones else 0
                
                nuevo_estado = st.selectbox("Estado", opciones, index=indice, key=f"tramite_{i}")
                
                if nuevo_estado != estado_actual:
                    lista_tramites[i]["estado"] = nuevo_estado
                    guardar_datos_json("tramites.json", {"tramites": lista_tramites})
                    st.success("¡Estado actualizado!")
                    st.rerun()
    else:
        st.info("No hay trámites registrados en el archivo `tramites.json`.")

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
