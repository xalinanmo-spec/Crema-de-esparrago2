import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Crema de Espárrago", page_icon="🥫", layout="wide")

st.title("🥫 Balance de Masa - Crema de Espárrago")

def calcular(F, Mcorte, Mselec, Mpulpeo, CMC, GMS, NaCl, AC):
    despues_corte = F - Mcorte
    despues_seleccion = despues_corte - Mselec
    pulpa = despues_seleccion - Mpulpeo
    
    if pulpa < 0:
        return None
    
    total = (CMC + GMS + NaCl + AC) / 100
    aditivos = pulpa * total
    final = pulpa + aditivos
    
    return {
        'final': final,
        'pulpa': pulpa,
        'aditivos': aditivos,
        'despues_corte': despues_corte,
        'despues_seleccion': despues_seleccion,
        'rendimiento': (final/F)*100,
        'mermas': Mcorte + Mselec + Mpulpeo
    }

with st.sidebar:
    st.header("⚙️ Parámetros")
    F = st.slider("🌿 Espárrago fresco (kg)", 0.0, 5.0, 2.5, 0.1)
    Mcorte = st.slider("Corte (kg)", 0.0, 2.0, 0.3, 0.05)
    Mselec = st.slider("Selección (kg)", 0.0, 1.0, 0.2, 0.05)
    Mpulpeo = st.slider("Pulpeado (kg)", 0.0, 2.0, 0.4, 0.05)
    CMC = st.slider("CMC (%)", 0.0, 1.0, 0.2, 0.05)
    GMS = st.slider("GMS (%)", 0.0, 2.0, 0.8, 0.05)
    NaCl = st.slider("NaCl (%)", 0.0, 5.0, 1.5, 0.1)
    AC = st.slider("Ác. cítrico (%)", 0.0, 1.0, 0.1, 0.05)

if st.button("🔍 CALCULAR"):
    r = calcular(F, Mcorte, Mselec, Mpulpeo, CMC, GMS, NaCl, AC)
    if r:
        c1, c2, c3 = st.columns(3)
        c1.metric("🥫 Salsa final", f"{r['final']:.3f} kg")
        c2.metric("📊 Rendimiento", f"{r['rendimiento']:.1f}%")
        c3.metric("📉 Mermas", f"{r['mermas']:.3f} kg")
        
        fig, ax = plt.subplots()
        etapas = ['Fresco', 'Corte', 'Selección', 'Pulpa', 'Salsa']
        valores = [F, r['despues_corte'], r['despues_seleccion'], r['pulpa'], r['final']]
        colores = ['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336']
        ax.bar(etapas, valores, color=colores)
        for i, v in enumerate(valores):
            ax.text(i, v + 0.05, f'{v:.2f}', ha='center')
        st.pyplot(fig)
    else:
        st.error("ERROR: Las mermas son muy grandes")