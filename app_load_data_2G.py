import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Analyse des données 2G")

# Permettre à l'utilisateur d'uploader le fichier
uploaded_file = st.file_uploader("Choisissez un fichier XLSB", type=['xlsb'])

if uploaded_file is not None:
    # Charger le fichier Excel
    sheets_dict = pd.read_excel(uploaded_file, sheet_name=None, engine='pyxlsb')

    # Accéder aux feuilles spécifiques
    df_availability_2G = sheets_dict['2G_CELL_DISPONIBILITY']
    df_trafic_2G = sheets_dict['2G_TRAFFIC_ERLANG']

    # Remplacer les en-têtes problématiques par des noms valides
    replacements = {'#NAME?': 'Invalid_Name', '#N/A': 'Invalid_Name'}
    df_availability_2G.columns = df_availability_2G.columns.str.replace(r'#NAME\?', 'Invalid_Name', regex=True)
    df_availability_2G.columns = df_availability_2G.columns.str.replace(r'#N/A', 'Invalid_Name', regex=True)
    df_trafic_2G.columns = df_trafic_2G.columns.str.replace(r'#NAME\?', 'Invalid_Name', regex=True)
    df_trafic_2G.columns = df_trafic_2G.columns.str.replace(r'#N/A', 'Invalid_Name', regex=True)

    # Renommer les colonnes de dates
    date_columns_availability = df_availability_2G.columns[2:14]
    date_columns_availability = [f'Date_{i}' for i in range(1, len(date_columns_availability) + 1)]
    df_availability_2G.columns.values[2:14] = date_columns_availability

    date_columns_2G_Voice = df_trafic_2G.columns[2:14]
    date_columns_2G_Voice = [f'Date_{i}' for i in range(1, len(date_columns_2G_Voice) + 1)]
    df_trafic_2G.columns.values[2:14] = date_columns_2G_Voice

    # Suppression des colonnes dupliquées
    df_trafic_2G = df_trafic_2G.loc[:, ~df_trafic_2G.columns.duplicated()]
    df_availability_2G = df_availability_2G.loc[:, ~df_availability_2G.columns.duplicated()]

    # Définir les colonnes à vérifier pour les valeurs nulles
    columns_to_check = ['Date_1', 'Date_2', 'Date_3', 'Date_4', 'Date_5', 
                        'Date_6', 'Date_7', 'Date_8', 'Date_9', 'Date_10', 
                        'Date_11', 'Date_12']

    # Filtrer les DataFrames
    df_availability_filtered = df_availability_2G[(df_availability_2G[columns_to_check] == 0).any(axis=1)]
    df_trafic_2G_filtered = df_trafic_2G[(df_trafic_2G[columns_to_check] == 0).any(axis=1)]

    # Afficher les DataFrames filtrés
    st.subheader("Données de disponibilité filtrées")
    st.write(df_availability_filtered)

    st.subheader("Données de trafic filtrées")
    st.write(df_trafic_2G_filtered)

    # Bouton de téléchargement pour df_availability_filtered
    csv_availability = df_availability_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger les données de disponibilité (CSV)",
        data=csv_availability,
        file_name='availability_filtered_2G.csv',
        mime='text/csv'
    )

    # Bouton de téléchargement pour df_trafic_2G_filtered
    csv_trafic = df_trafic_2G_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger les données de trafic (CSV)",
        data=csv_trafic,
        file_name='trafic_filtered_2G.csv',
        mime='text/csv'
    )
