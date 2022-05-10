#!/usr/bin/env python

from pathlib import Path
import os
import time
import sys
from src.utils import helper
import src.open_file.open_file as op
import src.sort_words.sort_words as sw
import src.remove_tags.remove_tags as rt
import src.letters_sorted.letters_sorted as st
import src.find_ocurrences.find_ocurrences as fn
import src.general_ocurrences.find_all_ocurrences as fg
import src.generate_dict_posting_file.dict_posting_file_creation as pf
import src.hash_table.hash_table_creation as hash_table
import src.stop_list.remove_elements as stop_list
import src.weight_tokens.weight_tokens as weight_t
import src.documents_id.document_id as doc_file
import src.search_token.token_retrieval as tr
import src.search_token.token_search as ts

TOKENIZED_FILES = ['simple.html', 'medium.html', 'hard.html','049.html']

def get_params(params):
    if len(params) < 3:
        print('El programa no recibio los parametros completos. Finalizando ejecucion')
        helper.exit_program(1)
    input_dir = params[0]
    output_dir = params[1]
    tests = params[2]
    tests = helper.validate_tests_to_execute_option(tests)
    return input_dir, output_dir, tests


def present_working_exec_mode(args: list, tests) -> None:
    """ Helper function to present the parameters to work with.
        Args:
            parser (<class 'argparse.Namespace'>): parser of the arguments.
        Return:
            None
    """
    helper.format_msg_str(' VERIFICADOR DE ARCHIVOS ')
    helper.format_msg_str(' Modo de ejecucion ')
    print(f'> Directorio/archivo a utilizar: {args[0]}')
    print(f'> Path de los logs: {args[1]}')
    print('> Tests a ejecutar:')
    if 'all' in tests:
        for name in helper.TESTS_NAMES:
            print(f'---> {name}')
    else:
        for number in tests:
            print(f'---> {helper.TESTS_NAMES[int(number) - 1]}')


def start_tests(tests, input_dir, output_dir):
    output_logs = []
    num_tests = 0
    if 'all' in tests:
        num_tests = len(helper.TESTS_NAMES)
        output_logs = [os.path.join(output_dir, f'a{x+1}_equipo1.txt') for x in range(0,num_tests)]
        # First
        op.execute_open_file(input_dir, output_logs[0])

        # Second
        clean_html_logs = os.path.join(output_dir,'clean_tags')
        helper.validate_logs_path(clean_html_logs)
        rt.execute_remove_tags(input_dir, output_logs[1], clean_html_logs)

        # Third
        file_paths = helper.get_all_files(clean_html_logs, '.html')
        sorted_logs = os.path.join(output_dir, 'sorted_logs')
        helper.validate_logs_path(sorted_logs)
        sw.execute_sort_words(file_paths, output_logs[2], sorted_logs, True)

        # Fourth
        letters_logs = os.path.join(output_dir, 'letters_act4')
        helper.validate_logs_path(letters_logs)
        st.execute_letters_sorted(file_paths, output_logs[3], letters_logs)

        # Fifth
        file_paths = helper.get_all_files(letters_logs, '.html')
        tokenized = os.path.join(output_dir, 'tokenized')
        helper.validate_logs_path(tokenized)
        fn.execute_find_ocurrences(TOKENIZED_FILES, file_paths, output_logs[4], tokenized)

        # Sixth
        tokenized_gen = os.path.join(output_dir, 'all_files_tokenized')
        helper.validate_logs_path(tokenized_gen)
        fg.execute_find_all_ocurrences(file_paths, output_logs[5], tokenized_gen)

        # Seventh
        pf.execute_create_dict_posting_file(file_paths, output_logs[6], tokenized_gen, output_dir)

        # Eighth
        hash_table_dict = os.path.join(output_dir, 'dictionary_hash_table.txt')
        posting_hash_table = os.path.join(output_dir, 'posting_hash_table.txt')
        hash_table.create_dictionary_hash_table(file_paths, output_logs[7], output_dir, tokenized_gen)
        del hash_table.HASH_TABLE

        # Nineth
        stop_list_path = str(Path(input_dir[0]).parent).replace('Files','')
        stop_list_path = os.path.join(stop_list_path, 'Actividad9_stoplist.txt')
        stop_list.execute_stop_list(stop_list_path, file_paths, output_logs[8], output_dir, tokenized_gen)
        del stop_list.HASH_TABLE

        # Tenth
        posting_file_path = os.path.join(output_dir, 'posting_stop_list.txt')
        dictionary_file_path = os.path.join(output_dir, 'dictionary_stop_list.txt')
        weight_t.execute_weight_tokens(posting_file_path, dictionary_file_path, output_logs[9], output_dir)

        # Eleventh
        document_id = os.path.join(output_dir, 'documents_id.txt')
        posting_path = os.path.join(output_dir, 'posting_weight_tokens.txt')
        id_dict = doc_file.generate_documents_id_file(output_logs[10], output_dir, input_dir)
        doc_file.modify_posting_file(output_dir, posting_path, id_dict)

        # Twelveth
        posting_act_12 = os.path.join(output_dir, 'posting_act12.txt')
        dict_act12 = os.path.join(output_dir, 'dictionary_act12.txt')
        tr.generate_files_non_stop_list(output_dir, hash_table_dict, document_id, posting_hash_table, output_logs[11])
        docs_dict = tr.generate_document_id_dict(document_id)
        posting_lines, dictionary_id = tr.generate_file_dicts(posting_act_12, dict_act12)
        tr.token_menu(output_logs[11], docs_dict, posting_lines, dictionary_id)

        # Thirteenth
        ts.optimized_search(output_logs[12], output_dir)

    else:
        output_logs = execute_individual_activities(tests, output_dir, input_dir)

    return output_logs


