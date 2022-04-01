import os
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.utils import helper
from src.find_ocurrences.find_ocurrences import find_ocurrences
from collections import Counter, defaultdict


def execute_find_all_ocurrences(filepaths: list, output_file: str, token_output_dir: str, output_dir:str) -> None:
    """ Helper function that executes sort_only_words_in_file and writes a log file with the
        execution time.
        Args:
            filepaths (<class 'list'>): List of files to execute the function with.
            output_file (<class 'str'>): path of the file to write the execution logs.
        Return:
            None.
    """
    general = []
    ocurrences_dict = {}
    print(' Ejecutando: GENERAR DICCIONARIO DE OCURRENCIAS '.center(100, '*'))
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            print('Encontrar ocurrencias por orden alfabetico')
            counter = Counter()
            log_counter = 0
            output_obj.write('--> Prueba: encontrar numero de ocurrencias en un archivo (todos)\n')
            output_obj.write('\n')
            first_time = time.time()
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
            print(final_string)
            output_obj.write(final_string)

            output_dict_name = os.path.join(output_dir, 'dictionary.txt')
            final_time, ocurrences_dict = generate_ocurrences_dict(output_dict_name,general, counter)

            final_string = f'\nTiempo que tomo generar el diccionario: {final_time}\n'
            print(final_string)
            output_obj.write(final_string)

    except OSError:
        print(f'No se pudo escribir en archivo de logs: {output_file}')
        helper.exit_program(1)

    return ocurrences_dict, general


def generate_ocurrences_dict(output_file, file_ocurrences, general_counter):
    with open(output_file, 'w', encoding='utf-8') as output_obj:
        # File ocurrences is a list of dictionaries that contains all tokens and ocurrences per file
        # General counter is the counter that has the number of ocurrences of all tokens in all files
        ocurrences = dict(general_counter)
        msg_str = '--> Generando dictionario de occurencias en todos los archivos.\n'
        output_obj.write(f'{msg_str}\n')
        output_obj.write('Token | N# of occurrences | N# of files with token\n')
        first_time = time.time()
        print(msg_str)
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
            output_obj.write(f'{key}|{ocurrences[key]}|{value}\n')
        end_time = time.time()
    final_time = end_time - first_time

    return final_time, final_dict


def generate_posting_file(ocurrences_dict, output_dir, filepaths, file_ocurrences):
    print(helper.format_msg_str(' Generating posting file '))
    posting_file_name = os.path.join(output_dir, 'posting.txt')
    posting_content = []
    with open(posting_file_name, 'w', encoding='utf-8') as posting_obj:
        # for file in filepaths:
        #     with open(file, 'r', encoding='utf-8') as file_obj:
        #         lines = file_obj.readlines()
        #         for key, value in ocurrences_dict.items():
        #             if key in lines:
        #                 ocurrences_dict[key].append(os.path.relpath(file))
        # for key, value in ocurrences_dict.items():
        #     posting_obj.write(f'{key}: {value}')

        for key, value in ocurrences_dict.items():
            
            indexes = [file_ocurrences.index(dictionary) for dictionary in file_ocurrences if key in dictionary]
            # values = list(filter(lambda item: key in item, file_ocurrences))
            files = [filepaths[index] for index in indexes]
            for char in range(0,len(files)):
                posting_obj.write(f'{os.path.basename(files[char])}|{file_ocurrences[indexes[char]][key]}\n')

