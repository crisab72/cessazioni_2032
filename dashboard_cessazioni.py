
import pandas as pd
import plotly.express as px
import streamlit as st

# Carica il file CSV locale
df = pd.read_csv("Anagrafica_cessazioni.csv", sep=';', encoding='ISO-8859-1')

# Pulizia dei nomi delle colonne
df.columns = df.columns.str.replace('"', '').str.strip()

# Conversione della colonna "60 Anni" in formato data
df['60 Anni'] = pd.to_datetime(df['60 Anni'], format='%d/%m/%Y', errors='coerce')

# Filtra le date valide fino al 2032
df = df[df['60 Anni'].notna() & (df['60 Anni'] <= '2032-12-31')]

# Titolo della dashboard
st.title("Dashboard Cessazioni per Struttura")

# Selezione della struttura
structure_options = sorted(df['Struttura'].dropna().unique())
selected_structure = st.selectbox("Seleziona la struttura", structure_options)

# Filtra i dati per la struttura selezionata
df_filtered = df[df['Struttura'] == selected_structure].copy()
df_filtered['Month'] = df_filtered['60 Anni'].dt.to_period('M').dt.to_timestamp()
cessations_by_month = df_filtered.groupby(['Month']).size().reset_index(name='Cessazioni')

# Crea il grafico interattivo
fig = px.line(
    cessations_by_month,
    x='Month',
    y='Cessazioni',
    markers=True,
    title=f'Cessazioni mensili per {selected_structure} fino al 2032',
    labels={'Month': 'Mese', 'Cessazioni': 'Numero di cessazioni'}
)
fig.update_traces(mode='lines+markers', hovertemplate='Mese: %{x}<br>Cessazioni: %{y}')

# Mostra il grafico
st.plotly_chart(fig)
