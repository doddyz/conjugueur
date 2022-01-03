# Il faudra regler l'alignement des largeurs de tables de modes distincts avec contraintes existantes sur les tables st.columns

from conjugueur import *
import streamlit as st

st.set_page_config('Conjugueur App', page_icon=':memo:', layout='wide', initial_sidebar_state='expanded')

st.title('Conjugueur Français')


# CSS used to hide dataframes indexes
hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

# This code will hide the dataframes indexes, see where to place it
st.markdown(hide_table_row_index, unsafe_allow_html=True)


# Sidebar widgets
verbe = st.sidebar.text_input('Tapez ici le verbe à conjuguer')

if verbe:
    
    st.markdown(f'### {verbe.title()}')

    st.write('#####')
    
    modes_container = st.container()

    with modes_container:

        st.markdown('###### Indicatif')  
        
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
        df_present = df_from_mode_tense_sub_table(verbe, 'indicatif', 'present', False)
        df_passe_compose = df_from_mode_tense_sub_table(verbe, 'indicatif', 'passe_compose', True)

        df_indicatif_1 = pd.concat([df_present, df_passe_compose], axis=1)
    
        df_imparfait = df_from_mode_tense_sub_table(verbe, 'indicatif', 'imparfait', False)
        df_plus_que_parfait = df_from_mode_tense_sub_table(verbe, 'indicatif', 'plus_que_parfait', True)
        df_indicatif_2 = pd.concat([df_imparfait, df_plus_que_parfait], axis=1)

        df_passe_simple = df_from_mode_tense_sub_table(verbe, 'indicatif', 'passe_simple', False)

        df_passe_anterieur = df_from_mode_tense_sub_table(verbe, 'indicatif', 'passe_anterieur', True)

        df_indicatif_3 = pd.concat([df_passe_simple, df_passe_anterieur], axis=1)
    
        df_futur = df_from_mode_tense_sub_table(verbe, 'indicatif', 'futur', False)

        df_futur_anterieur = df_from_mode_tense_sub_table(verbe, 'indicatif', 'futur_anterieur', True)

        df_indicatif_4 = pd.concat([df_futur, df_futur_anterieur], axis=1)

        with col1:
            st.table(df_indicatif_1)
        
        with col2:
            st.table(df_indicatif_2)

        with col3:
            st.table(df_indicatif_3)

        with col4:
            st.table(df_indicatif_4)

        st.markdown('###### Subjonctif') 
            
        col5, col6 = st.columns(2)
            
        df_present = df_from_mode_tense_sub_table(verbe, 'subjonctif', 'present', False)
        df_passe = df_from_mode_tense_sub_table(verbe, 'subjonctif', 'passe', True)

        df_subjonctif_1 = pd.concat([df_present, df_passe], axis=1)
        
        df_imparfait = df_from_mode_tense_sub_table(verbe, 'subjonctif', 'imparfait', False)
        df_plus_que_parfait = df_from_mode_tense_sub_table(verbe, 'subjonctif', 'plus_que_parfait', True)

        df_subjonctif_2 = pd.concat([df_imparfait, df_plus_que_parfait], axis=1)

        with col5:
            st.table(df_subjonctif_1)
        
        with col6:
            st.table(df_subjonctif_2)


        st.markdown('###### Conditionnel') 
            
        col7, col8 = st.columns(2)
            
        df_present = df_from_mode_tense_sub_table(verbe, 'conditionnel', 'present', False)
        df_passe = df_from_mode_tense_sub_table(verbe, 'conditionnel', 'passe', True)
        df_conditionnel_1 = pd.concat([df_present, df_passe], axis=1)

        with col7:
            st.table(df_conditionnel_1)
        

        st.markdown('###### Imperatif') 
            
        col9, col10 = st.columns(2)
            
        df_present = df_from_mode_tense_sub_table(verbe, 'imperatif', 'present', True)
        df_passe = df_from_mode_tense_sub_table(verbe, 'imperatif', 'passe', True)
        
        df_imperatif_1 = pd.concat([df_present, df_passe], axis=1)

        with col9:
            st.table(df_imperatif_1)



