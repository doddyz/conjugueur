# Distinction entre verbes avec ou sans tables conj active/pronomiale

# characteres en trop dans les tables des formes composees de l'indicatif (passe compose, plus que parfait etc ...  j’eus j’eus \n\ndû \n\n\ʒ‿y dy\ ...)
# Recuperer tables pour chaque mode
# Recuperer sous tables pour chaque temps dans chaque mode
# Recuperer lignes pour (pronoms) et formes conjuguées

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_CONJUGATE_URL = 'https://fr.wiktionary.org/wiki/Conjugaison:fran%C3%A7ais/'

# May need to url safe encode verb if contains accents, test this !!
def get_page_soup(verb):
    r = requests.get(BASE_CONJUGATE_URL + verb)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

# def get_page_elts(verb):
#     page = get_page(verb)
#     soup = BeautifulSoup(page, 'html.parser')
    
    # get_page_mode_tables(verb)
    # get_page_tense_tables(verb, mode)
    # get_page_tense_forms(verb, mode)
    

def get_page_mode_tables(verb):
    soup = get_page_soup(verb)
    all_tables = soup.find_all('table', class_=is_none_css)
    return_dict = {}
    return_dict['modes'] = all_tables[0]
    return_dict['verbe_du_n_groupe'] = all_tables[1]
    return_dict['modes_impersonnels'] = all_tables[2]
    return_dict['indicatif'] = all_tables[3]
    return_dict['subjonctif'] = all_tables[4]
    return_dict['conditionnel'] = all_tables[5]
    return_dict['imperatif'] = all_tables[6]

    return return_dict

def get_mode_tense_sub_tables(verb, mode):
    if (mode == 'indicatif'):
        mode_table = get_page_mode_tables(verb)['indicatif']
        # print(mode_table)
    sub_tables = mode_table.find_all('table')

    # print(sub_tables)
    
    sub_tables_dict = {
        'present': sub_tables[0],
        'passe_compose': sub_tables[1],
        'imparfait': sub_tables[2],
        'plus_que_parfait': sub_tables[3],
        'passe_simple': sub_tables[4],
        'passe_anterieur': sub_tables[5],
        'futur': sub_tables[6],
        'futur_anterieur': sub_tables[7],
        }

    return sub_tables_dict


def df_from_mode_tense_sub_table(verb, mode, tense, is_compound_tense):
    mode_tense_sub_tables = get_mode_tense_sub_tables(verb, mode)
    mode_tense_sub_table = mode_tense_sub_tables[tense]
    mode_tense_sub_table_header = mode_tense_sub_table.find('th').text.replace('\n', '')

    mode_tense_sub_table_trs = mode_tense_sub_table.find_all('tr')
    mode_tense_sub_table_tds = mode_tense_sub_table.find_all('td')

    if not is_compound_tense:
        
        pronoums = [td.text.replace('\xa0', '') for i,td in enumerate(mode_tense_sub_table_tds) if i % 4 == 0]
        
        verb_forms = [td.text for i,td in enumerate(mode_tense_sub_table_tds) if i % 4 == 1]

        pronoums_and_verb_forms = [elt[0] + ' ' + elt[1] for elt in list(zip(pronoums, verb_forms))]

    else:
        pronoums_and_auxiliary = [td.text.replace('\n', '') for i,td in enumerate(mode_tense_sub_table_tds) if i % 3 == 0]

        participles = [td.text.replace('\n', '') for i,td in enumerate(mode_tense_sub_table_tds) if i % 3 == 1]

        pronoums_and_verb_forms = [elt[0].strip() + ' ' + elt[1] for elt in list(zip(pronoums_and_auxiliary, participles))]

    return pd.DataFrame({mode_tense_sub_table_header: pronoums_and_verb_forms})
        
    # print(test, pronoums, verb_forms)
    
    # Get verb forms 
    
    
    # Works only for non compound tenses like present, imparfait, passe simple
    # pronoums_tds = mode_tense_sub_table.find_all(align='right')
    # pronoums = [pronoums_tds[i].text.strip() for i,_ in enumerate(pronoums_tds) if i % 2 == 0]
    # verb_forms_tds = mode_tense_sub_table.find_all(align='left')
    # verb_forms = [verb_forms_tds[i].text.strip() for i,_ in enumerate(verb_forms_tds) if i % 2 == 0]
    # pronoums_and_verb_forms = [elt[0] + ' ' + elt[1] for elt in list(zip(pronoums, verb_forms))]

    # return pd.DataFrame({mode_tense_sub_table_header: pronoums_and_verb_forms})
    
# To check whether an element has a set class
def is_none_css(css_class):
    return css_class is None


    
# Play
df_from_mode_tense_sub_table('aimer', 'indicatif', 'present')
# df_from_mode_tense_sub_table('aimer', 'indicatif', 'passe_compose')
    

    





