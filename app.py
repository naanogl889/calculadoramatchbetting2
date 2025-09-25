# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 19:25:12 2025

@author: 34608
"""

import streamlit as st
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

from calculadoramatchbetting import (
    calcular_dinero_real,
    calcular_freebet,
    calcular_reembolso,
    calcular_rollover
)

st.set_page_config(page_title="Calculadora Match Betting", layout="centered")
st.title("💸 Calculadora de Match Betting")

# Menú de selección del tipo de apuesta
st.markdown("## 🎯 Selecciona el tipo de apuesta")
tipo_apuesta = st.selectbox("📌 Tipo de apuesta:", [
    "Dinero Real", "Freebet", "Reembolso", "Rollover"
])

st.markdown("### 💸 Parámetros generales")

# Agrupamos inputs en columnas para una presentación más ordenada
col1, col2 = st.columns(2)
with col1:
    importe = st.number_input("💰 Importe apostado (€)", min_value=1.0, value=10.0, step=1.0)
    cuota_en_contra = st.number_input("📉 Cuota en Betfair Exchange (En contra)", min_value=1.01, value=1.6, step=0.01)
   
with col2:
    cuota_a_favor = st.number_input("📈 Cuota en casa de apuestas (A favor)", min_value=1.01, value=1.55, step=0.01)
    comision = st.number_input("🏦 Comisión del Exchange (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1) / 100

# Mostrar parámetros adicionales según el tipo de apuesta
if tipo_apuesta == "Reembolso":
    with st.expander("⚙️ Parámetros específicos para apuesta con Reembolso"):
        col1, col2 = st.columns(2)
        with col1:
            retencion = st.slider("🔁 Retención esperada del valor de la freebet (%)", 0.0, 1.0, 0.7, step=0.05)
        with col2:
            reembolso = st.number_input("💵 Monto reembolsado si pierdes (€)", min_value=0.0, value=importe, step=1.0)

elif tipo_apuesta == "Rollover":
    with st.expander("⚙️ Parámetros específicos para apuesta con Rollover"):
        col1, col2 = st.columns(2)
        with col1:
            bono = st.number_input("🎁 Importe del bono (€)", min_value=1.0, value=importe, step=1.0)
            rollover = st.number_input("🔄 Rollover total requerido (€)", min_value=1.0, value=600.0, step=10.0)
        with col2:
            porcentaje_retencion = st.slider("🧲 Retención estimada tras completar rollover (%)", 0.0, 1.0, 0.95, step=0.01)

# Botón para calcular
st.markdown("---")
st.markdown("## 🚀 Pulsa para calcular tu apuesta óptima")

if st.button("🔍 Calcular"):
    if tipo_apuesta == "Dinero Real":
        resultado = calcular_dinero_real(importe, cuota_a_favor, cuota_en_contra, comision)
    elif tipo_apuesta == "Freebet":
        resultado = calcular_freebet(importe, cuota_a_favor, cuota_en_contra, comision)
    elif tipo_apuesta == "Reembolso":
        resultado = calcular_reembolso(importe, cuota_a_favor, cuota_en_contra, comision, reembolso, retencion)
    elif tipo_apuesta == "Rollover":
        resultado = calcular_rollover(importe, cuota_a_favor, cuota_en_contra, comision, bono, rollover, porcentaje_retencion)
    else:
        st.error("❌ Tipo de apuesta no reconocido.")
        st.stop()


    
    
   # Mostrar resultados visualmente mejorados
    st.subheader("📊 ¿Cuánto debes apostar en cada casa de apuestas?")
    
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    
    with col1:
        st.markdown("""
        <div style='background-color: #dbeafe; padding: 20px; border-radius: 15px; text-align: center;'>
            <h4 style='margin-bottom: 10px;'>A Favor</h4>
            <p style='font-size: 18px;'><strong>{:.2f}€</strong> a cuota <strong>{}</strong></p>
        </div>
        """.format(resultado['importe'], resultado['cuota_a_favor']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #fff7ed; padding: 20px; border-radius: 15px; text-align: center; border: 3px solid orange;'>
            <h4 style='margin-bottom: 10px;'>Ganancia Estimada</h4>
            <p style='font-size: 20px;'><strong>{:.2f}€</strong></p>
            <p style='color: #555;'>Rating {:.2f}%</p>
        </div>
        """.format(resultado['ganancia_casa'], resultado['porcentaje_valor']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #fee2e2; padding: 20px; border-radius: 15px; text-align: center;'>
            <h4 style='margin-bottom: 10px;'>En Contra</h4>
            <p style='font-size: 18px;'><strong>{:.2f}€</strong> a cuota <strong>{}</strong></p>
            <p style='color: #444;'>Riesgo: {:.2f}€</p>
        </div>
        """.format(resultado['lay'], cuota_en_contra, resultado['riesgo']), unsafe_allow_html=True)
    
    # Clasificación textual aparte
    st.markdown(f"<p style='text-align: center; font-size: 18px; margin-top: 20px;'>📊 <strong>Clasificación:</strong> {resultado['clasificacion']}</p>", unsafe_allow_html=True)
    
    st.markdown("---")

    # Mostrar tabla de resultados
    # Casa de apuestas
    if tipo_apuesta == "Freebet":
        casa_gana = resultado['importe'] * (resultado['cuota_a_favor'] - 1)
        casa_pierde = 0.0
    elif tipo_apuesta == "Reembolso":
        casa_gana = resultado['importe'] * (resultado['cuota_a_favor'] - 1)
        valor_reembolso = reembolso * retencion
        casa_pierde = -resultado['importe'] + valor_reembolso
    elif tipo_apuesta == "Rollover":
        casa_gana = resultado['ganancia_casa_real']  # incluye lo ganado + riesgo
        casa_pierde = -resultado['importe_real']            # lo que pierdes si gana el exchange

    else:  # Dinero Real
        casa_gana = resultado['importe'] * (resultado['cuota_a_favor'] - 1)
        casa_pierde = -resultado['importe']
    
    # Exchange (igual en todos)
    exchange_gana = -resultado['riesgo']
    exchange_pierde = resultado['lay'] * (1 - resultado['comision'])
    
    # Totales
    total_gana = casa_gana + exchange_gana
    total_pierde = casa_pierde + exchange_pierde

    st.markdown("### 📊 ¿Que pasa si ganas o pierdes la apuesta?")
    import pandas as pd
    import streamlit as st
    
    # Crear DataFrame
    data = {
        "Resultado de la apuesta": ["✅ Si ganas en la casa", "❌ Si pierdes en la casa"],
        "Casa de apuestas": [casa_gana, casa_pierde],
        "Exchange": [exchange_gana, exchange_pierde],
        "Total": [total_gana, total_pierde]
    }
    
    df = pd.DataFrame(data)
    
    # Mostrar tabla con formato visual mejorado
    def formato_monedas(val):
        return f"{val:.2f} €"
    
    # Aplicar estilos condicionales
    def resaltar_ganancias(val):
        color = "green" if val >= 0 else "red"
        return f"color: {color}; font-weight: bold"
    
    
    st.dataframe(
        df.style.format(formato_monedas, subset=["Casa de apuestas", "Exchange", "Total"])
                 .applymap(resaltar_ganancias, subset=["Casa de apuestas", "Exchange", "Total"])
                 .set_properties(**{'text-align': 'center'})
                 .set_table_styles([
                     {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'center'), ('background-color', '#f0f2f6')]},
                     {'selector': 'td', 'props': [('padding', '10px')]}
                 ])
    )
