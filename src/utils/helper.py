# -*- coding: utf-8 -*-
import os
import sys
import PyPDF2

TESTS_NAMES = [ '1. Abrir archivos.', '2. Remover etiquetas HTML.',
                '3. Ordenar palabras de un archivo.', '4. Ordenar por orden alfabetico en minusculas.',
                '5. Contabilizar ocurrencias.', '6. Contar palabras en todos los archivos.',
                '7. Archivo Posting', '8. Hash Table', '9. Stop List', '10. Weight Tokens']

MINIMAL_OCURRENCES = 5

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


def get_all_files(rootdir: str, file_type: str, search_subdirs:bool=False) -> list:
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


def validate_file_path(file_path: str, file_extension: str = 'html') -> list:
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
        paths = get_all_files(file_path, file_extension)
    elif os.path.isfile(file_path):
        if not file_path.endswith(file_extension):
            print('ADVERTENCIA: la extension indicada no coincide con la del archivo a utilizar.')
        paths.append(file_path)
    elif not os.path.exists(file_path):
        print('El directorio/archivo proporcionado no es valido. Introduce un path existente.')
        exit_program(1)

    return paths


def validate_tests_to_execute_option(options: str) -> list:
    """ Helper function to validate that the given options of tests to execute are available.

        Args:
            options (<class 'str'>): string with tests to execute.
        Return:
            new_options (<class 'list'>): list of tests to execute.
    """
    possible_options = [str(x+1) for x in range(0,len(TESTS_NAMES))]
    new_options = []
    if ',' in options:
        new_options = options.split(',')
        new_options = list(set([x.strip(' ') for x in new_options]))
        for element in new_options:
            if element not in possible_options:
                print(f'La opcion del test a ejecutar (seleccion: {options}) no es valido.'
                + 'Valores posibles: 1,2,3,4,5,6,7,8,9,10,"all"')
                exit_program(1)
    elif options.lower().strip(' ') == 'all':
        new_options.append(options.lower().strip(' '))
    else:
        if options not in possible_options:
            print(f'La opcion del test a ejecutar no es valido: {options}. Valores posibles:'
            + '1,2,3,4,5,6,7,8,9,10,"all"')
            exit_program(1)
        else:
            new_options.append(options)

    return new_options


def validate_logs_path(logs_path: str) -> str:
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


def format_msg_str(msg_str):
    print(msg_str.center(100, '*'))


def convert_pdf_to_text(pdf_path):
    final_content = []
    with open(pdf_path, 'rb') as pdf_obj:
        pdf_reader = PyPDF2.PdfFileReader(pdf_obj)
        for num in range(0, pdf_reader.numPages):
            page = pdf_reader.getPage(num)
            content = page.extractText()
            final_content.append(content.decode(encoding='utf-8'))
    return final_content

def hashing_function(key, hash_table):
    key = hash(key)
    return key % len(hash_table)


def insert_hash_table(hash_table, key, value):
    hash_key = hashing_function(key, hash_table)
    key_exists = False
    bucket = hash_table[hash_key]
    for index, kv in enumerate(bucket):
        k, v = kv
        if key == k:
            key_exists = True
            break
    if key_exists:
        bucket[index][1].append(value)
    else:
        bucket.append((key, value))


def search_hash_table(hash_table, key):
    hash_key = hashing_function(key, hash_table)
    bucket = hash_table[hash_key]
    for _, kv in enumerate(bucket):
        k, v = kv
        if key == k:
            return v


def delete_from_hash_table(hash_table, key):
    hash_key = hashing_function(key, hash_table)
    key_exists = False
    bucket = hash_table[hash_key]
    for index, kv in enumerate(bucket):
        k, v = kv
        if key == k:
            key_exists = True
            break
    if key_exists:
        del bucket[index]
