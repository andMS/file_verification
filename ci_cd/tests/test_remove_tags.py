import sys
import os
import glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
import src.remove_tags.remove_tags as rt

class TestRemoveTags():
    def test_remove_tags(self):
        resources_dir = os.path.join(os.getcwd(), 'resources\\Files\\*')
        logs_path = os.path.join(os.getcwd(), 'clean_tags')
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
        files = glob.glob(resources_dir)
        for file in files:
            clean_html_name = os.path.join(logs_path, f'clean_{os.path.basename(file)}')
            exec_time = rt.remove_html_tags(file, clean_html_name)
            with open(clean_html_name, 'r', encoding='utf-8') as output_obj:
                lines = output_obj.readlines()
                for line in lines:
                    assert '<' not in line and '>' not in line


    def test_negative_remove_tags(self):
        test_path = 'C:\\fake_path'
        exec_time = rt.remove_html_tags(test_path, test_path)
        assert exec_time == 'NA'

    
    def test_check_logs(self):
        logs_path = os.path.join(os.getcwd(), 'clean_tags')
        output_file = os.path.join(logs_path, 'temp2.txt')
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
        resources_dir = os.path.join(os.getcwd(), 'resources\\Files\\*')
        files = glob.glob(resources_dir)
        rt.execute_remove_tags(files, output_file, logs_path)
        with open(output_file, 'r', encoding='utf-8') as output_obj:
            match = False
            lines = output_obj.readlines()
            for file in files:
                rel_path = os.path.relpath(file)
                for line in lines:
                    if rel_path in line:
                        match = True
                assert match
