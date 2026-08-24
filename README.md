# 🚀 Dashboard de Migración Calgary 2026-2027

Dashboard interactivo para planificar y monitorear la migración de **Persona_L_01 Esthefanny Márquez Panuera + Persona_J_02** a Calgary, Alberta, Canadá.

## 📋 Descripción

Este dashboard permite:
- ✅ Registrar ahorros mensuales
- ✅ Monitorear gastos en trámites
- ✅ Proyectar fechas de viaje
- ✅ Controlar progreso hacia la meta de bolsa migratoria (S/ 60,000)
- ✅ Ver línea de tiempo de trámites separada por persona
- ✅ Análisis de presupuesto en múltiples monedas

## 🛠️ Stack Tecnológico

- **Python 3.8+**
- **Streamlit** - Framework para dashboards interactivos
- **Pandas** - Manipulación de datos
- **Plotly** - Visualizaciones interactivas
- **JSON** - Base de datos

## 📁 Estructura del Proyecto

```
Life-in-other-Country/
├── app.py                      # Main Streamlit app
├── config.py                   # Configuración global
├── requirements.txt            # Dependencias Python
├── .gitignore                  # Archivos a ignorar en Git
├── README.md                   # Este archivo
│
├── data/                       # BASE DE DATOS (JSON)
│   ├── config.json            # Tasas, fechas, metas
│   ├── tramites.json          # Catálogo de trámites
│   ├── cronograma.json        # Timeline por hito
│   ├── movimientos.json       # Ahorro/Gastos
│   ├── presupuesto.json       # Presupuesto detallado
│   └── bolsa_migracion.json   # Objetivo de bolsa
│
├── modules/                    # LÓGICA PYTHON
│   ├── __init__.py
│   ├── data_loader.py         # Carga datos JSON
│   ├── calculadora.py         # Cálculos automáticos
│   ├── conversiones.py        # S/ ↔ CAD$ conversiones
│   └── validators.py          # (Para futuras validaciones)
│
└── views/                      # VISTAS STREAMLIT
    ├── __init__.py
    └── (En futuras versiones: componentes reutilizables)
```

## 🚀 Instalación Local

### Requisitos
- Git
- Python 3.8+
- pip

### Pasos

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Persona_L_01marquez2/Life-in-other-Country.git
   cd Life-in-other-Country
   ```

2. **Crear entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el dashboard:**
   ```bash
   streamlit run app.py
   ```

5. **Abrir en navegador:**
   - La app se abrirá en `http://localhost:8501`

## 📝 Uso

### Estructura de Datos

#### 📌 Monedas
- **S/ (Soles):** Para gastos en Perú (pasaportes, vuelos, etc.)
- **CAD$:** Para gastos en Canadá (ECA, IELTS, Express Entry, etc.)

#### 📊 Tabs del Dashboard

1. **Resumen Ejecutivo**
   - KPIs principales
   - Gráficos de progreso
   - Próximos pasos

2. **Línea de Tiempo**
   - Timeline separada para Persona_L_01 y Persona_J_02
   - Fechas de trámites
   - Costos asociados

3. **Ahorro & Gastos**
   - Registro de movimientos por persona
   - Tabla interactiva de ahorro/gasto
   - Saldos acumulados

4. **Presupuesto**
   - Desglose por categoría
   - Gastos en S/ y CAD$
   - Presupuesto vs Gastado

5. **Bolsa Migratoria**
   - Progreso hacia meta (S/ 60,000)
   - Proyección mensual
   - Fechas de alcance de meta

6. **Configuración**
   - Información del proyecto
   - Tasas de cambio
   - Metas financieras

## 🔄 Editar Datos

Todos los datos se almacenan en archivos **JSON en la carpeta `data/`**.

Para agregar un movimiento, edita `data/movimientos.json`:

```json
{
  "id": 5,
  "fecha": "2026-08-20",
  "persona": "Persona_L_01",
  "tipo": "AHORRO",
  "concepto": "Sueldo septiembre",
  "monto_original": 2500,
  "moneda_original": "PEN",
  "fuente": "Clínica Adventista",
  "actividad": "Depósito",
  "observaciones": "Ahorro mes 2"
}
```

**Luego:** Git push y el dashboard se actualizará automáticamente en Streamlit Cloud.

