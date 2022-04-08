import os
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from src.utils import helper
from src.find_ocurrences.find_ocurrences import find_ocurrences
from collections import Counter, defaultdict


def execute_find_all_ocurrences(filepaths: list, output_file: str, output_dir: str) -> None:
    """ Helper function that executes sort_only_words_in_file and writes a log file with the
        execution time.
        Args:
            filepaths (<class 'list'>): List of files to execute the function with.
            output_file (<class 'str'>): path of the file to write the execution logs.
        Return:
            None.
    """
    general = []
    helper.format_msg_str(' Ejecutando: ACT 6. ENCONTRAR TODAS LAS OCURRENCIAS ')
    try:
        with open(output_file, 'w', encoding='utf-8') as output_obj:
            print('Encontrar ocurrencias por orden alfabetico')
            counter = Counter()
            ocurrences = []
            output_obj.write('--> Prueba: encontrar numero de ocurrencias en un archivo (todos)\n')
            output_obj.write('\n')
            first_time = time.time()
            for file in filepaths:
                tokenized_alph = os.path.join(output_dir, f'tokenized_all_{os.path.basename(file.replace("letters_sorted_clean_",""))}')
                general.append(find_ocurrences(file, tokenized_alph, False))
            for element in general:
                counter.update(element)
            ocurrences = dict(counter)

            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion: {(end_time - first_time)}\n'
            print(final_string)
            output_obj.write(final_string)
            msg_str = '\n--> Prueba: Buscando ocurrencias en todos los archivos.\n'
            output_obj.write('\nToken | N# of occurrences | N# of filesw with token\n')
            first_time = time.time()
            print(msg_str)
            
            output_obj.write(f'\n{msg_str}\n')

            data = [j for i in general for j in i.keys()]
            temp_dict = defaultdict(int)
            for key in data:
                temp_dict[key] += 1

            for key, value in temp_dict.items():
                output_obj.write(f'{key}|{ocurrences[key]}|{value}\n')
            end_time = time.time()
            final_string = f'\nTiempo total de ejecucion: {(end_time - first_time):02.2f}\n'
            output_obj.write(final_string)

    except OSError:
        print(f'No se pudo escribir en archivo de logs: {output_file}')
        helper.exit_program(1)
