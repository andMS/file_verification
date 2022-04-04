import os
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.utils import helper
from src.find_ocurrences.find_ocurrences import find_ocurrences
from collections import Counter, defaultdict


def execute_create_dict_posting_file(filepaths: list, output_file: str, token_output_dir: str, output_dir:str):
    general = []
    ocurrences_dict = {}
    helper.format_msg_str(' Ejecutando: ACT 7. CREANDO DICCIONARIO Y POSTING FILE ')
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            first_time = time.time()
            counter = Counter()
            log_counter = 0
            msg_str = '--> Prueba: encontrar numero de ocurrencias en todos los archivos\n'
            output_obj.write(msg_str)
            print(msg_str)
            for file in filepaths:
                log_counter += 1
                start_time = time.time()
                tokenized_alph = os.path.join(token_output_dir, f'tokenized_all_{os.path.basename(file.replace("letters_sorted_clean_",""))}')
                # General is list of dictionary of tokens of a file with all ocurrences within file
                general.append(find_ocurrences(file, tokenized_alph, False))
                end_time = time.time()
                output_obj.write(f'{log_counter : >03}. {os.path.relpath(file) : <100}{end_time - start_time}\n')
            # Updating python counter with num of ocurrences of all files
            # For every dictionary in general list, we use counter to update its values
            # So we get all ocurrences in all files
            for element in general:
                counter.update(element)

            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion (encontrar ocurrencias): {(end_time - first_time)}\n'

            start_time = time.time()
            print(final_string)
            output_obj.write(final_string)

            # Generating all files ocurrences dictionary
            ocurrences_dict = generate_ocurrences_dict(general, counter)

            # Generating posting file
            file_paths = helper.get_all_files(token_output_dir, '.html')
            ocurrences_dict = generate_posting_file(ocurrences_dict, output_dir, file_paths, general)

            # Writing ocurrences dict with position in posting file
            output_dict_name = os.path.join(output_dir, 'dictionary.txt')
            write_dictionary_with_posting_file(output_dict_name, ocurrences_dict)
            end_time = time.time()
            end_time = end_time - start_time

            final_string = f'\nTiempo que tomo generar el diccionario y posting file: {end_time}\n'
            print(final_string)
            output_obj.write(final_string)

    except OSError:
        print(f'No se pudo escribir en archivo de logs: {output_file}')
        helper.exit_program(1)


def generate_ocurrences_dict(file_ocurrences, general_counter):
    # File ocurrences is a list of dictionaries that contains all tokens and ocurrences per file
    # General counter is the counter that has the number of ocurrences of all tokens in all files
    ocurrences = dict(general_counter)
    first_time = time.time()
    print('--> Generando diccionario de occurencias en todos los archivos.\n')
    # the value of data is all keys from the list of dictionaries of ocurrences
    data = [j for i in file_ocurrences for j in i.keys()]
    temp_dict = defaultdict(int)

    # We populate the temp_dict to get the number of files that contain that word
    # For every key in data, we create a key in temp_dict
    # A dictionary cannot have duplicated keys, so every time a key is repeated, the value will add 1 to the sum
    # This is how we obtain the number of files, by checking the number of dictionaries that had this key
    for key in data:
        temp_dict[key] += 1

    final_dict = {}
    for key, value in temp_dict.items():
        final_dict[key] = [ocurrences[key], value]
    end_time = time.time()
    final_time = end_time - first_time
    print(f'Tiempo de ejecucion: {final_time}')

    return final_dict


def write_dictionary_with_posting_file(output_file, dictionary):
    print('\n--> Escribiendo diccionario con index en posting file')
    print('\nToken|No. de Archivos con token|Index en posting file\n')
    start_time = time.time()
    with open(output_file, 'w', encoding='utf-8') as output_obj:
        for key, value in dictionary.items():
            output_obj.write(f'{key}|{value[1]}|{value[2]}\n')
    end_time = time.time()
    end_time = end_time - start_time
    print(f'Tiempo de ejecucion: {end_time}')


def generate_posting_file(ocurrences_dict, output_dir, filepaths, file_ocurrences):
    start_time = time.time()
    print('\n--> Generando posting file')
    posting_file_name = os.path.join(output_dir, 'posting.txt')
    posting_index = 0
    with open(posting_file_name, 'w', encoding='utf-8') as posting_obj:
        for key, _ in ocurrences_dict.items():
            ocurrences_dict[key].append(posting_index)
            indexes = [file_ocurrences.index(dictionary) for dictionary in file_ocurrences if key in dictionary]
            # values = list(filter(lambda item: key in item, file_ocurrences))
            files = [filepaths[index] for index in indexes]
            for char in range(0,len(files)):
                posting_obj.write(f'{os.path.basename(files[char])}|{file_ocurrences[indexes[char]][key]}\n')
                posting_index += 1
    final_time = time.time()
    final_time = final_time - start_time
    print(f'\nTiempo de ejecucion: {final_time}')

    return ocurrences_dict

