import os
import sys
import time
from src.utils import helper

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

LEN_HASH_TABLE = 130000
HASH_TABLE = [[] for _ in range(LEN_HASH_TABLE)]

def execute_weight_tokens(posting_file, dict_file, log_file, logs_dir):
    general_start_time = time.time()
    weight_tokens = {}
    tokenized_files = os.path.join(logs_dir, 'all_files_tokenized')
    tokenized_files = helper.get_all_files(tokenized_files, '.html')
    helper.format_msg_str(' Ejecutando: ACT 10. WEIGHT TOKENS ')
    try:
        with open(log_file, 'w', encoding='utf-8') as log_obj:
            token_time = time.time()
            msg_str = '--> Obteniendo weight tokens\n'
            print(msg_str)
            log_obj.write(msg_str)
            log_counter = 0
            for file in tokenized_files:
                start_time = time.time()
                log_counter += 1
                with open(file, 'r', encoding='utf-8') as file_obj:
                    lines = file_obj.readlines()
                    ind_dict = create_dict_tokens(lines[:-2])
                    weight_tokens[os.path.basename(file)] = ind_dict
                end_time = time.time()
                log_obj.write(f'{log_counter : >03}. {os.path.relpath(file) : <100}{(end_time - start_time)}\n')
            end_time = time.time()
            msg_str = f'\nTiempo final de ejecucion (obtener weight tokens): {(end_time - token_time)}\n'
            log_obj.write(msg_str)
            print(msg_str)
            start_time = time.time()
            with open(dict_file, 'r', encoding='utf-8') as dict_obj:
                with open(posting_file, 'r', encoding='utf-8') as posting_obj:
                    msg_str = '\n--> Procesando diccionario y posting file\n'
                    print(msg_str)
                    log_obj.write(msg_str)
                    dict_lines = dict_obj.readlines()
                    posting_lines = posting_obj.readlines()
                    posting_content, times, dict_tokens = get_token_files(dict_lines, posting_lines, weight_tokens)
                    log_obj.write(f'\n---> {os.path.relpath(posting_file) : <100}{times[0]}\n')
                    log_obj.write(f'---> {os.path.relpath(dict_file) : <100}{times[1]}\n')
                    end_time = time.time()
                    msg_str = f'\nTiempo final de ejecucion (procesar posting file/diccionario): {(end_time - start_time)}\n'
                    log_obj.write(msg_str)
                    print(msg_str)
                    print('--> Generando posting file con weight tokens (16 bytes)\n')
                    posting_name = os.path.join(logs_dir, 'posting_weight_tokens.txt')
                    end_time = write_posting_file_weight_tokens(posting_content, posting_name)
                    print(f'Tiempo de ejecucion (creacion posting file): {end_time}\n')
                    print('--> Generando nuevo diccionario con tamano definido (40 bytes)\n')
                    dict_name = os.path.join(logs_dir, 'dictionary_defined_size.txt')
                    end_time = write_dictionary_weight_tokens(dict_tokens, dict_name)
                    print(f'Tiempo de ejecucion (creacion diccionario): {end_time}\n')
            log_obj.write(  '\nTiempo final de creacion de nuevo diccionario y posting file: ' +
                            f'{time.time() - general_start_time}\n')

            # log_temp = os.path.join(logs_dir, 'diccionario_weight.txt')
            # with open(log_temp, 'w') as temp:
            #     for key, values in weight_tokens.items():
            #         temp.write(f'{key}\n')
            #         temp.write(f'{values}\n')

    except OSError as error:
        print(f'No se pudo abrir el archivo: {error}')
        helper.exit_program(1)


def write_posting_file_weight_tokens(posting_content, posting_name):
    start_time = time.time()
    with open(posting_name, 'w', encoding='utf-8') as file_obj:
        for line in posting_content:
            # Lines of 16 bytes: 8 bytes for ID, 6 bytes for weight
            short_name = line[0].replace('tokenized_all_', '')
            short_name = short_name.replace('.html', '')
            message_str = f'{short_name:8}|{line[2]:6}\n'
            if len(message_str.encode('utf-8')) != 16:
                print(f'!! Tamano mayor a 16 bytes: {message_str}')
            file_obj.write(message_str)
    return time.time() - start_time


def write_dictionary_weight_tokens(dict_tokens, dict_name):
    start_time = time.time()
    with open(dict_name, 'w', encoding='utf-8') as dict_obj:
        for key, values in dict_tokens.items():
            # Lines of 40 bytes: 29 token, 1 whitespace, 3 file occurrences, 1 whitespace, 6 index
            message_str = f'{key[:28]:28} {values[0]:3} {values[1]:6}\n'
            if len(message_str.encode('utf-8')) != 40:
                print(f'!! Tamano mayor a 40 bytes: {message_str}')
            dict_obj.write(message_str)
    return time.time() - start_time


def create_dict_tokens(lines):
    dictionary = {}
    total_tokens = 0
    for line in lines:
        line = line.replace('\n', '')
        elements = line.split(':')
        total_tokens = int(total_tokens) + int(elements[1])
        dictionary[elements[0].strip()] = [elements[1].strip()]
    for line in lines:
        line = line.replace('\n', '')
        elements = line.split(':')
        weight = calculate_weight(elements[1], total_tokens)
        dictionary[elements[0].strip()].append(weight)
        # dictionary[elements[0].strip()].append(total_tokens)

    return dictionary


def calculate_weight(ocurrences, total_tokens):
    weight = (int(ocurrences) * 100) / int(total_tokens)
    return str(weight)[:6]


def get_token_files(dict_lines, posting_lines, weight_tokens):
    start_time = time.time()
    tokens = {}
    posting_files = []

    # Getting paths and number of tokens
    for line in posting_lines:
        line = line.replace('\n', '')
        elements = line.split('|')
        posting_files.append([elements[0].strip(),elements[1].strip()])
    posting_time = time.time() - start_time

    # Getting keys and indexes
    start_time = time.time()
    for line in dict_lines:
        line = line.replace('\n', '')
        elements = line.split()
        tokens[elements[0]] = [int(elements[1]), int(elements[2])]
    dict_time = time.time() - start_time

    # Populating with weights
    for key, values in tokens.items():
        index = int(values[0]) + int(values[1])
        for num in range(int(values[1]), index):
            file_key = posting_files[num][0]
            weight_value = weight_tokens[file_key][key][1]
            posting_files[num].append(weight_value)

    return posting_files, (posting_time, dict_time), tokens
