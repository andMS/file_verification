#!/usr/bin/env python

import os
import time
import sys
import argparse
from src.utils import helper
import src.open_file.open_file as op
import src.sort_words.sort_words as sw
import src.remove_tags.remove_tags as rt
import src.letters_sorted.letters_sorted as st
import src.find_ocurrences.find_ocurrences as fn
import src.general_ocurrences.find_all_ocurrences as fg

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
    print(' VERIFICADOR DE ARCHIVOS '.center(100, '*'))
    print(' Modo de ejecucion '.center(100, '*'))
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
        # Eighth
        # Nineth
        # Tenth
    else:
        if '1' in tests:
            first_act_name = os.path.join(output_dir, 'a1_equipo1.txt')
            output_logs.append(first_act_name)
            op.execute_open_file(input_dir, first_act_name)
        if '2' in tests:
            second_act_name = os.path.join(output_dir, 'a2_equipo1.txt')
            output_logs.append(second_act_name)
            clean_html_logs = os.path.join(output_dir,'clean_tags')
            helper.validate_logs_path(clean_html_logs)
            rt.execute_remove_tags(input_dir, output_logs[1], clean_html_logs)
        if '3' in tests:
            third_act_name = os.path.join(output_dir, 'a3_equipo1.txt')
            output_logs.append(third_act_name)
            clean_html_logs = os.path.join(output_dir,'clean_tags')
            if not os.path.exists(clean_html_logs):
                print('Clean tags needs to be executed first.')
                second_act_name = os.path.join(output_dir, 'a2_equipo1.txt')
                rt.execute_remove_tags(file_paths, second_act_name, clean_html_logs)
            file_paths = helper.get_all_files(clean_html_logs, '.html')
            sorted_logs = os.path.join(output_dir, 'sorted_logs')
            helper.validate_logs_path(sorted_logs)
            sw.execute_sort_words(file_paths, third_act_name, sorted_logs, True)
        if '4' in tests:
            fourth_act_name = execute_fourth_act(output_dir, input_dir)
            output_logs.append(fourth_act_name)
        if '5' in tests:
            fifth_act_name = os.path.join(output_dir, 'a5_equipo1.txt')
            output_logs.append(fifth_act_name)
            letters_logs = os.path.join(output_dir, 'letters_act4')
            if not os.path.exists(letters_logs):
                execute_fourth_act(output_dir, input_dir)
            file_paths = helper.get_all_files(letters_logs, '.html')
            tokenized = os.path.join(output_dir, 'tokenized')
            helper.validate_logs_path(tokenized)
            fn.execute_find_ocurrences(TOKENIZED_FILES, file_paths, fifth_act_name, tokenized)
        if '6' in tests:
            sixth_act_name = os.path.join(output_dir, 'a6_equipo1.txt')
            output_logs.append(sixth_act_name)
            ocurrences_dict = generate_dict_of_ocurrences(output_dir, input_dir, sixth_act_name)

        if '7' in tests:
            act_name = os.path.join(output_dir, 'a7_equipo1.txt')
            output_logs.append(act_name)
            ocurrences_dict, tokenized_paths, file_ocurrences = generate_dict_of_ocurrences(output_dir, input_dir, act_name)
            fg.generate_posting_file(ocurrences_dict, output_dir, tokenized_paths, file_ocurrences)

    return output_logs


def generate_dict_of_ocurrences(output_dir, input_dir, output_file):
    letters_logs = os.path.join(output_dir, 'letters_act4')
    if not os.path.exists(letters_logs):
        execute_fourth_act(output_dir, input_dir)
    file_paths = helper.get_all_files(letters_logs, '.html')
    tokenized_gen = os.path.join(output_dir, 'all_files_tokenized')
    helper.validate_logs_path(tokenized_gen)
    ocurrences_dict, file_ocurrences = fg.execute_find_all_ocurrences(file_paths, output_file, tokenized_gen, output_dir)
    tokenized_paths = helper.get_all_files(tokenized_gen, '.html')
    return ocurrences_dict, tokenized_paths, file_ocurrences


def execute_fourth_act(output_dir, input_dir):
    fourth_act_name = os.path.join(output_dir, 'a4_equipo1.txt')
    clean_html_logs = os.path.join(output_dir,'clean_tags')
    if not os.path.exists(clean_html_logs):
        print('Clean tags needs to be executed first.')
        helper.validate_logs_path(clean_html_logs)
        second_act_name = os.path.join(output_dir, 'a2_equipo1.txt')
        rt.execute_remove_tags(input_dir, second_act_name, clean_html_logs)
    file_paths = helper.get_all_files(clean_html_logs, '.html')
    letters_logs = os.path.join(output_dir, 'letters_act4')
    helper.validate_logs_path(letters_logs)
    st.execute_letters_sorted(file_paths, fourth_act_name, letters_logs)
    return fourth_act_name


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