def execute_individual_activities(tests, output_dir, input_dir):
    act_4_sum = 5
    total_sum = 0
    for element in tests:
        total_sum = total_sum + int(element)
    num_tests = len(helper.TESTS_NAMES)
    output_logs = [os.path.join(output_dir, f'a{x+1}_equipo1.txt') for x in range(0,num_tests)]
    final_logs = []
    # First only executed if 1 is in tests to execute
    # Open files
    if '1' in tests:
        op.execute_open_file(input_dir, output_logs[0])
        final_logs.append(output_logs[0])
        if len(tests) == 1:
            return final_logs

    # REQUIRED for all tests
    # Remove HTML Tags
    clean_html_logs = os.path.join(output_dir,'clean_tags')
    if '2' in tests or not os.path.exists(clean_html_logs):
        final_logs.append(output_logs[1])
        if not os.path.exists(clean_html_logs) and '2' not in tests:
            print(  '\nAVISO: Los archivos sin etiquetas HTML no se encontraron.' +
                    ' Se tienen que remover las etiquetas HTML primero\n')
        helper.validate_logs_path(clean_html_logs)
        rt.execute_remove_tags(input_dir, output_logs[1], clean_html_logs)

    file_paths = helper.get_all_files(clean_html_logs, '.html')

    # Third - sort words in file
    if '3' in tests:
        final_logs.append(output_logs[2])
        sorted_logs = os.path.join(output_dir, 'sorted_logs')
        helper.validate_logs_path(sorted_logs)
        sw.execute_sort_words(file_paths, output_logs[2], sorted_logs, True)

    # Fourth - sort words alphabetically in lowercase
    # REQUIRED for all tests
    letters_logs = os.path.join(output_dir, 'letters_act4')
    if '4' in tests or (not os.path.exists(letters_logs) and total_sum >= act_4_sum):
        if not os.path.exists(letters_logs) and '4' not in tests:
            print(  '\nAVISO: Los archivos con las palabras ordenadas en minusculas no se encontraron.' +
                    ' Se tienen que ordenar las palabras primero.\n')
        final_logs.append(output_logs[3])
        helper.validate_logs_path(letters_logs)
        st.execute_letters_sorted(file_paths, output_logs[3], letters_logs)

    # Fifth - Count ocurrences
    file_paths = helper.get_all_files(letters_logs, '.html')
    if '5' in tests:
        final_logs.append(output_logs[4])
        tokenized = os.path.join(output_dir, 'tokenized')
        helper.validate_logs_path(tokenized)
        fn.execute_find_ocurrences(TOKENIZED_FILES, file_paths, output_logs[4], tokenized)

    # Sixth - Count words in all files
    # REQUIRED for activity 7
    tokenized_gen = os.path.join(output_dir, 'all_files_tokenized')
    required_tokenized = check_tokenized_dependencies(tests)
    if '6' in tests or (not os.path.exists(tokenized_gen) and required_tokenized):
        if not os.path.exists(tokenized_gen) and '6' not in tests:
            print(  '\nAVISO: Los archivos tokenizados no se encontraron.' +
                    ' Se tienen que tokenizar primero\n')
        final_logs.append(output_logs[5])
        helper.validate_logs_path(tokenized_gen)
        fg.execute_find_all_ocurrences(file_paths, output_logs[5], tokenized_gen)

    # Seventh - Create dictionary and posting file
    if '7' in tests:
        final_logs.append(output_logs[6])
        pf.execute_create_dict_posting_file(file_paths, output_logs[6], tokenized_gen, output_dir)

    # Eighth - Create dictionary and posting file with hash table implementation
    hash_table_dict = os.path.join(output_dir, 'dictionary_hash_table.txt')
    posting_hash_table = os.path.join(output_dir, 'posting_hash_table.txt')
    if '8' in tests or (('12' in tests or '13' in tests) and \
        (not os.path.exists(hash_table_dict) or not os.path.exists(posting_hash_table))):
        if (not os.path.exists(hash_table_dict) or not os.path.exists(posting_hash_table)) and \
            '8' not in tests:
            print(  '\nAVISO: Los archivos dictionary y posting hash table no se encontraron.'+
                    ' Se tienen que generar primero.\n')
        final_logs.append(output_logs[7])
        hash_table.create_dictionary_hash_table(file_paths, output_logs[7], output_dir, tokenized_gen)
        del hash_table.HASH_TABLE
        print(f'Archivos generados: \n-->{hash_table_dict}\n-->{posting_hash_table}\n-->{output_logs[7]}\n')

    # Nineth - Remove elements from stop list
    posting_file_path = os.path.join(output_dir, 'posting_stop_list.txt')
    dictionary_file_path = os.path.join(output_dir, 'dictionary_stop_list.txt')
    if '9' in tests or (('10' in tests or '11' in tests) and \
        (not os.path.exists(posting_file_path) or not os.path.exists(dictionary_file_path))):
        if (not os.path.exists(posting_file_path) or not os.path.exists(dictionary_file_path) and \
            '9' not in tests):
            print(  '\nAVISO: Los archivos dictionary y posting stop list no se encontraron.'+
                    ' Se tienen que generar primero.\n')
        final_logs.append(output_logs[8])
        stop_list_path = str(Path(input_dir[0]).parent).replace('Files','')
        stop_list_path = os.path.join(stop_list_path, 'Actividad9_stoplist.txt')
        stop_list.execute_stop_list(stop_list_path, file_paths, output_logs[8], output_dir, tokenized_gen)
        del stop_list.HASH_TABLE
        print(f'Archivos generados: \n-->{posting_file_path}\n-->{dictionary_file_path}\n-->{output_logs[8]}\n')

    # Tenth - create file with weight tokens
    posting_path = os.path.join(output_dir, 'posting_weight_tokens.txt')
    dictionary_defined_size = os.path.join(output_dir, 'dictionary_defined_size.txt')
    if '10' in tests or (('11' in tests) and \
        not os.path.exists(posting_path)):
        if not os.path.exists(posting_path) and '10' not in tests:
            print(  '\nAVISO: El archivo de weight tokens no se encontro.'+
                    ' Se tienen que generar primero.\n')
        final_logs.append(output_logs[9])
        weight_t.execute_weight_tokens(posting_file_path, dictionary_file_path, output_logs[9], output_dir)
        print(f'Archivos generados: \n-->{posting_path}\n-->{dictionary_defined_size}\n-->{output_logs[9]}\n')

    # Eleventh - Create document file
    document_id = os.path.join(output_dir, 'documents_id.txt')
    posting_doc_id = os.path.join(output_dir, 'posting_doc_id.txt')
    if '11' in tests or (('12' in tests or '13' in tests) and not os.path.exists(document_id)):
        if not os.path.exists(document_id) and '11' not in tests:
            print(  '\nAVISO: El archivo de ID de documentos no se encontro.'+
                    ' Se tienen que generar primero.\n')
        final_logs.append(output_logs[10])
        id_dict = doc_file.generate_documents_id_file(output_logs[10], output_dir, input_dir)
        if '11' in tests:
            doc_file.modify_posting_file(output_dir, posting_path, id_dict)
        print(f'Archivos generados: \n-->{document_id}\n-->{posting_doc_id}\n-->{output_logs[10]}\n')

    posting_act_12 = os.path.join(output_dir, 'posting_act12.txt')
    dict_act12 = os.path.join(output_dir, 'dictionary_act12.txt')

    # Twelveth - Create posting, dict and doc file w/o stop list and search tokens
    if '12' in tests or ('13' in tests and \
            (not os.path.exists(posting_act_12) or not os.path.exists(dict_act12))):
        if '12' not in tests and \
            (not os.path.exists(posting_act_12) or not os.path.exists(dict_act12)):
            print(  '\nAVISO: los archivos necesarios no se encontraron.'+
                    ' Se tienen que generar primero.\n')
        final_logs.append(output_logs[11])
        tr.generate_files_non_stop_list(output_dir, hash_table_dict, document_id, posting_hash_table, output_logs[11])
        docs_dict = tr.generate_document_id_dict(document_id)
        if '12' in tests:
            posting_lines, dictionary_id = tr.generate_file_dicts(posting_act_12, dict_act12)
            tr.token_menu(output_logs[11], docs_dict, posting_lines, dictionary_id)
        print(f'Archivos generados: \n-->{posting_act_12}\n-->{dict_act12}\n-->{output_logs[11]}\n')

    # Thirteenth - Optimized token searching
    if '13' in tests:
        final_logs.append(output_logs[12])
        ts.optimized_search(output_logs[12], output_dir)
        print(f'Archivos generados: \n-->{output_logs[12]}\n')

    return final_logs


def check_tokenized_dependencies(tests):
    required = False
    if '7' in tests:
        required = True
    if '8' in tests:
        required = True
    if '9' in tests:
        required = True
    if '10' in tests:
        required = True
    if '11' in tests:
        required = True
    if '12' in tests:
        required = True
    if '13' in tests:
        required = True
    return required


def main() -> None:
    start_time = time.time()
    args = sys.argv[1:]
    input_dir, output_dir, tests = get_params(args)
    input_dir = helper.validate_file_path(input_dir)
    output_dir = helper.validate_logs_path(output_dir)
    present_working_exec_mode(args, tests)
    final_output_files = start_tests(tests,input_dir,output_dir)
    for file in final_output_files:
        try:
            with open(file, 'a', encoding='utf-8') as file_obj:
                end_time = time.time()
                content = f'\nTiempo final del programa: {(end_time - start_time)} segundos.'
                file_obj.write(content)
        except OSError:
            print(f'No se pudo escribir el log final: {file}')
    end_time = time.time()
    print(f'Ejecucion terminada en {end_time - start_time} segundos.')
    helper.exit_program(0)


if __name__ == '__main__':
    main()
