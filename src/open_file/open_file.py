import os
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.utils import helper

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
    counter = 0
    print(' Ejecutando: ACT 1. ABRIR ARCHIVOS '.center(100, '*'))
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            output_obj.write('Prueba: Abrir y cerrar archivos.\n')
            output_obj.write('\n')
            for file in filepaths:
                counter += 1
                relative_path = os.path.relpath(file)
                exec_time = open_file(file)
                output_obj.write(f'{counter : >03}. {relative_path : <100}{exec_time:02.8f}\n')
            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion: {(end_time - start_time)}\n'
            output_obj.write(final_string)
            print(final_string)
    except OSError:
        print(f'No se pudieron escribir los logs en archivo: {output_file}')
        helper.exit_program(1)
