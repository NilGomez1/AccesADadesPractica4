import streamlit as st
import pandas as pd

st.title("Mi Primer Dashboard de Libros")


def cargar_datos(archivo):
    try:
        df = pd.read_csv(archivo, sep=';')
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return pd.DataFrame()


df = cargar_datos('libros.csv')

if not df.empty:

    st.header("Filtros en el Centro")

    min_precio = float(df['Precio'].min())
    max_precio = float(df['Precio'].max())

    rango_precio = st.slider(
        "Rango de Precio:",
        min_value=min_precio,
        max_value=max_precio,
        value=(min_precio, max_precio)
    )

    df_filtrado = df.copy()

    df_filtrado = df_filtrado[
        (df_filtrado['Precio'] >= rango_precio[0]) &
        (df_filtrado['Precio'] <= rango_precio[1])
        ]

    st.header("Resultados Filtrados")

    if not df_filtrado.empty:
        st.subheader("Tabla de Libros")
        st.dataframe(df_filtrado)

        st.subheader("Gráfico de Distribución de Libros por Rating")

        df_conteo_rating = df_filtrado['Rating_Clase'].value_counts().reset_index()
        df_conteo_rating.columns = ['Rating', 'Conteo']
        df_conteo_rating.set_index('Rating', inplace=True)

        st.bar_chart(df_conteo_rating)

    else:
        st.warning("No hay datos que coincidan con los filtros seleccionados.")