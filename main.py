import os
import time
import sys
import argparse
from src.utils import helper
import src.open_file.open_file as op
import src.sort_words.sort_words as sw
import src.remove_tags.remove_tags as rt
import src.letters_sorted.letters_sorted as st

def present_working_exec_mode(parser: argparse.Namespace, tests_to_execute: list) -> None:
    """ Helper function to present the parameters to work with.
        Args:
            parser (<class 'argparse.Namespace'>): parser of the arguments.
        Return:
            None
    """
    tests_names = [ '1. Abrir archivos.', '2. Remover etiquetas HTML.',
                    '3. Ordenar palabras de un archivo.', '4. Ordenar por orden alfabetico en minusculas.']
    print(' VERIFICADOR DE ARCHIVOS '.center(100, '*'))
    print(' Modo de ejecucion '.center(100, '*'))
    print(f'> Directorio/archivo a utilizar: {parser.root}')
    print(f'> Extension de archivos a utilizar: {parser.file_type}')
    print('> Tests a ejecutar:')
    if 'all' in tests_to_execute:
        for name in tests_names:
            print(f'---> {name}')
    else:
        for number in tests_to_execute:
            print(f'---> {tests_names[int(number) - 1]}')
    if '2' in parser.test_to_execute or 'all' in parser.test_to_execute:
        print(f'> Path de los logs para test 2: {parser.clean_tags_dir}')
    if '3' in parser.test_to_execute or 'all' in parser.test_to_execute:
        print(f'> Path de los logs para test 3: {parser.sorted_logs_dir}')


def start_tests(parser: argparse.Namespace, tests_to_execute: list, file_paths: list) -> list:
    """ Helper function that will check the selected tests and execute them.
        Args:
            parser (<class 'argparse.Namespace'>): parser of the arguments.
            tests_to_execute (<class 'list'>): list with number of tests to execute.
            file_paths (<class 'list'>): list with all filepaths to execute the tests on.
        Return:
            output_logs (<class 'list'>): list with all the output files to write.
    """
    output_logs = []
    output_dir = parser.output_dir
    clean_html_logs = parser.clean_tags_dir
    sorted_logs_dir = parser.sorted_logs_dir
    clean_chars = parser.clean_chars
    open_file_logs_name = os.path.join(output_dir, 'a1_equipo1.txt')
    remove_tags_logs_name = os.path.join(output_dir, 'a2_equipo1.txt')
    sort_letters_logs_name = os.path.join(output_dir, 'a3_equipo1.txt')
    letters_sorted_logs_name = os.path.join(output_dir, 'a4_equipo1.txt')
    if 'all' in tests_to_execute:
        output_logs = [open_file_logs_name, remove_tags_logs_name, sort_letters_logs_name]
        op.execute_open_file(file_paths, open_file_logs_name)
        rt.execute_remove_tags(file_paths, remove_tags_logs_name, clean_html_logs)
        file_paths = helper.get_all_files(clean_html_logs, '.html')
        print(file_paths[-1])
        sw.execute_sort_words(file_paths, sort_letters_logs_name, sorted_logs_dir, clean_chars)
    else:
        if '1' in tests_to_execute:
            output_logs.append(open_file_logs_name)
            op.execute_open_file(file_paths, open_file_logs_name)
        if '2' in tests_to_execute:
            output_logs.append(remove_tags_logs_name)
            rt.execute_remove_tags(file_paths, remove_tags_logs_name, clean_html_logs)
        if '3' in tests_to_execute:
            output_logs.append(sort_letters_logs_name)
            if not os.path.exists(clean_html_logs):
                print('Clean tags needs to be executed first.')
                rt.execute_remove_tags(file_paths, remove_tags_logs_name, clean_html_logs)
            file_paths = helper.get_all_files(clean_html_logs, '.html')
            sw.execute_sort_words(file_paths, sort_letters_logs_name, sorted_logs_dir, clean_chars)
        if '4' in tests_to_execute:
            output_logs.append(letters_sorted_logs_name)
            if not os.path.exists(clean_html_logs):
                print('Clean tags needs to be executed first.')
                rt.execute_remove_tags(file_paths, remove_tags_logs_name, clean_html_logs)
            file_paths = helper.get_all_files(clean_html_logs, '.html')
            ot_dir = os.path.join(parser.output_dir, 'letters_act4')
            helper.validate_logs_path(ot_dir)
            st.execute_letters_sorted(file_paths, letters_sorted_logs_name, ot_dir)

    return output_logs


def __parse_args() -> argparse.Namespace:
    """ Helper function to parse arguments from command line to execute the script with.
        Args:
            None.
        Return:
            args (<class 'argparse.Namespace'>): Arguments parsed.
    """
    sorted_logs_path = os.path.join(os.getcwd(), 'logs\sorted')
    clean_logs_path = os.path.join(os.getcwd(), 'logs\clean_html')
    logs_path = os.path.join(os.getcwd(), 'logs')
    file_paths = os.path.join(os.getcwd(), 'resources\Files')
    parser = argparse.ArgumentParser(description='Files Verification System')
    parser.add_argument('-c', '--cleanChars', dest='clean_chars', default=True, type=bool,
                        help='Indica si se eliminaran caracteres especiales en las pruebas.'
                        + 'Default: True')
    parser.add_argument('-e', '--execTest', dest='test_to_execute', default='all',
                        help='Test a ejecutar: "1" para Abrir archivos.'
                        + '"2" para remover etiquetas HTML. '
                        + '"3" para acomodar las letras de un archivo.'
                        + '"all" para ejecutar todas las pruebas. Default: all')
    parser.add_argument('-f', '--fileType', dest='file_type', default='.html', type=str,
                        help='Extension de los archivos a manipular al buscar en un directorio.'
                        + 'Default: .html')
    parser.add_argument('-s', '--sortedLogsDir', dest='sorted_logs_dir', default=sorted_logs_path,
                        type=str, help='Directorio para los logs de la prueba 3.'
                        + f'Default: {sorted_logs_path}')
    parser.add_argument('-o', '--outputDir', dest='output_dir', default=logs_path,
                        type=str, help='Directorio en donde se guardaran los logs generados.'
                        + f'Default: {logs_path}')
    parser.add_argument('-t', '--cleanTagsDir', dest='clean_tags_dir', default=clean_logs_path,
                        type=str, help='Directorio para los logs de la prueba 2.'
                        + f'Default: {clean_logs_path}')
    parser.add_argument('-r', '--rootDir', dest='root', default=file_paths, type=str,
                        help='Directorio/archivo en donde se ejecutara la herramienta.'
                        + f'Default: {file_paths}')
    args = parser.parse_args()

    return args


def main() -> None:
    """ Main function calls all helper functions and executes the tests. """
    start_time = time.time()
    parsed_args = __parse_args()
    tests_to_execute = helper.validate_tests_to_execute_option(parsed_args.test_to_execute)
    file_paths = helper.validate_file_path(parsed_args.root, parsed_args.file_type)
    logs_path = [parsed_args.output_dir, parsed_args.sorted_logs_dir, parsed_args.clean_tags_dir]
    for log in logs_path:
        helper.validate_logs_path(log)
    present_working_exec_mode(parsed_args, tests_to_execute)
    final_output_files = start_tests(parsed_args, tests_to_execute, file_paths)
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
