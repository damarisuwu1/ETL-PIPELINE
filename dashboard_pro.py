import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# --- 1. CARGA DE DATOS ---
file_path = "output_data/mental_health_final.parquet"
if not os.path.exists(file_path): 
    print("⚠️ Faltan datos. Corre el DAG 'mental_health_etl_matrix' en Airflow.")
    exit()
df = pd.read_parquet(file_path)

# Conversiones a texto
cols = ['age_group', 'sector', 'risk_category', 'destress_method', 'stress_source', 'gender']
# Verificamos si existe la columna género (por si usas un ETL viejo)
if 'gender' not in df.columns:
    df['gender'] = "Desconocido"
df[cols] = df[cols].astype(str)

# --- 2. PREPARACIÓN DE DATOS ---

# A. Radar (Sector)
radar_data = df.groupby('sector')['stress_level'].mean().reset_index()

# B. Área (Edad)
age_order = ['Gen Z (20-29)', 'Millennials (30-39)', 'Gen X (40-49)', 'Boomers (50+)']
df['age_group'] = pd.Categorical(df['age_group'], categories=age_order, ordered=True)
area_data = df.groupby('age_group')['stress_level'].mean().reset_index()

# C. MATRIZ DE VULNERABILIDAD (HEATMAP) - VA A LA IZQUIERDA
matrix_data = df.groupby(['age_group', 'gender'])['stress_level'].mean().reset_index()
matrix_pivot = matrix_data.pivot(index='age_group', columns='gender', values='stress_level')

# D. EMBUDO (FUNNEL) - VA A LA DERECHA
funnel_data = df.groupby('destress_method')['stress_level'].mean().sort_values(ascending=False).reset_index()

# E. KPIs
risk_dist = df['risk_category'].value_counts().reset_index()
risk_dist.columns = ['category', 'count']
avg_stress = df['stress_level'].mean()

# --- 3. COLORES NEÓN ---
BG_COLOR = "#000000"
PAPER_COLOR = "#121212"
TEXT_COLOR = "#ffffff"
NEON_CYAN = "#00f3ff"
NEON_MAGENTA = "#d500f9" 
NEON_LIME = "#00e676"
NEON_AMBER = "#ff9100"
# Colores manuales para el embudo para que resalte
funnel_colors = ['#ff0055', '#ff9100', '#f2ff00', '#00f3ff', '#00e676'] 

# --- 4. LAYOUT ---
fig = make_subplots(
    rows=3, cols=2,
    specs=[
        [{"type": "indicator"}, {"type": "domain"}],
        [{"type": "polar"}, {"type": "xy"}],
        [{"type": "xy"}, {"type": "funnel"}] # <--- XY (Matriz) | Funnel (Embudo)
    ],
    subplot_titles=(
        "", "<b>Distribución de Riesgo</b>", 
        "<b>Perfil General por Sector</b>", "<b>Tendencia por Edad</b>",
        "<b>Matriz de Vulnerabilidad (Edad vs Género)</b>", "<b>Efectividad de Desestrés</b>"
    ),
    vertical_spacing=0.12, horizontal_spacing=0.1, row_heights=[0.2, 0.4, 0.4]
)

# --- FILA 1 ---
fig.add_trace(go.Indicator(
    mode="number+delta", value=avg_stress,
    delta={'reference': 5, 'increasing': {'color': NEON_MAGENTA}, 'decreasing': {'color': NEON_LIME}},
    number={'suffix': "/10", 'font': {'size': 50, 'color': NEON_CYAN}},
    title={"text": "ESTRÉS PROMEDIO"}
), row=1, col=1)

colors_risk_pie = {'Alto Riesgo': NEON_MAGENTA, 'Riesgo Moderado': NEON_AMBER, 'Bajo Riesgo': NEON_LIME}
fig.add_trace(go.Pie(
    labels=risk_dist['category'], values=risk_dist['count'], hole=0.6,
    marker=dict(colors=[colors_risk_pie.get(k) for k in risk_dist['category']], line=dict(color='#000000', width=2)),
    textinfo='label+percent'
), row=1, col=2)

# --- FILA 2 ---
fig.add_trace(go.Scatterpolar(
    r=radar_data['stress_level'], theta=radar_data['sector'], fill='toself',
    line=dict(color=NEON_MAGENTA), marker=dict(color=NEON_CYAN), name="General Sector"
), row=2, col=1)

fig.add_trace(go.Scatter(
    x=area_data['age_group'], y=area_data['stress_level'], fill='tozeroy',
    mode='lines+markers', line=dict(color=NEON_CYAN, width=3),
    marker=dict(size=8, color='#ffffff'), name="Edad"
), row=2, col=2)

# --- FILA 3 (LA COMBINACIÓN PERFECTA) ---

# 1. MATRIZ DE VULNERABILIDAD (Izquierda)
fig.add_trace(go.Heatmap(
    z=matrix_pivot.values,
    x=matrix_pivot.columns, 
    y=matrix_pivot.index,   
    colorscale='Hot_r',     
    colorbar=dict(title="Estrés", x=-0.1), # Barra a la izquierda
    hovertemplate='Edad: %{y}<br>Género: %{x}<br>Estrés: %{z:.2f}<extra></extra>'
), row=3, col=1)

# 2. EMBUDO DE DESESTRÉS (Derecha) - Con colores manuales vibrantes
fig.add_trace(go.Funnel(
    y=funnel_data['destress_method'], 
    x=funnel_data['stress_level'],
    marker=dict(color=funnel_colors, line=dict(width=0)),
    textinfo="label+value",
    textposition="inside",
    name="Efectividad"
), row=3, col=2)

# --- ESTÉTICA FINAL ---
fig.update_layout(
    template="plotly_dark", paper_bgcolor=BG_COLOR, plot_bgcolor=PAPER_COLOR,
    font=dict(family="Arial", color=TEXT_COLOR),
    title={'text': "<b>DASHBOARD DE BIENESTAR: ANÁLISIS COMPLETO</b>", 'y': 0.96, 'x': 0.5, 'xanchor': 'center'},
    height=1100, showlegend=False, 
    margin=dict(t=100, l=50, r=50, b=50),
    polar=dict(bgcolor=PAPER_COLOR, radialaxis=dict(visible=True, range=[0, 10], gridcolor='#333'), angularaxis=dict(gridcolor='#333'))
)
fig.update_yaxes(showgrid=True, gridcolor='#333333')

output_file = "dashboard_final_v16_mix.html"
fig.write_html(output_file)
print(f"🔥 DASHBOARD FINAL LISTO: {output_file}")