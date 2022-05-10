import os
import time
import src.utils.helper as helper
import src.weight_tokens.weight_tokens as wt

def generate_files_non_stop_list(logs_dir, dict_file, document_id, posting_path, logs_path):
    start_time = time.time()
    helper.format_msg_str(' Ejecutando: ACT 12. BUSQUEDAS EN DICCIONARIO ')
    weight_tokens = {}
    with open(logs_path, 'w', encoding='utf-8') as logs_obj:
        token_time = time.time()
        msg_str = '--> Obteniendo weight tokens: \n'
        print(msg_str)
        logs_obj.write(msg_str)
        log_counter = 0
        tokenized_files = os.path.join(logs_dir, 'all_files_tokenized')
        tokenized_files = helper.get_all_files(tokenized_files, '.html')
        for file in tokenized_files:
            file_time = time.time()
            log_counter += 1
            with open(file, 'r', encoding='utf-8') as file_obj:
                lines = file_obj.readlines()
                ind_dict = wt.create_dict_tokens(lines[:-2])
                weight_tokens[os.path.basename(file)] = ind_dict
            logs_obj.write(f'{log_counter : >03}. {os.path.relpath(file) : <100}{(time.time() - file_time)}\n')
        msg_str = f'\nTiempo final de ejecucion (obtener weight tokens): {(time.time() - token_time)}\n'
        logs_obj.write(msg_str)
        print(msg_str)

        # log_temp = os.path.join(logs_dir, 'diccionario_weight.txt')
        # with open(log_temp, 'w') as temp:
        #     for key, values in weight_tokens.items():
        #         temp.write(f'{key}\n')
        #         temp.write(f'{values}\n')

        with open(dict_file,'r') as ex:
            with open(posting_path, 'r') as ex2:
                dict_lines = ex.readlines()
                posting_lines = ex2.readlines()
                posting_content, times, _ = wt.get_token_files(dict_lines, posting_lines, weight_tokens)
        print('--> Generando posting file con weight tokens (sin stop list)\n')
        start_time = time.time()
        id_dicts = generate_document_id_dict(document_id)
        logs_obj.write(f'\n---> {os.path.relpath(posting_path) : <100}{times[0]}\n')
        logs_obj.write(f'---> {os.path.relpath(dict_file) : <100}{times[1]}\n')
        generate_posting_non_stoplist(logs_dir, id_dicts, posting_content)
        print('\n--> Generando nuevo diccionario\n')
        with open(dict_file, 'r', encoding='utf-8') as dict_obj:
            newname = os.path.join(logs_dir, 'dictionary_act12.txt')
            lines = dict_obj.readlines()
            with open(newname, 'w', encoding='utf-8') as new_obj:
                for line in lines:
                    content = line.split()
                    new_obj.write(f'{content[0]:28} {content[1]:3} {content[2]:6}\n')
        msg_str = f'\nTiempo final de ejecucion (creacion de nuevo diccionario y posting file): {time.time() - start_time}\n'
        print(msg_str)
        logs_obj.write(msg_str)


def generate_file_dicts(posting_path, dictionary_path):
    # Generate posting_dict
    posting_lines = []
    posting_weights = []
    with open(posting_path, 'r', encoding='utf-8') as posting_obj:
        lines = posting_obj.readlines()
        for line in lines:
            posting_lines.append(line.split('|')[0].strip())
            posting_weights.append(line.split('|')[1].strip())
    # Generate dictionary dict
    dictionary_id = {}
    with open(dictionary_path, 'r', encoding='utf-8') as dictionary_obj:
        lines = dictionary_obj.readlines()
        for line in lines:
            elements = line.split()
            dictionary_id[elements[0]] = [elements[1], elements[2]]

    return posting_lines, dictionary_id, posting_weights


def generate_document_id_dict(document_path):
    # Generate document ID dict
    document_id = {}
    with open(document_path, 'r', encoding='utf-8') as document_obj:
        lines = document_obj.readlines()
        for line in lines:
            elements = line.split()
            document_id[elements[0]] = elements[1]
    return document_id


def generate_posting_non_stoplist(output_dir, ids_dict, posting_content):
    newpath = os.path.join(output_dir, 'posting_act12.txt')
    with open(newpath, 'w', encoding='utf-8') as output_obj:
        for element in posting_content:
            id = element[0].replace('tokenized_all_', '')
            weight = element[2]
            for key, value in ids_dict.items():
                if id == value:
                    output_obj.write(f'{key:>3} | {weight}\n')


def token_menu(output_logs, docs_dict, posting_lines, dictionary_id):
    with open(output_logs, 'a', encoding='utf-8') as output_obj:
        start_time = time.time()
        print('\n--> BUSQUEDA DE TOKENS <--\n')
        print('Introduce el token que deseas buscar: ')
        token = input()
        search_token(docs_dict, posting_lines, dictionary_id, token)
        while True:
            print('Deseas buscar otro token? (y/n)')
            option = input()
            option = str(option.lower().strip())
            if option not in ['y', 'n']:
                print('Opcion no valida. Intenta nuevamente')
            elif option == 'y':
                print('Introduce el token a buscar:')
                token = input()
                search_token(docs_dict, posting_lines, dictionary_id, token)
            elif option == 'n':
                break
        msg_str = f'\nTiempo final busqueda de tokens: {time.time() - start_time}\n'
        print(msg_str)
        output_obj.write(msg_str)


def search_token(docs_dict, posting_lines, dictionary_id, token):
    start_time = time.time()
    token = token.strip().lower()
    print(f'Token a buscar: {token}\n')
    try:
        positions = dictionary_id[token]
        print('Token encontrado en los siguientes documentos:\n')
        for x in range(int(positions[1]), (int(positions[0]) + int(positions[1]))):
            print(f'-> {docs_dict[posting_lines[x]]}')
    except KeyError:
        print('Token no se encuentra en los archivos.\n')
    print(f'Tiempo de busqueda: {time.time() - start_time}\n')