## 🌐 Deployment en Streamlit Cloud

### Pasos (Una sola vez)

1. **Push a GitHub:**
   ```bash
   git add .
   git commit -m "Initial Calgary migration dashboard"
   git push origin main
   ```

2. **Ir a Streamlit Cloud:**
   - Acceder a https://share.streamlit.io

3. **Crear nueva app:**
   - Click en "New app"
   - Repository: `Persona_L_01marquez2/Life-in-other-Country`
   - Branch: `main`
   - File path: `app.py`
   - Click "Deploy"

4. **Configurar privacidad (opcional):**
   - Settings → Sharing → Private (requiere GitHub login)

5. **Tu app estará en:**
   ```
   https://[username]-life-in-other-country.streamlit.app/
   ```

### Auto-deploy
Streamlit Cloud auto-actualiza cada vez que hagas push a `main` (en ~2 minutos).

## 📊 Ejemplo de Workflow

1. **Registrar ahorro mensual:**
   - Edita `data/movimientos.json`
   - Agrega entrada: `{ "fecha": "2026-09-05", "persona": "Persona_L_01", "tipo": "AHORRO", ...}`

2. **Registrar gasto en trámite:**
   - Edita `data/movimientos.json`
   - Agrega entrada: `{ "fecha": "2026-08-20", "persona": "Persona_L_01", "tipo": "GASTO", ...}`

3. **Push a GitHub:**
   ```bash
   git add data/movimientos.json
   git commit -m "Registro de ahorros agosto"
   git push origin main
   ```

4. **Dashboard se actualiza automáticamente en ~2 minutos** ✅

## 💡 Características Principales

### ✅ Cálculos Automáticos
- Conversión automática S/ ↔ CAD$
- Saldos acumulados por persona
- Proyección de fechas según ahorro real
- Progreso hacia meta

### ✅ Datos Reales
- Todos los costos reales en S/ y CAD$
- Tasas de cambio actualizables
- Línea de tiempo detallada
- Información de ambas personas

### ✅ Monedas Correctas
- **Perú:** Gastos en soles (S/)
- **Canadá:** Gastos en dólares (CAD$)
- Conversiones automáticas en dashboard

## 🔐 Privacidad

El repositorio es **PRIVADO**. Solo Persona_L_01, Persona_J_02 y colaboradores autorizados tienen acceso.

Para agregar colaboradores:
1. GitHub → Settings → Collaborators
2. Agregar emails autorizados

## 🐛 Troubleshooting

### "Módulo no encontrado"
```bash
# Verifica que estés en el directorio correcto
cd Life-in-other-Country
# Reinstala dependencias
pip install -r requirements.txt
```

### Dashboard no se actualiza
```bash
# Limpia cache Streamlit
streamlit cache clear
# O reinicia el servidor
```

### Error en Streamlit Cloud
- Check logs: Settings → Deploy logs
- Verifica que `requirements.txt` esté actualizado
- Verifica que archivos JSON estén en `data/` folder

## 📧 Contacto

**Creado para:** Persona_L_01 Esthefanny Márquez Panuera + Persona_J_02  
**Email:** esthef356@gmail.com  
**GitHub:** https://github.com/Persona_L_01marquez2/Life-in-other-Country

## 📝 Notas Importantes

### Monedas
- **SIEMPRE** usa S/ para Perú
- **SIEMPRE** usa CAD$ para Canadá
- El dashboard convierte automáticamente

### Proyecciones
- La bolsa migratoria es dinámica
- Si ahorros se atrasan, fecha de viaje se ajusta
- Si ahorras más rápido, fecha se adelanta

### Actualizaciones
- Edita JSON directamente
- No necesitas recompilar
- Dashboard se actualiza en ~2 minutos en Streamlit Cloud

## ✅ Versión Actual

- **v1.0.0** - Agosto 2026
- Datos iniciales precargados
- 6 tabs principales funcionales
- Conversión de monedas automática

## 🚀 Roadmap Futuro

- [ ] Agregar vista de documentos PDF
- [ ] Integración con Google Drive
- [ ] Notificaciones por email
- [ ] Exportar reportes a Excel
- [ ] Modo oscuro

---

**¡Que tengan un gran viaje a Calgary en Junio 2027!** 🇨🇦✈️
