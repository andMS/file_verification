import os
import re
import sys
import time
import argparse
from pathlib import Path
import src.utils.helper as helper

def open_file(file: str) -> float:
    """ Function to open/close files and check execution time.
        Args:
            file (<class 'str'>): path of the file to open/close.
        Return:
            exec_time (<class 'float'>): execution time of the action.
    """
    start_time = time.time()
    if os.path.exists(file):
        try:
            file_obj = open(file, 'r', encoding='utf-8')
            file_obj.close()
            end_time = time.time()
            exec_time = end_time - start_time
        except OSError:
            print(f'No se pudo abrir archivo: {file}')
            exec_time = 'NA'
    else:
        print(f'El archivo no existe: {file}')
        exec_time = 'NA'

    return exec_time


def remove_html_tags(file: str, output_file: str) -> float:
    """ Function to remove HTML tags of a file.
        Args:
            file (<class 'str'>): path of the file to remove the tags.
            output_file (<class 'str'>): path of the file to write the clean file.
        Return:
            final_time (<class 'float'>): final execution time.
    """
    start_time = time.time()
    clean_re = re.compile('<.*?>')
    clean_lines = []
    if os.path.exists(file):
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as html_file:
                lines = html_file.readlines()
                for line in lines:
                    clean_txt = re.sub(clean_re, '', line).strip()
                    if clean_txt != '':
                        clean_lines.append(clean_txt)
        except OSError:
            print(f'No se pudo abrir el archivo: {file}')
            final_time = 'NA'
        try:
            with open(output_file, 'w', encoding='utf-8') as output_obj:
                output_obj.write('\n'.join(str(element) for element in clean_lines))
        except OSError:
            print(f'No se pudo escribir el archivo nuevo: {output_file}')
            final_time = 'NA'
        end_time = time.time()
        final_time = end_time - start_time
    else:
        print(f'El archivo no existe: {file}')
        final_time = 'NA'

    return final_time


def sort_words_in_file(file: str, output_file: str, remove_chars:bool) -> float:
    """ Function to sort all words of a file.
        Args:
            file (<class 'str'>): path of the file to sort words.
            output_file (<class 'str'>): path of the file to write the sorted file.
            remove_chars (<class 'bool'>): if True, all special characters will be removed.
        Return:
            final_time (<class 'float'>): final execution time.
    """
    start_time = time.time()
    disallowed_chars_re = re.compile('[^A-Za-z0-9]|&[a-zA-Z]+')
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as file_obj:
            lines = file_obj.read().split()
            if remove_chars:
                clean_lines = [re.sub(disallowed_chars_re, '', line) for line in lines]
                lines = clean_lines
            lines.sort(key=lambda x: x.lower())
    except OSError:
        print(f'No se pudo abrir el archivo: {file}')
        final_time = 'NA'
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            output_obj.write('\n'.join(str(element) for element in lines))
        end_time = time.time()
        final_time = end_time - start_time
    except OSError:
        print(f'No se pudo crear el archivo: {output_file}')
        final_time = 'NA'

    return final_time


def execute_open_file(filepaths: list, output_file: str) -> None:
    """ Helper function that executes open_file and writes a log file with the
        execution time.
        Args:
            filepaths (<class 'list'>): List of files to execute the function with.
            output_file (<class 'str'>): path of the file to write the execution logs.
        Return:
            None.
    """
    start_time = time.time()
    helper.format_msg_str(' Ejecutando: ABRIR ARCHIVOS ')
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            output_obj.write('Prueba: Abrir y cerrar archivos.\n')
            output_obj.write('\n')
            for file in filepaths:
                exec_time = open_file(file)
                output_obj.write(f'{file : <100}{exec_time:02.8f}\n')
            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion: {(end_time - start_time)}\n'
            output_obj.write(final_string)
            print(final_string)
    except OSError:
        print(f'No se pudieron escribir los logs en archivo: {output_file}')
        exit_program(1)


