import os
import re
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.utils import helper

def remove_html_tags(file: str, output_file: str) -> float:
    """ Function to remove HTML tags of a file.
        Args:
            file (<class 'str'>): path of the file to remove the tags.
            output_file (<class 'str'>): path of the file to write the clean file.
        Return:
            final_time (<class 'float'>): final execution time.
    """
    start_time = time.time()
    clean_re = re.compile('<.*?>|[<>]')
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


def execute_remove_tags(filepaths: list, output_file: str, logs_path: str) -> None:
    """ Helper function that executes remove_html_tags and writes a log file with the
        execution time.
        Args:
            filepaths (<class 'list'>): List of files to execute the function with.
            output_file (<class 'str'>): path of the file to write the execution logs.
            logs_path (<class 'str'>): path of the file to save the logs.
        Return:
            None.
    """
    start_time = time.time()
    counter = 0
    print(' Ejecutando: ACT 2. REMOVER ETIQUETAS HTML '.center(100, '*'))
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            output_obj.write('Prueba: remover etiquetas HTML.\n')
            output_obj.write('\n')
            for file in filepaths:
                counter += 1
                relative_path = os.path.relpath(file)
                clean_html_name = os.path.join(logs_path, f'clean_{os.path.basename(file)}')
                exec_time = remove_html_tags(file, clean_html_name)
                output_obj.write(f'{counter : >03}. {relative_path : <100}{exec_time:02.8f}\n')
            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion: {(end_time - start_time)}\n'
            output_obj.write(final_string)
            print(final_string)
    except OSError:
        print(f'No se pudo escribir en archivo de logs: {output_file}')
        helper.exit_program(1)
