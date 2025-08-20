# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# ==============================================================================
# CONFIGURACIÓN DE LA PÁGINA Y ESTILOS
# ==============================================================================
st.set_page_config(page_title="Calculadora Match Betting", layout="centered")

# Inyectamos la fuente 'Inter' para que coincida con tu web
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
       font-family: 'Inter', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# FUNCIONES DE CÁLCULO (Lógica de la calculadora)
# ==============================================================================

def calcular_dinero_real(importe, cuota_a_favor, cuota_exchange, comision):
    mejor_lay = 0
    mejor_diferencia = float('inf')
    mejor_ganancia_casa = 0
    mejor_ganancia_exchange = 0

    for lay in [x / 100 for x in range(1, int(importe * 200) + 1)]:
        ganancia_casa = importe * (cuota_a_favor - 1) - lay * (cuota_exchange - 1)
        ganancia_exchange = lay * (1 - comision) - importe
        diferencia = abs(ganancia_casa - ganancia_exchange)

        if diferencia < mejor_diferencia:
            mejor_diferencia = diferencia
            mejor_lay = lay
            mejor_ganancia_casa = ganancia_casa
            mejor_ganancia_exchange = ganancia_exchange

    riesgo = mejor_lay * (cuota_exchange - 1)
    beneficio_promedio = (mejor_ganancia_casa + mejor_ganancia_exchange) / 2
    porcentaje_valor = 100 + (beneficio_promedio / importe) * 100

    if porcentaje_valor >= 98:
        clasificacion = "🟢 Excelente"
    elif porcentaje_valor >= 95:
        clasificacion = "🟢 Muy Bueno"
    elif porcentaje_valor >= 90:
        clasificacion = "🟠 Regular (Busca cuotas mas bajas y mas parejas)"
    else:
        clasificacion = "🔴 Malo (Busca cuotas mas bajas y mas parejas)"

    return {
        "tipo": "real", "importe": importe, "cuota_a_favor": cuota_a_favor,
        "cuota_exchange": cuota_exchange, "comision": comision, "lay": mejor_lay,
        "riesgo": riesgo, "ganancia_casa": mejor_ganancia_casa,
        "ganancia_exchange": mejor_ganancia_exchange, "diferencia": mejor_diferencia,
        "porcentaje_valor": porcentaje_valor, "clasificacion": clasificacion
    }

def calcular_freebet(importe, cuota_a_favor, cuota_exchange, comision):
    mejor_lay = 0
    mejor_diferencia = float('inf')
    mejor_ganancia_casa = 0
    mejor_ganancia_exchange = 0

    for lay in [x / 100 for x in range(1, int(importe * 200) + 1)]:
        ganancia_casa = (cuota_a_favor - 1) * importe - lay * (cuota_exchange - 1)
        ganancia_exchange = lay * (1 - comision)
        diferencia = abs(ganancia_casa - ganancia_exchange)

        if diferencia < mejor_diferencia:
            mejor_diferencia = diferencia
            mejor_lay = lay
            mejor_ganancia_casa = ganancia_casa
            mejor_ganancia_exchange = ganancia_exchange

    riesgo = mejor_lay * (cuota_exchange - 1)
    beneficio_promedio = (mejor_ganancia_casa + mejor_ganancia_exchange) / 2
    porcentaje_valor = (beneficio_promedio / importe) * 100

    if porcentaje_valor >= 75:
        clasificacion = "🟢 Excelente"
    elif porcentaje_valor >= 70:
        clasificacion = "🟢 Muy Bueno"
    elif porcentaje_valor >= 65:
        clasificacion = "🟠 Regular (Busca cuotas mas altas y mas parejas)"
    else:
        clasificacion = "🔴 Malo (Busca cuotas mas altas y mas parejas)"

    return {
        "tipo": "freebet", "importe": importe, "cuota_a_favor": cuota_a_favor,
        "cuota_exchange": cuota_exchange, "comision": comision, "lay": mejor_lay,
        "riesgo": riesgo, "ganancia_casa": mejor_ganancia_casa,
        "ganancia_exchange": mejor_ganancia_exchange, "diferencia": mejor_diferencia,
        "porcentaje_valor": porcentaje_valor, "clasificacion": clasificacion
    }

# ... (Las otras funciones de cálculo como `calcular_reembolso` y `calcular_rollover` irían aquí si las necesitas)
# Por simplicidad, las he omitido, pero puedes pegarlas aquí si quieres que la calculadora las tenga.


# ==============================================================================
# INTERFAZ DE USUARIO (UI) DE STREAMLIT
# ==============================================================================

st.title("💸 Calculadora de Match Betting")

st.markdown("## 🎯 Selecciona el tipo de apuesta")
tipo_apuesta = st.selectbox("📌 Tipo de apuesta:", ["Dinero Real", "Freebet"]) # He simplificado a 2 por ahora

st.markdown("### 💸 Parámetros generales")

col1, col2 = st.columns(2)
with col1:
    importe = st.number_input("💰 Importe apostado (€)", min_value=1.0, value=10.0, step=1.0)
    cuota_en_contra = st.number_input("📉 Cuota en Betfair Exchange (En contra)", min_value=1.01, value=1.6, step=0.01)
    
with col2:
    cuota_a_favor = st.number_input("📈 Cuota en casa de apuestas (A favor)", min_value=1.01, value=1.55, step=0.01)
    comision = st.number_input("🏦 Comisión del Exchange (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1) / 100

st.markdown("---")

if st.button("🔍 Calcular apuesta óptima"):
    if tipo_apuesta == "Dinero Real":
        resultado = calcular_dinero_real(importe, cuota_a_favor, cuota_en_contra, comision)
    elif tipo_apuesta == "Freebet":
        resultado = calcular_freebet(importe, cuota_a_favor, cuota_en_contra, comision)
    else:
        st.error("❌ Tipo de apuesta no reconocido.")
        st.stop()

    # --- Mostrar resultados visualmente ---
    st.subheader("📊 ¿Cuánto debes apostar?")
    
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    
    with col1:
        st.markdown(f"""
        <div style='background-color: #dbeafe; padding: 20px; border-radius: 15px; text-align: center; height: 100%;'>
            <h4 style='margin-bottom: 10px;'>A Favor (Back)</h4>
            <p style='font-size: 18px;'><strong>{resultado['importe']:.2f}€</strong> a cuota <strong>{resultado['cuota_a_favor']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        beneficio = (resultado['ganancia_casa'] + resultado['ganancia_exchange']) / 2
        st.markdown(f"""
        <div style='background-color: #fff7ed; padding: 20px; border-radius: 15px; text-align: center; border: 3px solid #f97316; height: 100%;'>
            <h4 style='margin-bottom: 10px;'>Beneficio</h4>
            <p style='font-size: 20px; color: #16a34a;'><strong>{beneficio:.2f}€</strong></p>
            <p style='color: #555;'>Rating: {resultado['porcentaje_valor']:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background-color: #fee2e2; padding: 20px; border-radius: 15px; text-align: center; height: 100%;'>
            <h4 style='margin-bottom: 10px;'>En Contra (Lay)</h4>
            <p style='font-size: 18px;'><strong>{resultado['lay']:.2f}€</strong> a cuota <strong>{cuota_en_contra}</strong></p>
            <p style='color: #444;'>Riesgo: {resultado['riesgo']:.2f}€</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"<p style='text-align: center; font-size: 18px; margin-top: 20px;'><strong>Clasificación:</strong> {resultado['clasificacion']}</p>", unsafe_allow_html=True)