def execute_remove_tags(filepaths: list, output_file: str, logs_path: str) -> None:
    """ Helper function that executes remove_html_tags and writes a log file with the
        execution time.
        Args:
            filepaths (<class 'list'>): List of files to execute the function with.
            output_file (<class 'str'>): path of the file to write the execution logs.
        Return:
            None.
    """
    start_time = time.time()
    helper.format_msg_str(' Ejecutando: REMOVER ETIQUETAS HTML ')
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            output_obj.write('Prueba: remover etiquetas HTML.\n')
            output_obj.write('\n')
            for file in filepaths:
                clean_html_name = os.path.join(logs_path, f'clean_{os.path.basename(file)}')
                exec_time = remove_html_tags(file, clean_html_name)
                output_obj.write(f'{file : <100}{exec_time:02.8f}\n')
            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion: {(end_time - start_time)}\n'
            output_obj.write(final_string)
            print(final_string)
    except OSError:
        print(f'No se pudo escribir en archivo de logs: {output_file}')
        exit_program(1)


def execute_sort_words(filepaths: list, output_file: str, logs_path: str, clean_char: bool) -> None:
    """ Helper function that executes sort_words_in_file and writes a log file with the
        execution time.
        Args:
            filepaths (<class 'list'>): List of files to execute the function with.
            output_file (<class 'str'>): path of the file to write the execution logs.
        Return:
            None.
    """
    start_time = time.time()
    helper.format_msg_str(' Ejecutando: ORDENAR PALABRAS EN ARCHIVO ')
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            output_obj.write('Prueba: ordenar palabras de un archivo.\n')
            output_obj.write('\n')
            for file in filepaths:
                sorted_file_name =  Path(logs_path, f'sorted_{os.path.basename(file)}')
                exec_time = sort_words_in_file(file, sorted_file_name, clean_char)
                output_obj.write(f'{file : <100}{exec_time:02.8f}\n')
            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion: {(end_time - start_time)}\n'
            output_obj.write(final_string)
            print(final_string)
    except OSError:
        print(f'No se pudo escribir en archivo de logs: {output_file}')
        exit_program(1)


def __parse_args() -> argparse.Namespace:
    """ Helper function to parse arguments from command line to execute the script with.
        Args:
            None.
        Return:
            args (<class 'argparse.Namespace'>): Arguments parsed.
    """
    sorted_logs_path = os.path.join(os.getcwd(), 'logs/sorted')
    clean_logs_path = os.path.join(os.getcwd(), 'logs/clean_html')
    logs_path = os.path.join(os.getcwd(), 'logs')
    file_paths = os.path.join(os.getcwd(), 'resources/Files')
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


def __get_all_filepaths(rootdir: str, file_type: str, search_subdirs:bool=False) -> list:
    """ Helper function to get all filepaths in a given rootdir.
        Args:
            rootdir (<class 'str'>): path to search files.
            file_type (<class 'str'>): extension of the files to search.
            search_subdirs (<class 'bool'>): option to search in subdirectories for files.
        Return:
            filepaths (<class 'list'>): list of filepaths in rootdir.
    """
    filepaths = []
    for root, _, files in os.walk(rootdir):
        for file in files:
            current_file = os.path.join(root, file)
            if current_file.lower().endswith(file_type):
                filepaths.append(current_file)
        if not search_subdirs:
            break

    return filepaths


def __validate_file_path(file_path: str, file_extension: str) -> list:
    """ Helper function to validate that the path that is given to work with is a valid
        path.
        Args:
            file_path (<class 'str'>): path of the file/directory to work with.
            file_extension (<class 'str'>): extension of the files to search.
        Return:
            paths (<class 'list'>): list with filepath/s to work with.
    """
    paths = []
    if os.path.isdir(file_path):
        paths = __get_all_filepaths(file_path, file_extension)
    elif os.path.isfile(file_path):
        if not file_path.endswith(file_extension):
            print('ADVERTENCIA: la extension indicada no coincide con la del archivo a utilizar.')
        paths.append(file_path)
    elif not os.path.exists(file_path):
        print('El directorio/archivo proporcionado no es valido. Introduce un path existente.')
        exit_program(1)

    return paths


