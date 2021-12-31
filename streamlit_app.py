from conjugueur import *
import streamlit as st

st.set_page_config('Conjugueur App', page_icon=':memo:', layout='centered', initial_sidebar_state='expanded')

st.title('Conjugueur App')

# Sidebar widgets
verbe = st.sidebar.text_input('Tapez ici le verbe à conjuguer')

if verbe:
    col1, col2 = st.columns(2)
    with col1:
        st.write(df_from_mode_tense_sub_table(verbe, 'indicatif', 'present', False))
    with col2:
        st.write(df_from_mode_tense_sub_table(verbe, 'indicatif', 'passe_compose', True))
        




