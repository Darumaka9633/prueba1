import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard de Satisfacción", layout="wide")

# ======================
# 1. TÍTULO
# ======================
st.title("📊 Dashboard Interactivo de Satisfacción UNALM")
st.write("Este dashboard permite subir un archivo Excel y generar automáticamente las visualizaciones.")

# ======================
# 2. SUBIDA DE ARCHIVO
# ======================
uploaded_file = st.file_uploader("Sube tu archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:

    # ======================
    # 3. LECTURA DEL EXCEL
    # ======================
    df_respuestas = pd.read_excel(uploaded_file)

    st.subheader("📄 Vista previa de la data")
    st.write(df_respuestas.head())

    # ---------------------------
    # Diccionario de variables
    # ---------------------------
    diccionario_data = {
        'Variable': ['V1','V2','V3','V4','V5','V6','V7','V8','V9','V10',
                     'V11','V12','V13','V14','V15','V16','V17'],
        'Consulta': [
            'Apertura de aulas', 'Aire acondicionado', 'Cortinas',
            'Calefacción', 'Equipos', 'Horario baños', 'Limpieza',
            'Ambiente', 'Iluminación', 'Trato personal', 'Mobiliario',
            'Ruido', 'Ventilación', 'Ambientes modernos', 'Clases',
            'Internet', 'Sistema eléctrico'
        ]
    }

    df_diccionario = pd.DataFrame(diccionario_data)
    variable_labels = df_diccionario.set_index('Variable')['Consulta'].to_dict()

    df_data = df_respuestas.drop(columns=['Nro'])

    # ======================
    # 4. GRAFICO 1: BARRAS PROMEDIO
    # ======================
    st.subheader("📌 Promedio de Satisfacción por Servicio")

    satisfaction_mean = df_data.mean().sort_values(ascending=False)
    mean_df = pd.DataFrame(satisfaction_mean, columns=['Promedio']).reset_index()
    mean_df['Servicio'] = mean_df['index'].map(variable_labels)

    fig1, ax1 = plt.subplots(figsize=(10,7))
    sns.barplot(data=mean_df, x="Promedio", y="Servicio", ax=ax1)
    ax1.set_title("Promedio por Servicio")
    plt.axvline(3, color="red", linestyle="--")
    st.pyplot(fig1)

    # ======================
    # 5. GRAFICO 2: DISTRIBUCIONES
    # ======================
    st.subheader("📌 Distribución detallada de respuestas")

    df_melted = df_data.melt(var_name='Variable', value_name='Nivel')
    df_melted['Servicio'] = df_melted['Variable'].map(variable_labels)

    fig2 = sns.catplot(
        data=df_melted, x="Nivel", col="Servicio", kind="count",
        col_wrap=3, height=4, aspect=1.4
    )
    st.pyplot(fig2)

    # ======================
    # 6. GRAFICO 3: BOXPLOT
    # ======================
    st.subheader("📌 Distribución (Boxplot)")

    df_labeled = df_data.rename(columns=variable_labels)
    order = df_labeled.median().sort_values(ascending=False).index

    fig3, ax3 = plt.subplots(figsize=(11,7))
    sns.boxplot(data=df_labeled, orient='h', order=order, ax=ax3)
    st.pyplot(fig3)

    # ======================
    # 7. GRAFICO 4: CORRELACION
    # ======================
    st.subheader("📌 Matriz de correlación")

    correlation = df_data.corr()
    correlation.columns = [variable_labels[c] for c in correlation.columns]
    correlation.index = [variable_labels[i] for i in correlation.index]

    fig4, ax4 = plt.subplots(figsize=(12,10))
    sns.heatmap(correlation, annot=True, cmap="Blues", ax=ax4)
    st.pyplot(fig4)

    # ======================
    # 8. GRAFICO 5: VIOLIN PLOT
    # ======================
    st.subheader("📌 Gráfico de Violín")

    fig5, ax5 = plt.subplots(figsize=(11,8))
    sns.violinplot(data=df_melted, y='Servicio', x='Nivel', ax=ax5)
    st.pyplot(fig5)

else:
    st.info("👆 Sube un archivo Excel para continuar.")