def __validate_tests_to_execute_option(options: str) -> list:
    """ Helper function to validate that the given options of tests to execute are available.
        path.
        Args:
            options (<class 'str'>): string with tests to execute.
        Return:
            new_options (<class 'list'>): list of tests to execute.
    """
    possible_options = ['1','2','3']
    new_options = []
    if ',' in options:
        new_options = options.split(',')
        new_options = [x.strip(' ') for x in new_options]
        for element in new_options:
            if element not in possible_options:
                print(f'La opcion del test a ejecutar (seleccion: {options}) no es valido.'
                + 'Valores posibles: 1,2,3,"all"')
                exit_program(1)
    elif options.lower().strip(' ') == 'all':
        new_options.append(options.lower().strip(' '))
    else:
        if len(options) > 1:
            print(f'La opcion del test a ejecutar no es valido: {options}. Valores posibles:'
            + '1,2,3,"all"')
            exit_program(1)
        else:
            if options[0] not in possible_options:
                print(f'La opcion del test a ejecutar no es valido: {options}. Valores posibles:'
                + '1,2,3,"all"')
                exit_program(1)
            else:
                new_options.append(options[0])

    return new_options


def __validate_logs_path(logs_path: str) -> str:
    """ Helper function to validate/create the path to save the generated logs.
        path.
        Args:
            logs_path (<class 'str'>): path of the file/directory to save the logs.
        Return:
            logs_path (<class 'str'>): path of the file/directory to save the logs.
    """
    if not os.path.isdir(logs_path):
        try:
            os.mkdir(logs_path)
        except OSError as exception:
            print('No se pudo crear el directorio para los logs. Verifica que es un nombre valido.')
            print(f'Error: {exception}')
            exit_program(1)

    return logs_path


def present_working_exec_mode(parser: argparse.Namespace, tests_to_execute: list) -> None:
    """ Helper function to present the parameters to work with.
        Args:
            parser (<class 'argparse.Namespace'>): parser of the arguments.
        Return:
            None
    """
    tests_names = [ '1. Abrir archivos.', '2. Remover etiquetas HTML.',
                    '3. Ordenar palabras de un archivo.']
    helper.format_msg_str(' VERIFICADOR DE ARCHIVOS ')
    helper.format_msg_str(' Modo de ejecucion ')
    print(f'> Directorio/archivo a utilizar: {parser.root}')
    print(f'> Extension de archivos a utilizar: {parser.file_type}')
    print('> Tests a ejecutar:')
    if 'all' in tests_to_execute:
        for name in tests_names:
            print(f'---> {name}')
    else:
        for number in tests_to_execute:
            print(f'---> {tests_names[int(number) - 1]}')
    if '2' in parser.test_to_execute:
        print(f'> Path de los logs para test 2: {parser.clean_tags_dir}')
    if '3' in parser.test_to_execute:
        print(f'> Path de los logs para test 3: {parser.sorted_logs_dir}')


def exit_program(exit_code: int) -> None:
    """ Helper function to end the program with a given exit code.
        Args:
            exit_code (<class 'int'>): exit code int.
        Return:
            None
    """
    if exit_code != 0:
        print('Error durante la ejecucion.')

    sys.exit(exit_code)


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
    if 'all' in tests_to_execute:
        output_logs = [open_file_logs_name, remove_tags_logs_name, sort_letters_logs_name]
        execute_open_file(file_paths, open_file_logs_name)
        execute_remove_tags(file_paths, remove_tags_logs_name, clean_html_logs)
        file_paths = __get_all_filepaths(clean_html_logs, '.html')
        execute_sort_words(file_paths, sort_letters_logs_name, sorted_logs_dir, clean_chars)
    else:
        if '1' in tests_to_execute:
            output_logs.append(open_file_logs_name)
            execute_open_file(file_paths, open_file_logs_name)
        if '2' in tests_to_execute:
            output_logs.append(remove_tags_logs_name)
            execute_remove_tags(file_paths, remove_tags_logs_name, clean_html_logs)
        if '3' in tests_to_execute:
            output_logs.append(sort_letters_logs_name)
            file_paths = __get_all_filepaths(clean_html_logs, '.html')
            execute_sort_words(file_paths, sort_letters_logs_name, sorted_logs_dir, clean_chars)

    return output_logs


def main() -> None:
    """ Main function calls all helper functions and executes the tests. """
    start_time = time.time()
    parsed_args = __parse_args()
    tests_to_execute = __validate_tests_to_execute_option(parsed_args.test_to_execute)
    file_paths = __validate_file_path(parsed_args.root, parsed_args.file_type)
    logs_path = [parsed_args.output_dir, parsed_args.sorted_logs_dir, parsed_args.clean_tags_dir]
    for log in logs_path:
        __validate_logs_path(log)
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

if __name__ == '__main__':
    main()
