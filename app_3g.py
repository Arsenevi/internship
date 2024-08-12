import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Analyse de Disponibilité 3G")

# Fonction pour traiter le fichier Excel
def process_file(uploaded_file):
    # Lire le fichier Excel
    sheets_dict = pd.read_excel(uploaded_file, sheet_name=None, engine='pyxlsb')
    
    # Accéder aux feuilles spécifiques
    df_availability = sheets_dict['availability']
    df_3G_Voice = sheets_dict['voice']
    df_3G_data = sheets_dict['trafficgb']
    df_3G_speech_drop = sheets_dict['speech drop']

    # Fonction pour nettoyer les DataFrames
    def clean_dataframe(df):
        # Afficher les noms des colonnes avant nettoyage
        st.write("Noms des colonnes avant nettoyage :")
        st.write(df.columns.tolist())

        # Remplacer les en-têtes problématiques par des noms valides
        replacements = {'#NAME?': 'Invalid_Name', '#N/A': 'Invalid_Name'}
        for old, new in replacements.items():
            df.columns = df.columns.str.replace(old, new, regex=False)

        # Renommer les colonnes de dates
        date_columns = df.columns[2:14]  # Ajustez l'index selon votre DataFrame
        date_columns = [f'Date_{i}' for i in range(1, len(date_columns) + 1)]
        df.columns.values[2:14] = date_columns

        # Suppression des colonnes dupliquées
        df = df.loc[:, ~df.columns.duplicated()]

        # Afficher les noms des colonnes après nettoyage
        st.write("Noms des colonnes après nettoyage :")
        st.write(df.columns.tolist())

        return df

    # Nettoyer les DataFrames
    df_availability = clean_dataframe(df_availability)
    df_3G_Voice = clean_dataframe(df_3G_Voice)
    df_3G_data = clean_dataframe(df_3G_data)
    df_3G_speech_drop = clean_dataframe(df_3G_speech_drop)

    # Définir les colonnes à vérifier pour les valeurs nulles
    columns_to_check = ['Date_1', 'Date_2', 'Date_3', 'Date_4', 'Date_5', 
                        'Date_6', 'Date_7', 'Date_8', 'Date_9', 'Date_10', 
                        'Date_11', 'Date_12']

    # Filtrer les lignes où au moins une des colonnes spécifiées est nulle ou égale à 0
    df_availability_filtered = df_availability[df_availability[columns_to_check].isnull().any(axis=1)]
    df_3G_Voice_filtered = df_3G_Voice[df_3G_Voice[columns_to_check].isnull().any(axis=1)]
    df_3G_data_filtered = df_3G_data[df_3G_data[columns_to_check].isnull().any(axis=1)]
    df_3G_speech_drop_filtered = df_3G_speech_drop[df_3G_speech_drop[columns_to_check].isnull().any(axis=1)]

    # Filtrer les lignes où au moins une des colonnes spécifiées est égale à 0
    df_availability_zero = df_availability[(df_availability[columns_to_check] == 0).any(axis=1)]
    df_3G_Voice_zero = df_3G_Voice[(df_3G_Voice[columns_to_check] == 0).any(axis=1)]
    df_3G_data_zero = df_3G_data[(df_3G_data[columns_to_check] == 0).any(axis=1)]
    df_3G_speech_drop_zero = df_3G_speech_drop[(df_3G_speech_drop[columns_to_check] == 0).any(axis=1)]

    # Afficher les résultats filtrés
    st.subheader("DataFrame 'availability' avec des valeurs nulles :")
    st.dataframe(df_availability_filtered)

    st.subheader("DataFrame '3G_Voice' avec des valeurs nulles :")
    st.dataframe(df_3G_Voice_filtered)

    st.subheader("DataFrame '3G_data' avec des valeurs nulles :")
    st.dataframe(df_3G_data_filtered)

    st.subheader("DataFrame '3G_speech_drop' avec des valeurs nulles :")
    st.dataframe(df_3G_speech_drop_filtered)

    # Afficher les résultats de disponibilité nulle
    st.subheader("Disponibilité 3G nulle :")
    st.write("DataFrame 'availability' :")
    st.dataframe(df_availability_zero)

    st.write("DataFrame '3G_Voice' :")
    st.dataframe(df_3G_Voice_zero)

    st.write("DataFrame '3G_data' :")
    st.dataframe(df_3G_data_zero)

    st.write("DataFrame '3G_speech_drop' :")
    st.dataframe(df_3G_speech_drop_zero)

    # Enregistrer les résultats nuls au format CSV
    if not df_availability_zero.empty:
        csv_availability = df_availability_zero.to_csv(index=False)
        st.download_button(
            label="Télécharger les résultats de disponibilité 3G nulle",
            data=csv_availability,
            file_name='disponibilite_3G_nulle.csv',
            mime='text/csv'
        )

# Interface utilisateur pour télécharger le fichier
uploaded_file = st.file_uploader("Téléchargez votre fichier Excel", type=["xlsb"])

if uploaded_file is not None:
    process_file(uploaded_file)
