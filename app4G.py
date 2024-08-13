import streamlit as st
import pandas as pd
import numpy as np

# Fonction pour traiter le fichier
def process_file(uploaded_file):
    sheets_dict = pd.read_excel(uploaded_file, sheet_name=None, engine='pyxlsb')
    
    # Accéder à la feuille spécifique
    df_availability_4G = sheets_dict['availability_auto']
    df_4G_data = sheets_dict['volume']

    # Utiliser str.replace sur les colonnes des DataFrames
    df_availability_4G.columns = df_availability_4G.columns.str.replace(r'#NAME\?', 'Invalid_Name', regex=True)
    df_availability_4G.columns = df_availability_4G.columns.str.replace(r'#N/A', 'Invalid_Name', regex=True)

    df_4G_data.columns = df_4G_data.columns.str.replace(r'#NAME\?', 'Invalid_Name', regex=True)
    df_4G_data.columns = df_4G_data.columns.str.replace(r'#N/A', 'Invalid_Name', regex=True)

    # Renommer les colonnes de dates pour chaque DataFrame
    date_columns_availability = df_availability_4G.columns[2:16]
    date_columns_availability = [f'Date_{i}' for i in range(1, len(date_columns_availability) + 1)]
    df_availability_4G.columns.values[2:16] = date_columns_availability

    date_columns_4G_data = df_4G_data.columns[2:16]
    date_columns_4G_data = [f'Date_{i}' for i in range(1, len(date_columns_4G_data) + 1)]
    df_4G_data.columns.values[2:16] = date_columns_4G_data

    # Définir les colonnes à vérifier pour les valeurs nulles
    columns_to_check = ['Date_1', 'Date_2', 'Date_3', 'Date_4', 'Date_5', 
                        'Date_6', 'Date_7', 'Date_8', 'Date_9', 'Date_10', 
                        'Date_11', 'Date_12','Date_13','Date_14']
    
    # Filtrer les DataFrames pour les lignes où au moins une des colonnes à vérifier a une valeur de 0
    df_availability_filtered = df_availability_4G[(df_availability_4G[columns_to_check] == 0).any(axis=1)]
    df_4G_data_filtered = df_4G_data[(df_4G_data[columns_to_check] == 0).any(axis=1)]

    return df_availability_filtered, df_4G_data_filtered

# Interface Streamlit
st.title('Uploader un fichier .xlsb')
uploaded_file = st.file_uploader('Choisissez un fichier .xlsb', type=['xlsb'])

if uploaded_file is not None:
    df_availability_filtered, df_4G_data_filtered = process_file(uploaded_file)
    
    # Afficher la taille des DataFrames
    st.write('Taille du DataFrame df_availability_filtered:', df_availability_filtered.shape)
    st.write('Taille du DataFrame df_4G_data_filtered:', df_4G_data_filtered.shape)

    # Afficher les DataFrames filtrés
    st.subheader('df_availability_filtered')
    st.dataframe(df_availability_filtered)

    st.subheader('df_4G_data_filtered')
    st.dataframe(df_4G_data_filtered)

    # Télécharger les DataFrames filtrés
    availability_csv = df_availability_filtered.to_csv(index=False).encode('utf-8')
    data_csv = df_4G_data_filtered.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Télécharger df_availability_filtered",
        data=availability_csv,
        file_name='df_availability_filtered.csv',
        mime='text/csv'
    )

    st.download_button(
        label="Télécharger df_4G_data_filtered",
        data=data_csv,
        file_name='df_4G_data_filtered.csv',
        mime='text/csv'
    )