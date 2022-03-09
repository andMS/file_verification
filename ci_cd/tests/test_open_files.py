import sys
import os
import glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
import src.open_file.open_file as of

class TestOpenFiles():
    def test_open_file(self):
        resources_dir = os.path.join(os.getcwd(), 'resources\\Files\\*')
        files = glob.glob(resources_dir)
        for file in files:
            exec_time = of.open_file(file)
            assert isinstance(exec_time, float)


    def test_negative_open_file(self):
        test_path = 'C:\\fake_path'
        exec_time = of.open_file(test_path)
        assert exec_time == 'NA'


    def test_log_files(self):
        logs_path = os.path.join(os.getcwd(), 'temp_logs')
        output_file = os.path.join(logs_path, 'temp1.txt')
        resources_dir = os.path.join(os.getcwd(), 'resources\\Files\\*')
        files = glob.glob(resources_dir)
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
        of.execute_open_file(files, output_file)
        assert os.path.exists(output_file)

    
    def test_check_logs(self):
        logs_path = os.path.join(os.getcwd(), 'temp_logs')
        output_file = os.path.join(logs_path, 'temp1.txt')
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
        resources_dir = os.path.join(os.getcwd(), 'resources\\Files\\*')
        files = glob.glob(resources_dir)
        of.execute_open_file(files, output_file)
        with open(output_file, 'r', encoding='utf-8') as output_obj:
            match = False
            lines = output_obj.readlines()
            for file in files:
                rel_path = os.path.relpath(file)
                for line in lines:
                    if rel_path in line:
                        match = True
                assert match
