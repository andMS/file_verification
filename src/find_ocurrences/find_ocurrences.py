import os
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.utils import helper
from collections import Counter

def find_ocurrences(file: str, output: str, ordered: bool) -> float:
    """ Function to sort all words of a file.
        Args:
            file (<class 'str'>): path of the file to sort words.
            output_file (<class 'str'>): path of the file to write the sorted file.
            remove_chars (<class 'bool'>): if True, all special characters will be removed.
        Return:
            final_time (<class 'float'>): final execution time.
    """
    start_time = time.time()
    ocurrences = {}
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as file_obj:
            lines = file_obj.readlines()
            clean_lines = [x.replace('\n', '') for x in lines]
            ocurrences = Counter(clean_lines)
            if ordered:
                ocurrences = dict(ocurrences.most_common())
            else:
                ocurrences = dict(sorted(ocurrences.items()))
        with open(output, 'w', encoding='utf-8') as output_obj:
            for key, value in ocurrences.items():
                output_obj.write(f'{key}: {value}\n')
            end_time = time.time()
            output_obj.write(f'\nTiempo total de ejecucion: {(end_time - start_time)}\n')
    except OSError:
        print(f'Could not open file')

    return ocurrences

def execute_find_ocurrences(tokenized_paths, filepaths: list, output_file: str, output_dir: str) -> None:
    """ Helper function that executes sort_only_words_in_file and writes a log file with the
        execution time.
        Args:
            filepaths (<class 'list'>): List of files to execute the function with.
            output_file (<class 'str'>): path of the file to write the execution logs.
        Return:
            None.
    """
    ocurrences = []
    print(' Ejecutando: ACT 5. ENCONTRAR NUMERO DE OCURRENCIAS '.center(100, '*'))
    filepaths = [x for x in filepaths for path in tokenized_paths if path in x]
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            # Ordered
            print('Encontrar ocurrencias por orden alfabetico')
            counter = Counter()
            ocurrences = []
            output_obj.write('--> Prueba: encontrar numero de ocurrencias en un archivo (orden alfabetico)\n')
            output_obj.write('\n')
            first_time = time.time()
            for file in filepaths:
                tokenized_alph = os.path.join(output_dir, f'tokenized_alphabetically_{os.path.basename(file.replace("letters_sorted_clean_",""))}')
                ocurrences.append(find_ocurrences(file, tokenized_alph, False))
            for element in ocurrences:
                counter.update(element)
            ocurrences = dict(sorted(counter.items()))
            for key, value in ocurrences.items():
                output_obj.write(f'{key}: {value}\n')
            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion: {(end_time - first_time)}\n'
            output_obj.write(final_string)
            print(final_string)

            # By frequency
            print('Encontrar ocurrencias por frecuencia')
            counter = Counter()
            ocurrences = []
            output_obj.write('\n--> Prueba: encontrar numero de ocurrencias en un archivo (orden de repeticion)\n')
            output_obj.write('\n')
            first_time = time.time()
            for file in filepaths:
                tokenized_frec = os.path.join(output_dir, f'tokenized_frequence_{os.path.basename(file.replace("letters_sorted_clean_",""))}')
                ocurrences.append(find_ocurrences(file, tokenized_frec, True))
            for element in ocurrences:
                counter.update(element)
            ocurrences = dict(counter.most_common())
            for key, value in ocurrences.items():
                output_obj.write(f'{key}: {value}\n')
            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion: {(end_time - first_time)}\n'
            output_obj.write(final_string)
            print(final_string)

    except OSError:
        print(f'No se pudo escribir en archivo de logs: {output_file}')
        helper.exit_program(1)
