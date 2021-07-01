"""
Detailed Testing of KIPET examples
"""
# Standard library imports
from pathlib import Path
import os
import subprocess
import sys
import time
import webbrowser

# Third party imports 
from jinja2 import Environment, FileSystemLoader


def run(cmd):
    os.environ['PYTHONUNBUFFERED'] = "1"
    proc = subprocess.Popen(cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
    )
    stdout, stderr = proc.communicate()
 
    return proc.returncode, stdout, stderr
 

class TestExamples():
    """Test to check if all of the example problems are working properly"""
    
    def __init__(self):
    
        self.dir_examples = Path.cwd().joinpath('examples')
        self.files = list(self.dir_examples.rglob("*.py"))
        self.file_dict = {}
        self.clean_logs()

    def run_examples(self):
        
        
        
        long_examples = [
            'Ex_2_estimation_direct_sigmas',
            'AD_6_sawall_SG_filter',
            'Ex_2_estimation_bound_prof_fixed_variance',
            'Ex_8_estimability',
            'Ex_7_concentration_CI'
            ]
        
        grades = {}
        flagpy = 0
        countpy = 0
        skip = 0
        
        print('Testing the example problems in folder: examples')
        number_of_examples = len(self.files)
        print(f'There are {number_of_examples} example problems to be evaluated')
        
        for n, file in enumerate(self.files):
            
            self.file_dict[n] = {}
            
            if file.stem in long_examples:
                print('Skipping this long one...')
                self.file_dict[n]['pass'] = False
                self.file_dict[n]['skipped'] = True
                self.file_dict[n]['file'] = file.stem    
                grades[file.stem] = None
                skip += 1
                continue
            
            else:
                self.file_dict[n]['skipped'] = False
            
            file = Path(file)
            margin = 10
            print(f'Running example ({n + 1}/{number_of_examples}):\n')
            print('File'.rjust(margin) + f' : {file.stem}')
            self.file_dict[n]['file'] = file.stem     
            
            start = time.time()
            flagpy, out, err = run([sys.executable, file, '1'])
            end = time.time()
            
            self.file_dict[n]['time'] = end - start
            
            if flagpy == 0:
                self.file_dict[n]['log'] = list(Path.cwd().rglob(f'log-{file.stem}*.txt'))[0]
            
            self.file_dict[n]['log_txt'] = out.decode()
            
            if flagpy == 0:
                log_file = Path(f"log-{file.stem}-*.txt")
                if log_file.is_file():
                    log_file.unlink()
                
            if flagpy!=0: 
                print('Status'.rjust(margin) + ' : Fail\n')
                countpy = countpy + 1
                flagpy=1
                grades[file.stem] = False 
                self.file_dict[n]['pass'] = False
                
            else:
                print('Status'.rjust(margin) + ' : Pass')
                print('Time'.rjust(margin) + f' : {end-start:0.4f}\n')
                grades[file.stem] = True
                self.file_dict[n]['pass'] = True
                
            print('Results'.rjust(margin) + f' : P: {n + 1 -countpy -skip} | F: {countpy} | S: {skip} | T: {n + 1} | R: {100*(n + 1 -countpy - skip)/(n + 1):0.2f}%\n')
            continue
        
        print(f'{countpy} files in {self.dir_examples} failed:')
        for file, grade in grades.items():
            if not grade:
                print(f'\t{file}')
            
        return grades
    
    def generate_report(self):
        """Generates an HTML report for the test suite.
        
        This provides a more useful interface for representing results than using individual charts.
        Logs for each example are included for further inspection.
        
        :return: None
        
        """
        current_dir = Path(__file__).parent
        templates_dir = (current_dir / 'templates').resolve()
        style_file = (templates_dir / 'report.css').resolve()
        prism_style_file = (templates_dir / 'prism.css').resolve()
        prism_js_file = (templates_dir / 'prism.js').resolve()
        
        with open(style_file, 'r+') as f:
            style_text = f.read()
        
        with open(prism_style_file, 'r+') as f:
            prism_css = f.read()
        
        with open(prism_js_file, 'r+') as f:
            prism_js = f.read()
    
        filename = (current_dir / 'test_report.html').resolve()
        env = Environment( loader = FileSystemLoader(templates_dir) )
        template = env.get_template('test_index.html')
        
        number_of_examples = len(self.file_dict)
        passing = sum([k['pass'] for k in self.file_dict.values()])
        skipped = sum([k['skipped'] for k in self.file_dict.values()])
        score = int(100*passing/number_of_examples)
        failing = number_of_examples - passing - skipped
        grades = [passing, failing, skipped, score]
        
        print(grades)
        
        t = time.localtime()
        
        with open(filename, 'w') as fh:
            fh.write(template.render(
                results = self.file_dict,
                style_text = style_text,
                prism_css = prism_css,
                prism_js = prism_js,
                grades = grades,
                date = f'{t.tm_year}-{t.tm_mon:02}-{t.tm_mday:02}-{t.tm_hour:02}-{t.tm_min:02}-{t.tm_sec:02}'
        
            ))
        
        webbrowser.open('file://' + os.path.realpath(filename))
        self.clean_logs()
        
        return None
    
    @staticmethod
    def clean_logs():
        
        current_dir = Path.cwd()
        logs = list(current_dir.rglob("log-*.txt"))
        
        for log in logs:
            if log.is_file():
                log.unlink()
                
        return None


if __name__ == '__main__':
    
    tests = TestExamples()
    tests.run_examples()
    tests.generate_report()
    