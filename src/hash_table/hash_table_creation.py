import os
import os
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.utils import helper
from src.find_ocurrences.find_ocurrences import find_ocurrences
from collections import Counter, defaultdict, OrderedDict

LEN_HASH_TABLE = 130000
HASH_TABLE = [[] for _ in range(LEN_HASH_TABLE)]

def create_dictionary_hash_table(filepaths, log_file, output_dir, tokenized_items_dir):
    general_start_time = time.time()
    helper.format_msg_str(' Ejecutando: ACT 8. CREANDO DICCIONARIO CON HASH TABLE ')
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
            final_string = f'\nTiempo total de ejecucion (encontrar ocurrencias): {(end_time - start_time)}\n'
            start_time = time.time()
            print(final_string)
            log_obj.write(final_string)

            # All tokens
            all_tokens_list = [j for i in all_tokens for j in i.keys()]

            # Populating hash table with ocurrences
            populate_ocurrences_hashtable(ocurrences_counter, all_tokens_list, HASH_TABLE)

            # Generating posting file
            tokenized_files = helper.get_all_files(tokenized_items_dir, '.html')
            dictionary_keys = list(OrderedDict.fromkeys(all_tokens_list))
            posting_file_name = os.path.join(output_dir, 'posting_hash_table.txt')
            generate_posting_file(posting_file_name, tokenized_files, all_tokens, dictionary_keys, HASH_TABLE)

            # Generating final dictionary with posting index
            output_dict_name = os.path.join(output_dir, 'dictionary_hash_table.txt')
            write_hash_table_dict(output_dict_name, HASH_TABLE)
            end_time = time.time()
            final_string = f'\nTiempo total que tomo generar el diccionario y posting file usando hash table: {end_time - general_start_time}\n'
            print(final_string)
            log_obj.write(final_string)
    except OSError as error:
        print(f'No se pudo abrir el archivo: {error}')
        helper.exit_program(1)


def populate_ocurrences_hashtable(ocurrences_counter, dictionary_keys, hash_table):
    first_time = time.time()
    ocurrences_dict = dict(ocurrences_counter)
    print('--> Generando diccionario de ocurrencias')
    # Temporal dictionary to get number of files with ocurrences
    temp_dict = defaultdict(int)
    for key in dictionary_keys:
        temp_dict[key] += 1

    # Starting to populate hash table with key and
    for key, value in temp_dict.items():
        helper.insert_hash_table(hash_table, key, [ocurrences_dict[key], value])
    end_time = time.time()
    print(f'\nTiempo final de ejecucion: {end_time - first_time}')


def generate_posting_file(posting_file_name, tokenized_files, all_tokens, token_keys, hash_table):
    start_time = time.time()
    print('\n--> Creando posting file')
    posting_index = 0
    with open(posting_file_name, 'w', encoding='utf-8') as posting_obj:
        for key in token_keys:
            helper.insert_hash_table(hash_table, key, posting_index)
            indexes = [all_tokens.index(dictionary) for dictionary in all_tokens if key in dictionary]
            files = [tokenized_files[index] for index in indexes]
            for char in range(0, len(files)):
                posting_obj.write(f'{os.path.basename(files[char])}|{all_tokens[indexes[char]][key]}\n')
                posting_index += 1
    final_time = time.time()
    final_time = final_time - start_time
    print(f'\nTiempo de ejecucion: {final_time}')


def write_hash_table_dict(output_dict_name, hash_table):
    start_time = time.time()
    print('\n--> Escribiendo valores en archivo diccionario')
    print('\nToken| No. de Archivos con token| Index en posting file\n')
    with open(output_dict_name, 'w', encoding='utf-8') as output_obj:
        for element in hash_table:
            if len(element) == 0:
                continue
            for obj in element:
                token = obj[0]
                values = obj[1]
                output_obj.write(f'{token : >35}   {values[1] : >06}  {values[2] : >06}\n')
        # for token in token_keys:
        #     values = helper.search_hash_table(hash_table, token)
        #     output_obj.write(f'{token : >35}   {values[1] : >06}  {values[2] : >06}\n')
    end_time = time.time()
    print(f'Tiempo de ejecucion: {end_time - start_time}')
