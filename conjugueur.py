# Simplifier df_from_mode_tense_sub_table pour que cela fonctionne avec autres modes

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_CONJUGATE_URL = 'https://fr.wiktionary.org/wiki/Conjugaison:fran%C3%A7ais/'

# TENSES = {'indicatif': {'simple': ['present', 'imparfait', 'plus_que_parfait', 'passe_simple', 'passe_anterieur', 'futur', 'futur_anterieur']} 'compound': ['passe_compose', ]}, 'subjonctif': {}}

# May need to url safe encode verb if contains accents, test this !!
def get_page_soup(verb):
    r = requests.get(BASE_CONJUGATE_URL + verb)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def get_page_mode_tables(verb):
    soup = get_page_soup(verb)
    all_tables = soup.find_all(border='0', width='100%')
    return_dict = {}
    # return_dict['verbe_du_n_groupe'] = all_tables[1]
    return_dict['modes_impersonnels'] = all_tables[0]
    return_dict['indicatif'] = all_tables[1]
    return_dict['subjonctif'] = all_tables[10]
    return_dict['conditionnel'] = all_tables[15]
    return_dict['imperatif'] = all_tables[18]

    return return_dict


def get_mode_tense_sub_tables(verb, mode):
    
    if (mode == 'indicatif'):
        
        mode_table = get_page_mode_tables(verb)['indicatif']

        sub_tables = mode_table.find_all('table')
        
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
        
    elif (mode == 'subjonctif'):
        
        mode_table = get_page_mode_tables(verb)['subjonctif']
        
        sub_tables = mode_table.find_all('table')
        
        sub_tables_dict = {
            'present': sub_tables[0],
            'passe': sub_tables[1],
            'imparfait': sub_tables[2],
            'plus_que_parfait': sub_tables[3],
        }

    elif (mode == 'conditionnel'):
        
        mode_table = get_page_mode_tables(verb)['conditionnel']

        # print(mode_table)
        
        sub_tables = mode_table.find_all('table')
        
        sub_tables_dict = {
            'present': sub_tables[0],
            'passe': sub_tables[1],
        }
        
    elif (mode == 'imperatif'):
        
        mode_table = get_page_mode_tables(verb)['imperatif']
        
        sub_tables = mode_table.find_all('table')
        
        sub_tables_dict = {
            'present': sub_tables[0],
            'passe': sub_tables[1],
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

    return pd.DataFrame({mode_tense_sub_table_header: pronoums_and_verb_forms}, index=None)


# Findall filter functions 
def has_width_attr(tag):
    return tag.has_attr('width')


def is_none_css(css_class):
    return css_class is None


    
# Play
# df_from_mode_tense_sub_table('aimer', 'indicatif', 'present')
# df_from_mode_tense_sub_table('aimer', 'indicatif', 'passe_compose')
    

    





