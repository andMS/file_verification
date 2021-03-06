import os
import re
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.utils import helper

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
    lines = []
    disallowed_chars_re = re.compile('[^A-Za-z0-9]|&[a-zA-Z]+')
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as file_obj:
            lines = file_obj.read().split()
            if remove_chars:
                clean_lines = [re.sub(disallowed_chars_re, '', line) for line in lines]
                lines = clean_lines
            lines.sort(key=lambda x: x.lower())
        try:
            with open(output_file, 'w', encoding='utf-8') as output_obj:
                output_obj.write('\n'.join(str(element) for element in lines))
            end_time = time.time()
            final_time = end_time - start_time
        except OSError:
            print(f'No se pudo crear el archivo: {output_file}')
            final_time = 'NA'
    except OSError:
        print(f'No se pudo abrir el archivo: {file}')
        final_time = 'NA'

    return final_time

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
    counter = 0
    helper.format_msg_str(' Ejecutando: ACT3. ORDENAR PALABRAS EN ARCHIVO ')
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            output_obj.write('Prueba: ordenar palabras de un archivo.\n')
            output_obj.write('\n')
            for file in filepaths:
                counter += 1
                relative_path = os.path.relpath(file)
                sorted_file_name = os.path.join(logs_path, f'sorted_{os.path.basename(file)}')
                exec_time = sort_words_in_file(file, sorted_file_name, clean_char)
                output_obj.write(f'{counter : >03}. {relative_path : <100}{exec_time:02.8f}\n')
            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion: {(end_time - start_time)}\n'
            output_obj.write(final_string)
            print(final_string)
    except OSError:
        print(f'No se pudo escribir en archivo de logs: {output_file}')
        helper.exit_program(1)
