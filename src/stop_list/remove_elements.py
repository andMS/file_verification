import os
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
import src.hash_table.hash_table_creation as hash_table
from src.utils import helper
from src.find_ocurrences.find_ocurrences import find_ocurrences
from collections import Counter, defaultdict, OrderedDict

LEN_HASH_TABLE = 130000
HASH_TABLE = [[] for _ in range(LEN_HASH_TABLE)]

def execute_stop_list(stop_list_path, filepaths, log_file, output_dir, tokenized_items_dir):
    general_start_time = time.time()
    helper.format_msg_str(' Ejecutando: ACT 9. CREAR DICCIONARIO OMITIENDO ELEMENTOS DE STOP LIST ')
    excluded_words = get_words_to_remove(stop_list_path)
    all_tokens = []
    try:
        with open(log_file, 'w', encoding='utf-8') as log_obj:
            start_time = time.time()
            ocurrences_counter = Counter()
            log_counter = 0
            msg_str = '--> Obteniendo tokens de todos los archivos\n'
            log_obj.write(msg_str)
            print(msg_str)
            # Start by gathering all tokens from each file
            for file in filepaths:
                file_time = time.time()
                log_counter += 1
                tokenized_alph = os.path.join(tokenized_items_dir, f'tokenized_all_{os.path.basename(file.replace("letters_sorted_clean_",""))}')
                all_tokens.append(find_ocurrences(file, tokenized_alph, False))
                end_time = time.time()
                log_obj.write(f'{log_counter : >03}. {os.path.relpath(file) : <100}{end_time - file_time}\n')
            # Updating python counter with number of ocurrences of all files
            for element in all_tokens:
                ocurrences_counter.update(element)
            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion (obtener tokens): {(end_time - start_time)}\n'
            print(final_string)
            log_obj.write(final_string)

            # All tokens
            print('--> Removiendo tokens de stop list\n')
            all_tokens_list = [j for i in all_tokens for j in i.keys() if j not in excluded_words]

            # Populating hash table with ocurrences
            hash_table.populate_ocurrences_hashtable(ocurrences_counter, all_tokens_list, HASH_TABLE)

            # Generating posting file
            tokenized_files = helper.get_all_files(tokenized_items_dir, '.html')
            dictionary_keys = list(OrderedDict.fromkeys(all_tokens_list))
            posting_file_name = os.path.join(output_dir, 'posting_stop_list.txt')
            hash_table.generate_posting_file(posting_file_name, tokenized_files, all_tokens, dictionary_keys, HASH_TABLE)

            # Removing elements from hashtable
            start_time = time.time()
            print(f'\n--> Removiendo elementos de hash table:\n' +
                    'Criterios:\n  - Palabras de un solo caracter.\n  - Frecuencia menor a 5')
            final_tokens = remove_elements_from_hashtable(1, helper.MINIMAL_OCURRENCES, dictionary_keys, HASH_TABLE)
            temp_end_time = time.time()
            msg_str = f'\nTiempo total (remover elementos segun criterio): {temp_end_time - start_time}\n'
            print(msg_str)
            log_obj.write(msg_str)
            # Generating final dictionary with posting index omitting elements from stop list
            output_dict_name = os.path.join(output_dir, 'dictionary_stop_list.txt')
            hash_table.write_hash_table_dict(output_dict_name, final_tokens, HASH_TABLE)
            end_time = time.time()
            final_string = f'\nTiempo total que tomo generar el diccionario y posting file (hash table, removiendo elementos): {end_time - general_start_time}\n'
            print(final_string)
            log_obj.write(final_string)
    except OSError as error:
        print(f'No se pudo abrir el archivo: {error}')
        helper.exit_program(1)


def remove_elements_from_hashtable(length, frequency, keys, hash_table):
    final_tokens = []
    for key in keys:
        if len(key) <= length:
            helper.delete_from_hash_table(hash_table, key)
            continue
        values = helper.search_hash_table(hash_table, key)
        if int(values[0]) < frequency:
            helper.delete_from_hash_table(hash_table, key)
            continue
        final_tokens.append(key)

    return final_tokens


def get_words_to_remove(stop_list_path):

    final_list = []
    with open(stop_list_path, 'r', encoding='utf-8') as file_obj:
        lines = file_obj.readlines()
        for line in lines:
            line = line.replace('\n', '')
            if 'Stop List' in line or '\x0c' in line:
                continue
            if len(line) != 0 and not line.isdigit():
                final_list.append(line)
    return final_list
