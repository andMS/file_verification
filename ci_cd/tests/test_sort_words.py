import sys
import os
import re
import glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
import src.sort_words.sort_words as sw

class TestSortWords():
    def test_sort_words(self):
        re_chars = re.compile('\n')
        resources_dir = os.path.join(os.getcwd(), 'clean_tags\\*')
        logs_path = os.path.join(os.getcwd(), 'sort_words')
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
        files = glob.glob(resources_dir)
        for file in files:
            sorted_file_name = os.path.join(logs_path, f'sorted_{os.path.basename(file)}')
            exec_time = sw.sort_words_in_file(file, sorted_file_name, True)
            with open(sorted_file_name, 'r', encoding='utf-8') as output_obj:
                lines = output_obj.readlines()
                sorted_lines = sorted(lines, key=lambda x: re.sub(re_chars,'',x.lower()))
                assert lines == sorted_lines


    def test_negative_remove_tags(self):
        test_path = 'C:\\fake_path'
        exec_time = sw.sort_words_in_file(test_path,test_path, True)
        assert exec_time == 'NA'

    
    def test_check_logs(self):
        logs_path = os.path.join(os.getcwd(), 'sort_words')
        output_file = os.path.join(logs_path, 'temp3.txt')
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
        resources_dir = os.path.join(os.getcwd(), 'clean_tags\\*')
        files = glob.glob(resources_dir)
        sw.execute_sort_words(files, output_file, logs_path, True)
        with open(output_file, 'r', encoding='utf-8') as output_obj:
            match = False
            lines = output_obj.readlines()
            for file in files:
                rel_path = os.path.relpath(file)
                for line in lines:
                    if rel_path in line:
                        match = True
                assert match
