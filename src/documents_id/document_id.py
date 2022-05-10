import time
import os
import sys
from src.utils import helper

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

def generate_documents_id_file(log_file, logs_dir, filepaths):
    helper.format_msg_str(' Ejecutando: ACT 11. Generando archivo documents ')
    general_time = time.time()
    documents_id = {}
    document_id_name = os.path.join(logs_dir, 'documents_id.txt')
    with open(log_file, 'w', encoding='utf-8') as log_obj:
        log_obj.write('--> Generando archivo documents\n')
        with open(document_id_name, 'w', encoding='utf-8') as document_obj:
            counter = 0
            for file in filepaths:
                file_time = time.time()
                counter += 1
                documents_id[file] = counter
                document_obj.write(f'{counter : >03} {os.path.basename(file) : >10}\n')
                file_time = time.time() - file_time
                log_obj.write(f'{counter : >03}. {os.path.relpath(file) : <100}{file_time}\n')
        log_obj.write(f'Tiempo de ejecucion: {time.time() - general_time}\n')

    return documents_id


def modify_posting_file(output_dir, posting_path, id_dict):
    new_posting_path = os.path.join(output_dir, 'posting_doc_id.txt')
    with open(new_posting_path, 'w', encoding='utf-8') as output_obj:
        with open(posting_path, 'r', encoding='utf-8') as posting_obj:
            lines = posting_obj.readlines()
            for line in lines:
                content = line.split('|')
                for key in id_dict.keys():
                    if str(content[0]).strip() in key:
                        content.append(id_dict[key])
                output_obj.write(f'{content[2] :>3} | {content[1]}')
