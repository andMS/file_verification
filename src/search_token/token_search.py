import time
import os
from src.utils import helper
import src.search_token.token_retrieval as tr

def optimized_search(output_file, output_dir):
    start_time = time.time()
    helper.format_msg_str(' Ejecutando: ACT 13. Busquedas de tokens ')
    with open(output_file, 'w', encoding='utf-8') as output_obj:
        msg_str = '--> BUSQUEDA DE TOKENS <--\n\n'
        print(msg_str)
        output_obj.write(msg_str)
        token_search_menu(output_file, output_dir)
    with open(output_file, 'a', encoding='utf-8') as output_obj:
        sec_msg = f'Tiempo final de busqueda de tokens: {time.time() - start_time}\n'
        print(sec_msg)
        output_obj.write(sec_msg)



def token_search_menu(output_file, output_dir):
    searches = 1
    print('Introduce el token que deseas buscar: ')
    token = input()
    with open(output_file, 'a') as output_obj:
        for _ in range(0,10):
            output_obj.write('.\n')
    token_retrieval(token, searches, output_file, output_dir)
    while True:
        print('Deseas buscar otro token? (y/n)')
        option = input()
        option = str(option.lower().strip())
        if option not in ['y', 'n','yes','no']:
            print('Opcion no valida. Intenta nuevamente')
        elif option in ['y', 'yes']:
            searches += 1
            print('Introduce el token a buscar:')
            token = input()
            token_retrieval(token, searches, output_file, output_dir)
        elif option in ['n', 'no']:
            break


def token_retrieval(token, counter, output_file, output_dir):
    start_time = time.time()
    token = token.strip().lower()
    posting_path = os.path.join(output_dir, 'posting_act12.txt')
    dict_path = os.path.join(output_dir, 'dictionary_act12.txt')
    documents_id = os.path.join(output_dir, 'documents_id.txt')
    docs_dict = tr.generate_document_id_dict(documents_id)
    posting_lines, dictionary, posting_weights = tr.generate_file_dicts(posting_path, dict_path)
    with open(output_file, 'a') as output_obj:
        file_limit = 0
        print(f'{counter}. Token: {token}')
        output_obj.write(f'{counter}. Token: {token}\n')
        try:
            positions = dictionary[token]
            msg_str = '***** Token encontrado en los siguientes documentos: *****\n'
            print(msg_str)
            output_obj.write(msg_str)
            # Sort by weight
            ocurrences = posting_lines[int(positions[1]):int(positions[0]) + int(positions[1])]
            weights = posting_weights[int(positions[1]):int(positions[0]) + int(positions[1])]
            ocurrences_dict = {ocurrences[x]:weights[x] for x in range(0,len(ocurrences))}
            sorted_occ = sorted(ocurrences_dict.items(), key=lambda x:x[1], reverse=True)
            for char in range(0, len(sorted_occ)):
                file_limit += 1
                if file_limit > 10:
                    break
                content = f'-> {docs_dict[sorted_occ[char][0]]}. Peso: {sorted_occ[char][1]}\n'
                print(content)
                output_obj.write(content)
            # for char in range(int(positions[1]), (int(positions[0]) + int(positions[1]))):
            #     file_limit += 1
            #     if file_limit > 10:
            #         break
            #     content = f'-> {docs_dict[posting_lines[char]]}\n'
            #     content = f'-> {docs_dict[sorted_occ[char]]}\n'
        except KeyError:
            msg_str = '-> Token no encontrado en los archivos.\n'
            print(msg_str)
            output_obj.write(msg_str)
        final_str = f'Tiempo de busqueda: {time.time() - start_time}\n\n'
        print(final_str)
        output_obj.write(final_str)
